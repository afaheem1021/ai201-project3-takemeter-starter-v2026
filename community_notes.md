# Milestone 1 — community and what I saw

## The community

**Hacker News comment threads** (news.ycombinator.com). Public, no login needed
to read, and every thread is open through the official Algolia HN API
(`hn.algolia.com/api/v1/items/<id>`), so the collection is reproducible.

I first tried r/nba, but Reddit now blocks unauthenticated reads of its JSON
endpoints. HN turned out to be a better fit anyway: the topics are varied
(cars, AI models, security, immigration policy, dentistry, home hardware) so
no single show or release dominates, and the quality of comments varies a lot
inside the same thread.

Threads I read from (all front-page, Oct 2026): Tesla Roadster, Mistral Large
4, Things to know when you get cancer, Cloudflare acquires Deno, Passkeys are
a trap, Do dentists know what they're doing?, How Amazon pushes up prices,
the H-1B / Microsoft green card story, supermarket fridge hack, the LLM
capability gap essay, "AI is a tool", Utah's VPN law, Rust borrow checker
bugs, Apple HomeView, "Everybody's home", the Ledger spy chip story.

## What I read

40 random comments, 60–600 characters, from those threads.

## Candidate distinctions I could point at

1. **Some comments point at something outside themselves you could check.**
   A link to docs, a block quote from the article ("Bad news, sorry, the
   article says: …"), a PEP number, a figure. Most don't.
2. **Some comments lean on what the writer personally did or saw.** "I've
   helped do it for industrial equipment (win95 controller…)", "Was just in
   Europe and saw plenty of smaller / cheaper EVs." The support is real but
   you have to trust the person.
3. **A lot of comments are a flat confident claim or a joke.** "All Musk
   cares about is Mars." "closed tab. thanks." "TOTP is just as phishable as
   a password." No support offered at all — sometimes right, never argued.
4. (Didn't keep) **Some comments are just questions** ("What's /side? Is that
   a Codex thing?"). They're real but rare in what I read (~2 of 40) and none
   of the other distinctions describe them.

The first three all answer the same question — *what is this comment's claim
resting on?* — which is what made me want to build labels around them instead
of around tone or "quality".
