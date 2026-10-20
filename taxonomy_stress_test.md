# Taxonomy stress test (Milestone 2)

I gave an AI model my three draft definitions and asked it for eight short
comments that sit on the boundaries. Then I tried to label each one using only
the definitions.

| # | Generated post | First try | Clean? | Final |
|---|---|---|---|---|
| 1 | "In my experience Postgres handles this fine up to a few billion rows." | experience? | **No** | `opinion` |
| 2 | "We moved our 40-node cluster from Postgres to Cockroach last year and p99 writes went from 12ms to 30ms." | experience / evidence? | **No** | `experience` |
| 3 | "Cockroach's own docs say every write needs a consensus round trip: https://www.cockroachlabs.com/docs/stable/architecture/replication-layer" | evidence | Yes | `evidence` |
| 4 | "Studies show remote workers are more productive. Everyone knows this." | evidence? | **No** | `opinion` |
| 5 | "My dentist tried to sell me a $3,000 deep cleaning; the second dentist I saw said I didn't need it." | experience | Yes | `experience` |
| 6 | "The ADA's guidance (I looked it up when my dentist pushed a deep clean on me) says scaling is only indicated at 4mm+ pockets." | either | **No** | `evidence` |
| 7 | "As someone who's been a dev for 20 years: this is a fad." | experience? | **No** | `opinion` |
| 8 | "lol imagine paying $100k for a car that can't drive itself in the rain" | opinion | Yes | `opinion` |

**Five of eight weren't clean on the first pass**, which told me the draft
definitions weren't finished. What I tightened before labeling anything real:

- **#1 and #7 → the main decision rule.** "In my experience" and "20 years as
  a dev" are credentials, not accounts. `experience` now requires a specific
  thing that happened. This is the `experience` / `opinion` boundary and it
  became the hardest-boundary rule in the README.
- **#2 → personal numbers stay `experience`.** A number only makes something
  `evidence` if a reader could look it up. Your own p99 can't be.
- **#6 → `evidence` beats `experience`** when the checkable item is what
  carries the point.
- **#4 → vague appeals are `opinion`.** "Studies show" with nothing named
  gives the reader nothing to check.

After those four changes, I re-labeled all eight from the written rules alone
and each one had exactly one answer.
