#!/usr/bin/env python3
"""
Daily Reflection Tree Agent
A deterministic CLI reflection tool. No LLM calls at runtime.
Usage: python agent.py [--tree path/to/reflection-tree.json]
"""

import json
import sys
import time
import argparse
import textwrap
from pathlib import Path


# ─── Terminal helpers ────────────────────────────────────────────────────────

def clear():
    print("\033[H\033[J", end="")

def slow_print(text, delay=0.018):
    for char in text:
        print(char, end="", flush=True)
        if char in ".!?\n":
            time.sleep(delay * 4)
        else:
            time.sleep(delay)
    print()

def wrap(text, width=70):
    paragraphs = text.split("\n")
    result = []
    for p in paragraphs:
        if p.strip() == "":
            result.append("")
        else:
            result.extend(textwrap.wrap(p, width))
    return "\n".join(result)

def divider():
    print("\n" + "─" * 60 + "\n")

def header():
    clear()
    print("\n")
    print("  ╔═══════════════════════════════════════════╗")
    print("  ║       THE DAILY REFLECTION TREE           ║")
    print("  ╚═══════════════════════════════════════════╝")
    print()

def section_label(label):
    print(f"\n  ▸ {label.upper()}\n")


# ─── State management ────────────────────────────────────────────────────────

class State:
    def __init__(self):
        self.answers = {}          # node_id -> chosen option value
        self.signals = {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"altrocentric": 0, "self": 0},
        }
        self.path = []             # list of visited node ids

    def record_answer(self, node_id, value):
        self.answers[node_id] = value

    def record_signal(self, signal_str):
        if not signal_str:
            return
        parts = signal_str.split(":")
        if len(parts) == 2:
            axis, pole = parts
            if axis in self.signals and pole in self.signals[axis]:
                self.signals[axis][pole] += 1

    def dominant(self, axis):
        scores = self.signals[axis]
        if not scores:
            return "balanced"
        return max(scores, key=scores.get)

    def interpolate(self, text):
        if not text:
            return text
        # Replace {NODE_ID.answer} placeholders
        result = text
        for node_id, answer in self.answers.items():
            result = result.replace(f"{{{node_id}.answer}}", answer)
        # Replace axis dominant/summary placeholders
        for axis_key in ["axis1", "axis2", "axis3"]:
            dom = self.dominant(axis_key)
            result = result.replace(f"{{{axis_key}.dominant}}", dom)
            result = result.replace(f"{{{axis_key}.summary}}", "")  # filled below
        return result

    def build_summary_text(self, template_node):
        interps = template_node.get("interpolations", {})

        a1_dom = self.dominant("axis1")
        a2_dom = self.dominant("axis2")
        a3_dom = self.dominant("axis3")

        a1_label = interps.get(f"axis1.dominant_{a1_dom}", a1_dom)
        a2_label = interps.get(f"axis2.dominant_{a2_dom}", a2_dom)
        a3_label = interps.get(f"axis3.dominant_{a3_dom}", a3_dom)

        a1_summary = interps.get(f"axis1.summary_{a1_dom}", "")
        a2_summary = interps.get(f"axis2.summary_{a2_dom}", "")
        a3_summary = interps.get(f"axis3.summary_{a3_dom}", "")

        combo_key = f"{a1_dom}_{a2_dom}_{a3_dom}"
        closing = interps.get("closing_insights", {}).get(
            combo_key, "Sit with that for a moment."
        )

        text = template_node["text"]
        text = text.replace("{axis1.dominant}", a1_label)
        text = text.replace("{axis2.dominant}", a2_label)
        text = text.replace("{axis3.dominant}", a3_label)
        text = text.replace("{axis1.summary}", a1_summary)
        text = text.replace("{axis2.summary}", a2_summary)
        text = text.replace("{axis3.summary}", a3_summary)
        text = text.replace("{closing_insight}", closing)
        return text


# ─── Tree engine ─────────────────────────────────────────────────────────────

