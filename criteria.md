# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.65 on the held-out test split, on every seed

Measured on the 15% test split the notebook holds out, for each of seeds 42, 7
and 2024. All three have to clear 0.65.

**Why this target:** Three labels means random guessing gets about 0.33, but
the real floor is higher than that: I expect `opinion` to be the biggest label
at roughly 45% of my file, so a model that only ever says `opinion` already
gets about 0.45. I want the model at least 20 points above that do-nothing
guesser before I'd call it useful for sorting a thread. I didn't go higher
because my test split will only be ~32 comments, so one or two posts swing it
by 3–6 points per seed.

---

## 2. `experience` has an F1 of at least 0.50 on every seed

**Why this target:** `experience` vs `opinion` is my hardest boundary — it
depends on the "specific thing that happened" rule, and a lot of HN opinions
borrow the vocabulary of experience ("in my experience", "every team I've
been on"). I expect this to be the model's weakest label, and with only ~9 of
them in each test split its F1 will be jumpy. 0.50 means it's catching about
half of real first-hand accounts without flooding the label with opinions; I
set it lower than criterion 3 on purpose because the surface words overlap so
much.

---

## 3. `evidence` has an F1 of at least 0.70 on every seed

**Why this target:** `evidence` should be my easiest label, because most of it
carries visible markers — a URL, a block quote from the article, a figure with
a source. If a fine-tuned model can't get to 0.70 on the label with the most
surface signal, it isn't learning my taxonomy. I'm holding it to a higher bar
than `experience` for that reason. (The risk I'm aware of: the model might
learn "has a link" instead of "rests on something checkable" — this criterion
can't tell those apart, and that's something to look at in the confusion
matrix next unit.)

---

## 4. No label is more than 50% of labels.csv, and every label has at least 50 rows

**Why this target:** The brief's cap is 70%, but on HN `opinion` is naturally
around 60–70% of comments, so if I only sampled randomly I'd sit right at the
cap and the model would learn to guess `opinion`. I'm setting a stricter 50%
cap so the majority-class guesser stays near 0.45 (which is what criterion 1
is measured against). The 50-row floor is so each label gets about 7–8
examples in the test split — the notebook flags fewer than 8 as too thin to
measure, and I'd rather fix that in the data than explain it later.

---

## 5. The most-confident third of predictions is at least 0.15 more accurate than the least-confident third, on every seed

Uses `accuracy_most_confident_third` minus `accuracy_least_confident_third`
from `results.json`.

**Why this target:** The point of TakeMeter would be to surface
evidence-backed comments in a long thread, and that only works if I can trust
a confident `evidence` call more than a hesitant one. If confident and unsure
predictions are right at about the same rate, the confidence score is
decoration. 0.15 on thirds of ~32 posts (about 10 posts each) means roughly
1–2 more correct posts in the confident group — a small but real gap. I
didn't ask for more because with 10 posts per third, one post moves it 0.10.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
