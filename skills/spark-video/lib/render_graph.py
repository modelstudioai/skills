"""
render_graph.py — compute parallel chain groups from a storyboard.

A new group starts at every shot with use_prev_last_frame_as_first=False
(and at the very first shot regardless of its flag). Groups can be
rendered in parallel; shots inside a group must run sequentially.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.storyboard import Shot, Storyboard


def compute_chain_groups(storyboard: "Storyboard") -> list[list[str]]:
    """Return list of chain groups, each as a list of shot IDs in order."""
    return _slice([s for s in storyboard.shots])


def _slice(shots: list["Shot"]) -> list[list[str]]:
    groups: list[list[str]] = []
    current: list[str] | None = None
    for i, s in enumerate(shots):
        starts_new = (i == 0) or (not s.use_prev_last_frame_as_first)
        if starts_new or current is None:
            current = []
            groups.append(current)
        current.append(s.id)
    return groups


def parallelism_stats(storyboard: "Storyboard") -> dict:
    """Quick metrics: count, max group size, distribution."""
    groups = compute_chain_groups(storyboard)
    sizes = [len(g) for g in groups]
    return {
        "groups": len(groups),
        "max_group_size": max(sizes) if sizes else 0,
        "min_group_size": min(sizes) if sizes else 0,
        "avg_group_size": round(sum(sizes) / len(sizes), 2) if sizes else 0,
        "total_shots": sum(sizes),
    }
