from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents.research import ResearchTask


def websearch(task: ResearchTask) -> str:
    return f"""
    Convert the following research task into a clear web search topic.

    Task Title:
    {task.title}

    Task Description:
    {task.description}

    Return only a concise and specific search topic.
    """