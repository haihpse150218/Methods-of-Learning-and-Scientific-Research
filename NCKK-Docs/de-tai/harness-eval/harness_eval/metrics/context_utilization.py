"""D2. Context Utilization metrics (M2.1, M2.2).

M2.1 Info Retention Score: BERTScore between full-context and compacted-context responses
M2.2 Effective Token Ratio: % tokens classified as task-relevant
"""

from dataclasses import dataclass


@dataclass
class ContextPair:
    """A pair of responses from the same task under different context strategies."""

    full_context_response: str
    compacted_context_response: str


@dataclass
class TokenSegment:
    """A segment of context with relevance classification."""

    text: str
    is_relevant: bool | None = None  # None = not yet classified
    token_count: int = 0


def info_retention_score(full_response: str, compacted_response: str) -> float:
    """M2.1: BERTScore between full-context and compacted-context responses.

    Measures how much information is retained after context compaction.
    Higher score = compaction preserves more relevant information.

    This is a simplified version using token overlap. For production,
    use bert_score library with the `bert` extra dependency.

    Returns:
        Float in [0, 1].
    """
    if not full_response or not compacted_response:
        return 0.0

    # Simplified: normalized token overlap (Jaccard similarity)
    # Production: replace with BERTScore F1
    full_tokens = set(full_response.lower().split())
    compacted_tokens = set(compacted_response.lower().split())

    if not full_tokens:
        return 0.0

    intersection = full_tokens & compacted_tokens
    union = full_tokens | compacted_tokens
    return len(intersection) / len(union) if union else 0.0


def info_retention_score_bert(full_response: str, compacted_response: str) -> float:
    """M2.1 (production): BERTScore F1 using the bert_score library.

    Requires: pip install harness-eval[bert]

    Returns:
        Float in [0, 1].
    """
    try:
        from bert_score import score as bert_score_fn
    except ImportError:
        raise ImportError(
            "BERTScore requires the 'bert' extra: pip install harness-eval[bert]"
        )

    _, _, f1 = bert_score_fn(
        [compacted_response],
        [full_response],
        lang="en",
        verbose=False,
    )
    return f1.item()


def effective_token_ratio(segments: list[TokenSegment]) -> float:
    """M2.2: % tokens classified as task-relevant.

    Each segment is classified by an LLM classifier (validated on 200 segments
    with human labels, acceptance threshold: accuracy > 90%).

    Returns:
        Float in [0, 1]. Returns 0.0 if no tokens.
    """
    classified = [s for s in segments if s.is_relevant is not None]
    if not classified:
        return 0.0

    total_tokens = sum(s.token_count for s in classified)
    if total_tokens == 0:
        return 0.0

    relevant_tokens = sum(s.token_count for s in classified if s.is_relevant)
    return relevant_tokens / total_tokens
