# How the posts were collected

Timeboxed helper scripts, kept for reproducibility. Not part of training.

1. `python fetch_hn.py <story ids...>` pulls every comment in those threads from
   the public Algolia HN API (`hn.algolia.com/api/v1/items/<id>`), strips the
   HTML, and writes `comments.json`. I used 16 front-page threads from
   October 2026 (ids listed in `community_notes.md`'s thread list):
   `50112657 49977979 50093568 50019911 50048312 50050553 50084757 50006832
   50055304 50047422 50063427 49927754 50069499 50071017 49891295 50054092`
2. `python build_pool.py` keeps comments of 40–900 characters, drops exact
   duplicates, and builds a 280-comment candidate pool: 140 random, 70 that
   match evidence-ish keywords (links, "according to", percentages, years) and
   70 that match experience-ish keywords ("I worked", "in my experience", "my
   wife", …).
3. A second pass of 70 more evidence-keyword candidates (links, percentages,
   dollar figures, with at least 60 characters of prose besides the link) was
   added when `evidence` came out thinnest.

Keywords only decided which comments got *looked at*. Every label was assigned
by reading the comment against the rules in the README — about 40% of the
keyword-sampled comments ended up as a different label than the keyword hinted.
