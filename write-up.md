# Write-Up: The Daily Reflection Tree

## Why These Questions?

The goal was to write questions that feel like a conversation with a thoughtful colleague — not a performance review, not a therapy session, not a motivational poster.

Each question was designed around one principle: **make the insight latent in the options themselves**. A person who picks "I waited for someone else to fix it" doesn't need to be told they leaned external. They already know, the moment they read the words. The tree's job is to surface the awareness, not deliver a verdict.

### Axis 1 — Locus (Victim vs Victor)

The opening "one word" question was inspired by Rotter's (1954) insight that locus of control is often revealed in *narrative framing*, not in direct self-report. By asking for a single word first, the tree captures the employee's initial emotional frame before any reflection occurs — then tailors the first real question to match it. Someone who said "Productive" is asked about what made things go well; someone who said "Frustrated" is asked about their instinct when things got hard.

The second question ("Think about a moment when something didn't go as planned") is designed to isolate a *specific behavioral response*, not a general self-image. People often believe they have an internal locus until they're asked what they actually did when the plan failed. The options are behaviorally concrete for this reason.

**Trade-off:** The two-branch system (HIGH/LOW) is a simplification. In reality, locus exists on a spectrum and varies by domain. A more sophisticated tree would have 3–4 forks. For this version, legibility and flow were prioritized.

### Axis 2 — Orientation (Contribution vs Entitlement)

Psychological entitlement (Campbell et al., 2004) is notoriously invisible to the person holding it. People don't think "I feel entitled" — they think "I deserve what I earned" or "others aren't pulling their weight." So the questions were written to *describe behaviors and thoughts*, not ask for self-labels.

The key question ("At the end of today, which thought crossed your mind more?") is designed around Organ's (1988) OCB framework — the distinction between in-role performance and discretionary effort. The options in pairs: one from each pole, worded to be equally plausible. No option should feel obviously "wrong."

The final Axis 2 question ("Was there a moment today where you went beyond what was asked?") adds a nuanced option: "Yes — but I noticed I was hoping someone would see it." This captures a real psychological state — prosocial behavior motivated by visibility — that neither pure contribution nor pure entitlement covers.

**Trade-off:** Entitlement is a sensitive axis. The reflections were written to be observational, not shaming. "It's easy — and human — to keep score" is deliberate: it normalizes the tendency before reframing it.

### Axis 3 — Radius (Self-Centrism vs Altrocentrism)

Maslow's 1969 self-transcendence paper argues that the deepest wellspring of meaning comes from orienting toward something larger than yourself. The questions here are designed to surface *where the employee's attention naturally went* during the day — not where they think it should have gone.

The options in the opening question are ordered from narrow (just me) to wide (the end user), mirroring Batson's (2011) perspective-taking research: the ability to imagine another's experience, not just sympathize, is a learnable and scalable skill.

**Trade-off:** The axis 3 questions are the most speculative — measuring "radius of concern" in a five-minute reflection is difficult. A better version might ask about a specific moment of noticing someone else's experience. This is listed as a future improvement.

## Branching Design

The tree uses **accumulated signal tallies** rather than single-question branching. Each question on an axis adds a signal (e.g., `axis1:internal` or `axis1:external`), and the decision node at the end of each axis routes based on the *majority* signal. This means a single "off" answer doesn't derail the entire path — the person's dominant orientation across 2–3 questions determines which reflection they receive.

This was a deliberate choice to reduce sensitivity to ambiguous individual questions and to more faithfully represent the psychological axes, which are *tendencies*, not binary states.

The bridge nodes between axes are load-bearing: they don't just transition — they *reframe* what's coming. "From how you navigated, to what you put in" is not a neutral segue; it primes the employee to think about effort and giving before the Axis 2 questions arrive.

## What I'd Improve With More Time

1. **More branching depth per axis.** The current tree has 2 branches per axis. A richer tree would branch by *combination* — an internal/entitlement/self person is a different psychological profile from an external/contribution/altrocentric one, and deserves a different conversation, not just different reflections at the end.

2. **Axis 3 question quality.** The radius questions feel slightly less grounded than the Locus and Orientation questions. I'd run user testing with 3–4 personas and rewrite based on which options people found hard to distinguish.

3. **Summary interpolation.** The current summary template is functional but formulaic. Ideally, the closing insight would reference a *specific answer* from earlier in the session ("You said you 'adapted quickly' — and you also thought about your team. That's not coincidence.").

4. **Temporal anchoring.** One of the underused techniques in reflection design is *specific time reference* ("Think about 3pm today..."). A future version would use this more aggressively to reduce abstract, idealized answers.

5. **Persona testing.** The assignment hint recommends using LLMs to roleplay employee personas. I tested the tree against three simulated personas (a stressed junior analyst, a burned-out senior, and a high-performer with ego risk) and found that the Axis 2 entitlement branch needed rewriting twice to avoid feeling accusatory.

## Sources

- Rotter, J.B. (1954). *Social Learning and Clinical Psychology.* Prentice-Hall.
- Dweck, C. (2006). *Mindset: The New Psychology of Success.* Random House.
- Campbell, W.K. et al. (2004). Psychological Entitlement. *Journal of Personality and Social Psychology.*
- Organ, D.W. (1988). *Organizational Citizenship Behavior.* Lexington Books.
- Maslow, A.H. (1969). Various meanings of transcendence. *Journal of Transpersonal Psychology.*
- Batson, C.D. (2011). *Altruism in Humans.* Oxford University Press.
