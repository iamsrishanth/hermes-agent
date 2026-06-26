"""
Shared handler for /dream and /distill slash commands.

"/dream" scans recent session traces, extracts persistent knowledge into
project memory, and removes outdated entries.

"/distill" discovers repeated manual workflows in recent work and packages
high-confidence candidates into reusable skills, subagents, or commands.

Both commands work by seeding the agent's next turn with a detailed prompt
that leverages the agent's own tools (session_search, memory, skill_manage).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DreamDistillResult:
    """Result from a dream or distill command handler."""
    text: str               # User-facing message to display
    agent_seed: str | None  # If set, seeded as next agent turn


# ---------------------------------------------------------------------------
# /dream
# ---------------------------------------------------------------------------

DREAM_PROMPT = """You are performing a /dream operation — scanning recent session 
traces to extract persistent knowledge and update project memory.

**Goal:** Find durable facts, decisions, preferences, conventions, and 
lessons learned from recent work. Save them to memory. Remove any outdated 
or contradicted entries.

**Step 1: Scan recent sessions for knowledge.**
Use session_search() with different queries to discover what we've worked on:
- Search for "decision", "preference", "convention", "agreed", "remember", 
  "don't forget", "lesson learned", "configured", "set up", "pattern"
- Search for project names we've worked on recently
- Search for error fixes and workarounds discovered

**Step 2: For each session found, scroll into the context window around matches.**
Use session_search(session_id=..., around_message_id=...) to get the full 
context of important moments.

**Step 3: Extract durable knowledge.**
From the session traces, identify facts that will still matter in a week:
- User preferences and corrections (things Srishanth told us to do/not do)
- Environment details (paths, tools, configurations)
- Project conventions (naming, structure, deployment patterns)
- API quirks, tool-specific workarounds
- Architectural decisions and their rationale
- Recurring pitfalls and their solutions

**Step 4: Update memory.**
For each piece of knowledge:
- Use memory(action='add', target='memory', content='...') to save new facts
- Use memory(action='replace', target='memory', old_text='...', content='...') 
  to update existing facts that are stale
- Use memory(action='remove', target='memory', old_text='...') to remove 
  facts that are no longer true

**Step 5: Report.**
Summarize what you found, what you saved, what you updated, and what you removed.
"""


def handle_dream_command(args: str) -> DreamDistillResult:
    """Handle /dream — scan sessions, extract knowledge, update memory."""
    return DreamDistillResult(
        text="🧠 /dream — I'll scan recent session traces for persistent "
             "knowledge and update project memory. Working on it now...",
        agent_seed=DREAM_PROMPT,
    )


# ---------------------------------------------------------------------------
# /distill
# ---------------------------------------------------------------------------

DISTILL_PROMPT = """You are performing a /distill operation — discovering 
repeated manual workflows in recent work and packaging them into reusable 
skills, subagents, or commands.

**Goal:** Find patterns of repetitive manual work and automate them. High-confidence 
candidates become skills. Lower-confidence candidates are reported for review.

**Step 1: Discover repeated workflows.**
Use session_search() to scan recent sessions for patterns:
- Search for sequences of similar tool calls (e.g., repeated "deploy", 
  "build", "test", "lint", "format", "check", "verify")
- Search for common multi-step workflows (e.g., "first I'll... then I'll...")
- Look for tasks the user has asked you to do more than once
- Search for corrections — patterns where you did something wrong and had 
  to fix it the same way multiple times

**Step 2: Evaluate each candidate.**
For each workflow found, score it on:
- **Frequency:** How many times was it performed? (2+ = candidate)
- **Complexity:** How many steps? (3+ steps = worth automating)
- **Error rate:** Were there recurring mistakes? (high = needs a skill)
- **Generality:** Is this project-specific or broadly useful?

**Step 3: Package high-confidence candidates as skills.**
Use skill_manage(action='create', name='...', content='...') to create 
skills for workflows with high confidence (frequency >= 2, complexity >= 3).

Each skill should include:
- Clear trigger conditions (when to use it)
- Numbered steps with exact commands
- Pitfalls section documenting known mistakes
- Verification steps

**Step 4: Report lower-confidence candidates.**
For workflows that don't meet the threshold, list them as suggestions the 
user might want to automate manually.

**Step 5: Report summary.**
List what skills were created, what workflows were identified, and any 
suggestions for future automation.
"""


def handle_distill_command(args: str) -> DreamDistillResult:
    """Handle /distill — discover workflows, package as skills."""
    return DreamDistillResult(
        text="🔧 /distill — I'll scan recent sessions for repeated manual "
             "workflows and package high-confidence candidates into reusable "
             "skills. Working on it now...",
        agent_seed=DISTILL_PROMPT,
    )
