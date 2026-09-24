"""
Scorer module for AI201 Project 1
"""

def judge(question: str, expects: str, answer: str, results: list) -> bool:
    """
    Return True if the answer matches expectations, False otherwise.
    """
    return expects.strip().lower() in answer.strip().lower()