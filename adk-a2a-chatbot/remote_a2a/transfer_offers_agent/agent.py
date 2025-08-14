import os
import logging
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional
from datetime import datetime as dt

from . import prompts

today = dt.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"server-{today}.log"

logger = logging.basicConfig(level=logging.DEBUG, filename=log_filename, filemode="w")
logger = logging.getLogger(__name__)

load_dotenv()

# Before Agent Callback Function
def update_session_datetime_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    logging.info(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    logging.info(f"[Callback] Current Session State: {current_state}")

    callback_context.state['today'] = dt.now().strftime("%A, %d %B %Y (%Y-%m-%d %H:%M:%S)")
    new_state = callback_context.state.to_dict()

    logging.info(f"[Callback] Updated Session DateTime State: {current_state} --> {new_state}")
    return None

root_agent=Agent(
    model='gemini-2.0-flash',
    name='transfer_offers_agent',
    description='A specialized agent for searching and providing information about airport transfer offers',
    instruction=prompts.TRANSFER_OFFERS_AGENT,
    tools=[
        MCPToolset(connection_params=
            StreamableHTTPConnectionParams(
                url=os.getenv('MCP_SERVER_URL')
            ),
            tool_filter=["search_airport_transfers"]
        )
    ],
    output_key='transfer_offers',
    before_agent_callback=update_session_datetime_callback
)

# a2a_app = to_a2a(root_agent, port=8001)
# uvicorn hotel_offers.agent:a2a_app --host localhost --port 8002