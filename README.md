# The Unofficial Guide

Dearte Hammonds - City Guides

---

# Unit 1

## What This Does

This project uses a vector database to answer questions about the 'city_guides' corpus, which consists of 14 markdown files covering various locations in a fictional region. These guides cover topics such as travel, sight seeing, activities, restaurants, and accommodation.

## Chunking Strategy

**Chunk size:** 400
**Overlap:** 0

The starter chunker's 800 character window often cut directly across markdown section headers which fragmented the content, often merging unrelated subjects or splitting important sentences in half. This was most noticable in the verbosity/length of responses for questions that required more than one section to answer. 

Measuring the section sizes across each file helped me identify that most sections were under the 400 character threshold, with an average of 358 characters. I used this as a baseline and decided to make the chunk size 400. Since each `##` section is an independent topic, using character overlap made little sense for this dataset, as it would reintroduce fragmentation issues. Instead, I attached the `##` title to the front of each chunk to preserve the topic context and ensuring the embedding model and LLM both know which section the chunk came from. I also noticed that the section title provides more relevant context than the source filename alone. 

In the intial prototype, a plain split on the section headers produced 5 violations of Criterion 4 (minimum 150 characters, 2+ complete sentences). This was due to some files not having any text before the first section header, which resulted in tiny title chunks or some chunks with only 1 sentence. I fixed this by updating the chunking logic to merge the intro text into the file's first `##` section chunk. Resulting in 84 chunks with 0 violations of Criterion 4. 

## Sample Chunks

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are

difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## Where to stay

Two inns on the square and a handful of rooms above the pubs. Booking ahead matters between May and September and not at all otherwise. There is no accommodation of any kind within four miles of the town in either direction.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Which bay is built on three levels?

**Answer:**

```
Halden Bay is built on three levels (Source: `guide_halden_bay.md` and `guide_accessibility.md`).

Sources retrieved: guide_accessibility.md, guide_eating.md, guide_halden_bay.md
```

**My relevance cutoff:** 0.65

To determine the cutoff, I evaluated all in scope and out of scope questions, logging the best distance for each.

The in scope questions had a best distance range of .2464 to .5314 with a mean of .3683. The out of scope questions had a best distance range of .8350 to .9968 with a mean of .8836. The gap between these two groups is .3036. For the in scope questions, queries with distinct names matched tightly while broader queries scored higher due to terms appearing in multiple documents.

I set the threshold at .65 to provide a buffer against the chunking strategy I used, which resulted in smaller, more focused chunks that won't always include the context of the entire document. Since each chunk targets a narrow topic, questions phrased indirectly or with only some keywords tend to score higher, so the buffer is used to avoid losing relevant chunks. 

| Question | In corpus? | Best distance |
|---|---|---|
| Which bay is built on three levels? | Yes | 0.3424 |
| In which season do riverside businesses in Brightwater close? | Yes | 0.2464 |
| Which two types of food can be found on Pellew Sands's seafront? | Yes | 0.2626 |
| Which town requires booking ahead in the summer, due to lack of accommodation? | Yes | 0.5314 |
| How long is the canal walk from Northgate to the old lock? | Yes | 0.4585 |
| What is the capital of Mongolia? | No | 0.8463 |
| How do I change the oil in a diesel engine? | No | 0.9032 |
| Who won the 1994 World Cup? | No | 0.9968 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8350 |
| How do I write a for loop in Rust? | No | 0.8365 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
