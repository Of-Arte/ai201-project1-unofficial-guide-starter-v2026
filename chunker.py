"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Split documents into chunks based on markdown sections.

    Strategy for city_guides:
      - Breaks each document along markdown '## ' section headers 
        so topics remain intact and unfragmented.
      - Attaches any introduction text before the first '## ' into
        the first section chunk to avoid short fragments.
      - Prepends the document title ('# <Title>') to each section chunk 
        so chunks in isolation retain standalone context.
      - Emits Chunk objects with produced_by="chunker.py::split_documents".

    Args:
        documents: List of Document objects loaded from the corpus.

    Returns:
        List of Chunk objects.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.text
        lines = text.split("\n")
        doc_title = ""
        for line in lines:
            if line.startswith("# "):
                doc_title = line[2:].strip()
                break

        # Split on markdown section headers '## '
        parts = re.split(r"\n(?=## )", text)
        intro_part = parts[0].strip()
        section_parts = parts[1:]

        # Extract any intro body lines beyond '# Title'
        intro_lines = [
            line.strip()
            for line in intro_part.split("\n")
            if line.strip() and not line.startswith("# ")
        ]
        intro_body = "\n\n".join(intro_lines)

        chunk_index = 0
        if not section_parts:
            # Fallback for documents without '## ' sections
            piece = text.strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=chunk_index,
                        produced_by="chunker.py::split_documents",
                    )
                )
            continue

        for i, sec in enumerate(section_parts):
            sec_clean = sec.strip()
            if not sec_clean:
                continue

            if i == 0 and intro_body:
                # Merge intro overview into the first section chunk
                if doc_title:
                    chunk_text = f"# {doc_title}\n\n{intro_body}\n\n{sec_clean}"
                else:
                    chunk_text = f"{intro_body}\n\n{sec_clean}"
            else:
                if doc_title:
                    chunk_text = f"# {doc_title}\n\n{sec_clean}"
                else:
                    chunk_text = sec_clean

            chunks.append(
                Chunk(
                    text=chunk_text,
                    source=doc.source,
                    index=chunk_index,
                    produced_by="chunker.py::split_documents",
                )
            )
            chunk_index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
