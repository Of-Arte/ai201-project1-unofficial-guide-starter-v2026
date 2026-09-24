"""
Checks criterion 4 directly against the chunks: no chunk shorter than 150
characters, and every chunk contains at least two complete sentences.

    python tools/check_criterion4.py
    python tools/check_criterion4.py --corpus city_guides
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from ingest import load_documents
from chunker import split_documents


def sentence_count(text: str) -> int:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return len([s for s in sentences if s.strip()])


def main():
    parser = argparse.ArgumentParser(description="Check criterion 4 against real chunks.")
    parser.add_argument("--corpus", default=None)
    args = parser.parse_args()

    corpus = args.corpus or config.CORPUS
    docs = load_documents(corpus=corpus)
    chunks = split_documents(docs)

    too_short = [(c.label, len(c.text)) for c in chunks if len(c.text) < 150]
    too_few_sentences = [
        (c.label, sentence_count(c.text), len(c.text))
        for c in chunks
        if sentence_count(c.text) < 2
    ]

    print(f"Total chunks: {len(chunks)}")

    print(f"\nChunks shorter than 150 chars: {len(too_short)}")
    for label, length in too_short:
        print(f"  {label}: {length} chars")

    print(f"\nChunks with fewer than 2 sentences: {len(too_few_sentences)}")
    for label, sc, length in too_few_sentences:
        print(f"  {label}: {sc} sentence(s), {length} chars")


if __name__ == "__main__":
    main()
