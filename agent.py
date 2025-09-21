from __future__ import annotations

from typing import Dict # type hinting for dictionaries
from uuid import uuid4 # generate unique session IDs

from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool
from strands.agent.conversation_manager import SlidingWindowConversationManager # conversation memory
import strands.types.content as types

from database import run_query

# In-memory map: session_id -> (Agent, ConversationManager)
_sessions: Dict[str, SlidingWindowConversationManager] = {}
_agents: Dict[str, Agent] = {}

SCHEMA = """CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT,
    price INT,
    color VARCHAR(30)
);"""

SYSTEM_PROMPT = f"""You are an expert PostgreSQL analyst. You will:
1. Write ONE valid PostgreSQL query based only on the provided schema.
2. Use the execute_sql tool to run it.
3. Respond with a concise natural language answer (do NOT include raw SQL unless specifically asked).
4. Use LOWER(column) for any case-insensitive text comparisons, such as a clause like "WHERE LOWER(color) = 'red'".
5. If information is unavailable, state that briefly and suggest a clarifying question.

Database Schema:
{SCHEMA}
"""

# tool definition for the agent to use
@tool
def execute_sql(sql_query: str) -> str:
    """Execute SQL query and return result string."""
    lowered = sql_query.lower()
    forbidden = ["drop table", "drop database", "truncate ", "alter table", "delete from"]
    if any(f in lowered for f in forbidden):
        return "Refused: potentially destructive statement."
    print(f"Executing query: {sql_query}")
    result = run_query(sql_query)
    print(f"--- AGENT: Received from database: {result} ---")
    return str(result)

# Session management
def _get_or_create_session(session_id: str | None, window_size: int = 10) -> str:
    """Return a valid session_id, creating structures if needed."""
    sid = session_id or str(uuid4())
    if sid not in _sessions:
        cm = SlidingWindowConversationManager(window_size=window_size)
        model = BedrockModel(
            max_tokens=512,
            model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        )
        agent = Agent(
            model=model,
            tools=[execute_sql],
            conversation_manager=cm,
            system_prompt=SYSTEM_PROMPT,
        )
        _sessions[sid] = cm
        _agents[sid] = agent
    return sid

# Generate response with per-session memory
async def generate_response(user_prompt: str, session_id: str | None = None) -> types.Message:
    """Generate a response with per-session memory.

    Returns the assistant message object from Strands. Caller can also keep
    track of the session_id (if newly created) to continue the conversation.
    """
    sid = _get_or_create_session(session_id)
    agent = _agents[sid]
    # Invoke with just the new user turn; conversation manager retains history
    response = agent(user_prompt)
    return response.message


def get_active_session_ids() -> list[str]:  # for utility (optional)
    return list(_sessions.keys())