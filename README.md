# DT-Fellowship-Assignment-The-Daily-Reflection-Tree

# Daily Reflection Tree

A deterministic end-of-day reflection tool. No LLM at runtime. Built for the DT Fellowship assignment.

---

## What's Here

```
/tree/
  reflection-tree.json    ← Part A: the complete tree data (25 nodes)
  tree-diagram.md         ← Part A: Mermaid visual diagram of branching structure
/agent/
  agent.py                ← Part B: Python CLI agent (no dependencies beyond stdlib)
/transcripts/
  persona-1-transcript.md ← Victor / Contributing / Altrocentric path
  persona-2-transcript.md ← Victim / Entitled / Self-centric path
write-up.md               ← Design rationale (Part A)
README.md                 ← This file
```

---

## Reading the Tree (Part A)

Open `tree/reflection-tree.json`. Each node has:

| Field | Meaning |
|-------|---------|
| `id` | Unique node identifier |
| `type` | `start`, `question`, `decision`, `reflection`, `bridge`, `summary`, `end` |
| `text` | What the employee sees. `{NODE_ID.answer}` tokens are interpolated at runtime. |
| `options` | For question/reflection nodes: array of `{label, value, next, signal}` |
| `routing` | For decision nodes: condition → next node mappings |
| `signal` | Axis tally tag, e.g. `axis1:internal` |
| `target` | Hard-coded next node (for start/bridge nodes) |

To trace a path manually: start at `START`, follow `target` or `options[n].next`, evaluate `routing` conditions at decision nodes using accumulated signals.

---

## Running the Agent (Part B)

Python 3.7+ required. No external dependencies.

```bash
# From the repo root:
python3 agent/agent.py

# Or specify a custom tree file:
python3 agent/agent.py --tree path/to/reflection-tree.json
```

The agent:
1. Loads the tree from JSON
2. Renders each node to the terminal
3. Waits for numeric input at question nodes
4. Branches deterministically based on answers and signal tallies
5. Interpolates earlier answers into reflection text
6. Produces a personalised summary at the end

No network calls. No LLM API. Fully offline.

---

## Tree Requirements Check

| Requirement | Minimum | Actual |
|-------------|---------|--------|
| Total nodes | 25+ | 25 |
| Question nodes | 8+ | 10 |
| Decision nodes | 4+ | 4 |
| Reflection nodes | 4+ | 6 |
| Bridge nodes | 2+ | 2 |
| Summary nodes | 1+ | 1 |
| Axes covered | All 3 | All 3 |

---

## The Three Axes

1. **Locus** (Axis 1): Internal vs External locus of control — did the employee see their own agency today?
2. **Orientation** (Axis 2): Contribution vs Entitlement — did the employee focus on what they gave or what they were owed?
3. **Radius** (Axis 3): Altrocentric vs Self-centric — did the employee's attention extend to others or stay close to home?

Each axis has 2–3 questions. Signals accumulate. The majority pole determines which reflection the employee receives. All 8 combinations produce a unique closing insight in the summary.
