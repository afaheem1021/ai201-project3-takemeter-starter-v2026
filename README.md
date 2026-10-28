# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts **Hacker News comments** by *what the comment's point rests
on*. `evidence` comments point at something you can check yourself: a link, a
quote from the article, a public figure. `experience` comments rest on
something the writer actually did or saw. `opinion` comments rest on the
writer's say-so. It's not a quality score, since plenty of great HN comments
are well-reasoned opinions. The use I have in mind is long threads: being able
to pull out the comments that cite something, or the ones from people who've
actually done the thing, without reading 1,000 replies.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

All three labels answer one question: **what is this comment's main claim
resting on?** Not whether it's right, not whether it's polite — just what kind
of support it offers.

### `evidence`

**Definition:** The comment's point rests on something outside the comment
that a reader could check without trusting the writer — a link, a quote from
the article or docs, or a specific figure, date, law or spec tied to a public
source.

**Example 1:**
> \> I'm happy if this means Deno is able to get a second impulse
>
> Bad news, sorry, the article says:
>
> \> We will support the Deno runtime for another year with monthly releases
> containing bug fixes and security updates. After that year we will end our
> development of the Deno runtime.
>
> Sounds like Celld will live on within workerd, Deno is over.

**Example 2:**
> if you're not locked to javascript you could use python with pep-723[1] to
> declare inline dependencies
>
> 1: https://peps.python.org/pep-0723/

### `experience`

**Definition:** The comment's point rests on a concrete first-hand account —
something the writer (or their workplace or household) actually did, saw, or
had happen to them, specific enough that you could picture it.

**Example 1:**
> Yeah I'm absolutely the market for this thing. We have an old Google Home
> that we use as a digital photo frame and Google has progressively destroyed
> every other piece of functionality we once used on it.
>
> My only complaint is that a truly environmentally friendly company (like
> Apple claims to be!) would make this OS available for old iPads. […]

**Example 2:**
> Maintaining old hardware to 2026 security requirements is damn near
> impossible, and what constitutes "old" is very variable; HOWEVER putting
> them behind a dedicated VLAN+firewall+VPN is not that hard.
>
> I've helped do it for industrial equipment (win95 controller or something)
> that couldn't be upgraded without spending millions, but it sill required
> pulling out the old 10base2 network and installing cat 6 cables in a factory
> floor and new switches.

### `opinion`

**Definition:** The comment asserts a claim, judgment, prediction or joke and
offers no support beyond the writer's own say-so or reasoning — nothing to
check and no first-hand account.

**Example 1:**
> All Musk cares about is Mars. The CT is going to be a Mars vehicle, that's
> why it looks like that by and large.
>
> And this tech is simply part of the Tesla/SpaceX merge, and right in line
> with flamethrowers, tunnels, and chainsaws. It's going to funnel loads of
> cash his way, which was the idea.

**Example 2:**
> TOTP is just as phishable as a password and offering it today is as much
> security malpractice as SMS.
>
> For all their faults, passkeys/webauthn is the future and you can absolutely
> just use nitrokeys you control, with backups, as you like.

### The hardest boundary

**Which two labels:** `experience` vs `opinion`.

HN is full of comments that *wave at* experience without giving one: "In my
experience…", "As someone who's done this for 20 years…", "Every team I've
been on…". The borderline post I found while reading:

> Even projects that you could have done without having to look anything up?
>
> In my experience, it seems to mostly save time on things you don't really
> know that well, whilst depriving you of the chance to learn new things.

**The decision rule I used every time:**

**It's `experience` only if the comment describes a specific thing that
happened** — a job, a setup, a place, an event, something you could picture.
The phrase "in my experience", a job title, or years of seniority on their own
are not an account; they're a credential attached to a claim, and the comment
is `opinion`. The post above is `opinion`.

**Two smaller rules that came out of the stress test:**

- **`evidence` beats `experience`.** If a comment has both an anecdote and a
  checkable item, and the checkable item is what carries the point, it's
  `evidence`. Personal numbers ("our p99 went from 12ms to 30ms") are still
  `experience` — you can't check them, you have to trust the writer.
- **Quoting the comment you're replying to isn't evidence.** HN replies often
  open with `> parent's words`. Only a quote from the article, docs, or another
  outside source counts. Vague appeals ("studies show", "everyone knows") are
  `opinion`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** 16 front-page Hacker News threads from
