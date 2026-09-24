# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. _"Retrieval works"_ is an opinion. _"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"_ is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; _"80% seemed reasonable"_ does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

4 questions mention specific towns that appear in one or two files, while the booking question uses terms that appear in nearly every town guide.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

LLMs hallucinate if chunks don't contain anything relevant, so we want to make sure each answer has a source to refer to.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**

Our out of scope questions share almost no overlap with our scoped questions. A target of 4 out of 5 leaves room for edge cases where general words might lower the distance score for an out of scope question.

There was a clean 0.3036 gap between the highest in-scope distance (0.5314) and the lowest out-of-scope distance (0.8350), with zero overlap between the two groups.

---

## 4. Each chunk has more than 150 characters with at least two complete sentences

No chunk is shorter than 150 characters, and every chunk contains at least two complete sentences.

**Why this target:** Markdown headings can produce tiny chunks or incomplete sentences, and our questions require the retrieval of full sentences.

---

## 5. Primary file cited matches the file where the answer is found

For at least 4 of my 5 test questions, the primary file cited in the answer is the same file where the answer is found.

**Why this target:** Our questions require specific details from individual files, and we want to ensure that the system is able to retrieve the relevant file containing the correct answer.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