class TreeEngine:
    def __init__(self, tree_path):
        with open(tree_path) as f:
            data = json.load(f)
        self.nodes = {n["id"]: n for n in data["nodes"]}
        self.meta = data.get("meta", {})

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def evaluate_routing(self, routing_rules, state):
        """Evaluate decision node routing rules against current state."""
        for rule in routing_rules:
            cond = rule["condition"]
            # answer_in(['val1','val2']) style
            if cond.startswith("answer_in("):
                values_str = cond[len("answer_in("):-1]
                values = json.loads(values_str.replace("'", '"'))
                last_answer = list(state.answers.values())[-1] if state.answers else None
                if last_answer in values:
                    return rule["next"]
            # axis comparison: axis1.internal >= axis1.external
            elif ">=" in cond or ">" in cond:
                parts = cond.replace(">=", " >= ").replace(">", " > ").split()
                left_val = self._resolve_axis_val(parts[0], state)
                right_val = self._resolve_axis_val(parts[2], state)
                op = parts[1]
                if op == ">=" and left_val >= right_val:
                    return rule["next"]
                elif op == ">" and left_val > right_val:
                    return rule["next"]
        # fallback: return last rule's next
        return routing_rules[-1]["next"] if routing_rules else None

    def _resolve_axis_val(self, expr, state):
        # e.g. "axis1.internal" -> state.signals["axis1"]["internal"]
        parts = expr.split(".")
        if len(parts) == 2:
            axis, pole = parts
            return state.signals.get(axis, {}).get(pole, 0)
        return 0


# ─── Node renderers ──────────────────────────────────────────────────────────

def render_start(node, state, engine):
    header()
    divider()
    slow_print(wrap(node["text"]))
    divider()
    input("  Press Enter to begin...\n")
    return node.get("target")

def render_question(node, state, engine):
    header()
    section_label("Reflection")
    text = state.interpolate(node["text"])
    slow_print(wrap(text))
    print()
    options = node["options"]
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt['label']}")
    print()

    while True:
        try:
            raw = input("  Your answer (enter number): ").strip()
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                chosen = options[idx]
                state.record_answer(node["id"], chosen["value"])
                if chosen.get("signal"):
                    state.record_signal(chosen["signal"])
                return chosen.get("next")
            else:
                print(f"  Please enter a number between 1 and {len(options)}.")
        except (ValueError, KeyboardInterrupt):
            print("  Please enter a valid number.")

def render_decision(node, state, engine):
    routing = node.get("routing", [])
    return engine.evaluate_routing(routing, state)

def render_reflection(node, state, engine):
    header()
    section_label("Reflection")
    text = state.interpolate(node["text"])
    print()
    slow_print(wrap(text))
    print()
    if node.get("signal"):
        state.record_signal(node["signal"])
    options = node.get("options", [])
    if options:
        input(f"  [ {options[0]['label']} — press Enter ]\n")
        return options[0].get("next")
    return node.get("target")

def render_bridge(node, state, engine):
    header()
    section_label("Transition")
    slow_print(wrap(node["text"]))
    print()
    time.sleep(1.5)
    return node.get("target")

def render_summary(node, state, engine):
    header()
    section_label("Today's Reflection")
    text = state.build_summary_text(node)
    print()
    slow_print(wrap(text))
    print()
    options = node.get("options", [])
    if options:
        input(f"  [ {options[0]['label']} — press Enter ]\n")
        return options[0].get("next")
    return None

def render_end(node, state, engine):
    header()
    print()
    slow_print(f"  {node['text']}")
    print()
    time.sleep(1)
    print("  ──────────────────────────────────────────────\n")
    return None


# ─── Main loop ────────────────────────────────────────────────────────────────

RENDERERS = {
    "start": render_start,
    "question": render_question,
    "decision": render_decision,
    "reflection": render_reflection,
    "bridge": render_bridge,
    "summary": render_summary,
    "end": render_end,
}

def run(tree_path):
    engine = TreeEngine(tree_path)
    state = State()

    current_id = "START"

    while current_id:
        node = engine.get_node(current_id)
        if not node:
            print(f"\n[Error: node '{current_id}' not found in tree]")
            break

        state.path.append(current_id)
        node_type = node.get("type", "question")
        renderer = RENDERERS.get(node_type)

        if not renderer:
            print(f"\n[Unknown node type: {node_type}]")
            break

        next_id = renderer(node, state, engine)
        current_id = next_id

    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily Reflection Tree Agent")
    parser.add_argument(
        "--tree",
        default="tree/reflection-tree.json",
        help="Path to the reflection tree JSON file",
    )
    args = parser.parse_args()

    tree_path = Path(args.tree)
    if not tree_path.exists():
        print(f"Error: Tree file not found at '{tree_path}'")
        sys.exit(1)

    try:
        run(tree_path)
    except KeyboardInterrupt:
        print("\n\n  Session ended early. See you tomorrow.\n")