October 2026, pulled through the public Algolia HN API (no login, no key).
The topics are deliberately mixed: the Tesla Roadster, Mistral Large 4,
cancer advice, Cloudflare buying Deno, passkeys, dentists, Amazon pricing,
H-1B policy, a supermarket-fridge hack, LLM capability, Utah's VPN law, a
Rust compiler bug, Apple HomeView, hosting dinner parties, and a hardware-wallet
breach. I kept whole comments of 40–900 characters and dropped exact
duplicates. Scripts and the thread IDs are in [`collect/`](collect/README.md).

I first tried r/nba, but Reddit blocks unauthenticated reads now. HN turned
out to suit this taxonomy better anyway, because citing sources and "I worked
at X" are both normal moves there.

**How I labelled them:** Every row was **pre-labelled by AI** (Claude Code)
applying the written rules in the Label Taxonomy section, and the note column
says so on every row. Full disclosure is in How I Used AI below. Rows that
needed a judgement call carry a note in the `note` column saying which rule
decided them (72 of 307 rows).

- **Sampling.** I built a 280-comment pool: 140 random, 70 matching
  evidence-ish keywords (links, "according to", percentages) and 70 matching
  experience-ish keywords ("I worked", "my wife", "in my experience"). Keywords
  only chose what got *read*. About half of the keyword-sampled comments (104
  of 200) ended up with a different label than the keyword suggested.
- **What I skipped (15):** pure questions with no claim ("Break into your
  comma? Google-fu is letting me down"), bare links, and thank-yous. None of
  my three labels describe them. They were about 5% of what I read.
- **Balance fix.** After the first 280, `evidence` was thinnest (48), so I
  pulled 70 more evidence-keyword candidates and labelled those (29 came out
  `evidence`). That gave 335 usable rows with `opinion` at 53%, over my own
  50% cap in criterion 4. So I randomly held back 28 `opinion` rows that had
  no hard-case note. They're in `data/held_back_opinion.csv`, not in
  `labels.csv`, in case unit 6 needs them.
- **Finding:** in the purely random slice, **99 of 121 usable comments (82%)
  were `opinion`**. HN left alone is way over the brief's 70% cap. Without
  targeted sampling this dataset would train a model that just says `opinion`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `evidence` | 77 | 25.1% |
| `experience` | 80 | 26.1% |
| `opinion` | 150 | 48.9% |
| **Total** | 307 | 100% |

**Three hard cases**

**1. "In my experience" with and without an account** (`experience` vs
`opinion`, my hardest boundary)
> *The post:* "Buying a car is the easy part. In my experience, new cars have
> new car problems, but old cars have old car problems. There's no clear
> winner in every metric, just trade offs."
>
> …compared with: "In my experience, the customer-friendly return experience
> is withering. I ordered a small table about a year ago that didn't ship with
> the correct hardware. […] I had to call to get a refund […] The customer
> service representative was pretty reluctant to accept it […]"
>
> *Could have been:* both start with the exact same phrase, so either both
> `experience` or both `opinion`.
>
> *I chose:* `opinion` for the car one and `experience` for the table one.
> The decision rule says the phrase doesn't count, only a specific event does.
> The table comment has a specific event (wrong hardware, a refund call, a
> reluctant rep); the car comment is a generalisation. This pair is the reason
> I wrote the rule. It's also exactly the kind of pair a model could get wrong
> by keying on the words "in my experience".

**2. A memory of watching TV that's really a citation** (`experience` vs
`evidence`)
> *The post:* "I remember seeing a TV program[1] where the UK govt had proposed
> some hare-brained key escrow thing (this is circa 2000 ish) […] The expert
> they had on to explain the drawbacks of the scheme was Whitfield Diffie[2]
> […] Diffie explained that there is essentially no security measure that is
> effective if you create a prize of infinite value. […] [1] "Newsnight" on BBC
> [2] As in Diffie-Hellman etc https://en.wikipedia.org/wiki/Whitfield_Diffie"
>
> *Could have been:* `experience`, since it's framed as "I remember seeing",
> a first-hand memory.
>
> *I chose:* `evidence`. The point rests on what a named public figure said on
> a named programme, which you could look up without trusting the writer. The
> writer's memory is just how they found it. That's the "`evidence` beats
> `experience`" rule.

**3. A link that isn't support** (`evidence` vs `opinion`)
> *The post:* "Maybe embedding things about a derivative AI's company will be
> the Reflections on Trusting Trust[0] vulnerability of the 21st century.
> [0] https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/Sec/Reflections-on-Trusting-Trust.pdf"
>
> *Could have been:* `evidence`, because it has a link to a real paper.
>
> *I chose:* `opinion`. The link only defines a term. The claim itself
> ("maybe this will be…") is speculation that the paper can't back up, since
> the paper is from 1984. I applied this the same way to joke links, links to
> Wikipedia definitions, and "you'd like this chapter" recommendations.
> **It's the case I expect the model to get wrong most.** 45 of 77 `evidence`
> rows contain a URL, but so do 17 `opinion` rows and 5 `experience` rows.
> "Has a link" is an easy shortcut for a model to learn instead of "rests on
> something checkable".

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased` (the notebook default).

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. 70/15/15 stratified split done by the notebook. I never split
`labels.csv` myself.

**Device:** **`cpu`** (torch 2.14.1+cpu, Windows 11, Python 3.12.10), and
`results.json` records the same. I ran sections 1–5 in this repo's `.venv`
kernel. Sections 6–7 are unit 6 and weren't run.

**Anything I changed from the defaults, and why:** No hyperparameters. The
only edits to the notebook were `LABELS = ["evidence", "experience",
"opinion"]` and my name/email. With 307 rows I didn't have a reason to touch
the settings before seeing a single result, and changing them blind would
just be guessing.

One related check on `MAX_LENGTH`: I counted tokens with the DistilBERT
tokenizer. **65 of 307 comments (21%) are longer than 128 tokens** and get
cut off; the longest is 228. It isn't spread evenly: 36% of `experience`
rows, 23% of `evidence` rows and 12% of `opinion` rows get truncated. That
makes sense, since stories run long and `evidence` often puts its link or
footnote at the very end (`[0] https://…`). So the labels that depend most on
the end of the comment are the ones losing it. I kept the default rather than
change it before seeing results, and I'm noting it here as a likely suspect
for unit 6.

**Split sizes:** train 214 · val 46 · test 47

| Label | train | val | test |
|---|---|---|---|
| `evidence` | 53 | 12 | 12 |
| `experience` | 56 | 12 | 12 |
| `opinion` | 105 | 22 | 23 |

Every label has at least 12 in the test split, above the notebook's 8-example
warning. That's what the 50-row floor in criterion 4 was for. 12 is still
small, though: one post moves a label's recall by about 8 points, so expect
per-label F1 to move between seeds next unit.

`results.json` and `test_split.csv` are committed. Per the brief, I haven't
compared the numbers to my criteria yet. That's unit 6.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

I did this unit with **Claude Code** (Anthropic's coding agent) working in
this repo. It wrote the collection scripts, set up the Python 3.12 venv (my
machine only had 3.14, which the pins don't support), did the labelling pass,
ran the notebook, and drafted this write-up from my direction. Two moments
that changed the project:

**Moment 1: stress-testing the taxonomy**

- *What I asked for:* eight short comments sitting on the boundaries between
  my three draft definitions, which I then tried to label using only the
  definitions.
- *What came back:* five of the eight weren't clean. "In my experience
  Postgres handles this fine up to a few billion rows" and "As someone who's
  been a dev for 20 years: this is a fad" both read as `experience` under the
  draft wording. A post mixing an anecdote with a cited ADA guideline could
  have been either. Full table in [`taxonomy_stress_test.md`](taxonomy_stress_test.md).
- *What I changed:* four rules before labelling anything real. The main one
  is the hardest-boundary rule: `experience` needs a specific event, and
  credentials and "in my experience" don't count. The others: personal
  numbers stay `experience`, `evidence` beats `experience`, and vague appeals
  ("studies show") are `opinion`.

**Moment 2: the first label count**

- *What I asked for:* label the 280-comment pool against the written rules,
  put a note on every judgement call, then count.
- *What came back:* 151 `opinion` / 68 `experience` / 48 `evidence`. That was
  under my own 50-row floor for `evidence` and over my 50% `opinion` cap.
  Broken down by sampling source, the purely random comments were 82%
  `opinion`.
- *What I changed:* instead of loosening the `evidence` definition to get
  more of it, I sampled 70 more evidence-keyword candidates and labelled them
  under the same rules, then held back 28 random `opinion` rows. I kept the
  stricter definition because a looser `evidence` label would have meant
  "has a number in it", and that isn't what I want the model to learn.

**Pre-labelling disclosure:** **All 307 rows in `labels.csv` were labelled by
Claude Code**, applying the rules in this README. Every row's note starts with
`pre-labelled (AI)`, and 72 rows also have a note naming the rule that decided
a hard call. The criteria in `criteria.md` were also drafted with Claude Code,
before any labelling or training. The commit history shows they were filed
first.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Baseline is `facebook/bart-large-mnli` zero-shot, run on my machine (CPU).
Trained is my unit 5 DistilBERT run (seed 42, CPU). Both are scored on the
same 47 posts in `test_split.csv`, so it's like-for-like. The main baseline
uses my definitions from `label_definitions.txt` (`baseline_results.json`).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.383 | 0.660 | +0.277 |
| Macro F1 | 0.363 | 0.573 | +0.210 |
| F1 — `evidence` | 0.457 | 0.700 | +0.243 |
| F1 — `experience` | 0.471 | 0.286 | -0.185 |
| F1 — `opinion` | 0.160 | 0.733 | +0.573 |

**Definitions vs. bare label names.** I also ran it once with no definitions
file, so it only got the words `evidence` / `experience` / `opinion`
(`baseline_results_bare_names.json`). I expected that to be worse. It wasn't:

| Measure | Baseline, my definitions | Baseline, bare names | Trained (seed 42) |
|---|---|---|---|
| Overall accuracy | 0.383 | **0.596** | 0.660 |
| Macro F1 | 0.363 | **0.591** | 0.573 |
| F1 — `evidence` | 0.457 | 0.571 | 0.700 |
| F1 — `experience` | 0.471 | 0.571 | 0.286 |
| F1 — `opinion` | 0.160 | 0.632 | 0.733 |

So my definitions were worth **minus 21 points** to the zero-shot model. Looking
at the predictions, the definitions version called only 2 of 23 opinions
`opinion`. It put 11 in `evidence` and 10 in `experience`. My `opinion`
definition is basically a list of negatives ("offers no support… nothing to
check and no first-hand account"), and an entailment model reading "This post
is the comment asserts a claim… and offers no support…" doesn't really do
"no". The other two definitions describe things that *are* there, so they win
by default. These definitions were written for a person, and a person reads
"no support" fine. They just turned out to be a bad prompt. The table above
still uses the definitions run, because that's the baseline the assignment
asks for, but the bare-names run is the stronger opponent and I'm keeping it
in mind below.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

(Written before running the baseline. To be honest, the notebook printed my
trained accuracy at the end of unit 5, so I knew that one number, roughly
0.66. I hadn't seen anything from the baseline.)

My guess: the trained model wins on overall accuracy and on `opinion`,
because it's seen 105 HN opinions and has learned that "just say opinion" is a
safe bet here, while BART is reading three long definitions cold and will
spread its guesses around. I think it'll also win on `evidence`, since links
and `> quotes` are easy surface stuff to learn. Where I think the baseline
might actually be close, or even win, is `experience`. An NLI model can kind
of read "the writer actually did or saw something", and I remember my trained
model didn't catch many of those.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

My prediction was mostly right, and the part I flagged came true: training
beat the baseline on accuracy, `opinion` and `evidence`, and *lost* on
`experience` by 0.185 F1. But the +0.277 accuracy gap flatters it. Most of
that gap is the baseline having a broken `opinion` prompt. Against the
bare-names baseline, fine-tuning is only +0.064 on accuracy and actually
slightly *behind* on macro F1 (0.573 vs 0.591). Basically, what my fine-tuning
added on seed 42 was "lean hard on `opinion`, which is half the data." That
pays off on accuracy and costs you `experience`. A general model that's never
seen an HN comment found 10 of the 12 `experience` posts. Mine found 2.

The baseline is also slow: a few seconds a post, so a couple of minutes for
47, while the trained model gets through 46 validation posts in about 2 seconds
(the notebook's `eval_runtime`). If I were
running this over a 1,000-comment thread, that would matter.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
