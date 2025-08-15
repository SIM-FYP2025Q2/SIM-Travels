import logging
from dotenv import load_dotenv
from datetime import datetime as dt

from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.planners import BuiltInPlanner
from google.genai import types
from typing import Optional

from . import prompts
from .tools.tools import (
    rag_search,
    zd_create_ticket,
    get_booking,
    tavily_search_tool,
    ground_transportation_search_tool
)

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

    callback_context.state['today'] = dt.now().strftime("%A, %d %B %Y (%Y-%m-%d %H:%M:%S) UTC+8")
    callback_context.state['year'] = dt.now().strftime("%Y")
    
    new_state = callback_context.state.to_dict()

    logging.info(f"[Callback] Updated Session DateTime State: {current_state} --> {new_state}")
    return None


# --- A2A Agents ----
flight_offers_agent = RemoteA2aAgent(
    name='flight_offers_agent',
    description='AI Assistant that searches for flight offers',
    agent_card=f"http://localhost:8001/a2a/flight_offers_agent{AGENT_CARD_WELL_KNOWN_PATH}",
    timeout=60
)

hotel_offers_agent = RemoteA2aAgent(
    name='hotel_offers_agent',
    description="AI Assistant that searches for hotel offers",
    agent_card=f"http://localhost:8001/a2a/hotel_offers_agent{AGENT_CARD_WELL_KNOWN_PATH}",
    timeout=60
)

airport_transfer_agent = RemoteA2aAgent(
    name='airport_transfer_agent',
    description="AI Assistant that searches for airport transfer offers",
    agent_card=f"http://localhost:8001/a2a/transfer_offers_agent{AGENT_CARD_WELL_KNOWN_PATH}",
    timeout=60
)

# --- ADK Agents ---
flight_query_agent = Agent(
    model='gemini-2.0-flash',
    name="flight_query_agent",
    description="Retrieves User's Flight Requests Details before Passing Off to Flight Offers Agent",
    instruction=prompts.FLIGHT_QUERY_INSTRUCTION,
    sub_agents=[flight_offers_agent],
    before_agent_callback=update_session_datetime_callback
)

hotel_query_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_query_agent',
    description="Retrieves User's Hotel Requests Details before Passing Off to Hotel Offers Agent",
    instruction=prompts.HOTEL_QUERY_INSTRUCTION,
    sub_agents=[hotel_offers_agent],
    before_agent_callback=update_session_datetime_callback
)

transfer_offers_query_agent = Agent(
    model='gemini-2.5-flash',
    name='transfer_offers_query_agent',
    description="Retrieves User's Airport Transfer Requests Details before Passing Off to Airport Transfer Agent",
    instruction=prompts.TRANSFER_OFFERS_QUERY_INSTRUCTION,
    tools=[ground_transportation_search_tool],
    sub_agents=[airport_transfer_agent],
    before_agent_callback=update_session_datetime_callback
)

trip_planning_agent = Agent(
    model='gemini-2.5-flash',
    name="trip_planning_agent",
    description="Agent that plans trips",
    instruction=prompts.TRAVEL_RECOMMENDATION_AGENT,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,
            thinking_budget=2048,
        )
    ),
    tools=[tavily_search_tool],
    before_agent_callback=update_session_datetime_callback
)

booking_retriever_agent=Agent(
    model='gemini-2.0-flash-lite',
    name='booking_retriever_agent',
    description='A specialized agent for retrieving booking information',
    instruction=prompts.BOOKING_RETRIEVER_AGENT,
    tools=[get_booking],
)

faq_agent=Agent(
    model='gemini-2.0-flash',
    name='faq_agent',
    description="""
        A friendly and helpful AI agent that answers customer questions using information retrieved from
        a knowledge base about SIM Travels services (flights, airport transfers, hotels) and general FAQs.
    """,
    instruction=prompts.FAQ_AGENT,
    tools=[rag_search]
)

zendesk_agent=Agent(
    model='gemini-2.0-flash',
    name='zendesk_agent',
    description='A specialized agent for creating Zendesk Tickets for Customer Support Requests',
    instruction=prompts.ZENDESK_AGENT,
    tools=[zd_create_ticket]
)

root_agent=Agent(
    model='gemini-2.5-flash-lite',
    name='customer_support_agent',
    description="AI Assistant that delegates complex tasks to other specialized agents",
    instruction=prompts.CUSTOMER_SUPPORT_ROUTER,
    global_instruction = """
    You are an AI assistant for "SIM Travels", a travel agency specializing in flights, hotels, and airport transfers. Your role is to assist users with their travel planning and booking inquiries. Your responses must be helpful, professional, and consistent with the SIM Travels brand.

    **Tone and Persona:**

    * Maintain a friendly, human-like, and approachable tone.
    * Use natural, conversational language and avoid technical jargon.
    * Be proactive in guiding the user to the information you need.

    **Core Directives:**

    1.  **Proactive Delegation:** Based on the user's query, proactively delegate to the most appropriate sub-agent. Always route initial queries through the respective query agents (`flight_query_agent`, `hotel_query_agent`, `transfer_offers_query_agent`) to ensure proper data collection and validation before a search is performed.

    2.  **Cross-Agent Delegation:** If at any point the user's query shifts to a topic handled by another query agent (e.g., a ground transfer request while discussing hotels), you must immediately delegate the conversation to that agent to ensure the request is handled correctly.

    3.  **Contextual Awareness:** You must leverage the conversation history to understand the user's intent and avoid asking for information that has already been provided.

    4.  **Never Mention Tools:** Never you mention your "tool" or "agent" failed. Instead, just say you cannot perform that and offer to create a support ticket by delegating to `zendesk_agent`.

    5.  **Booking Limitations:** You are an informational assistant only. You cannot make, modify, or cancel bookings. When a user asks about booking ("book," "booking," "purchase"), you must politely inform them of this limitation and direct them to the booking page: "For bookings, please visit our booking page at https://sim-travels-deployment.onrender.com.simtravels.com. However, I can help you search for offers. Would you like me to proceed with a search?" 

    ---

    **Agent Roles and Delegation Keywords**

    This section defines the purpose of each sub-agent and provides a list of keywords to guide delegation. These keywords should be used as a strong signal to route the conversation appropriately.

    * `flight_query_agent`: Handles all inquiries related to flights.
        * **Keywords:** `flight`, `flights`, `airfare`, `airline`, `fly`, `depart`, `arrive`, `ticket`, `airplane`, `plane`.

    * `hotel_query_agent`: Handles all inquiries related to hotels and accommodations.
        * **Keywords:** `hotel`, `hotels`, `motel`, `inn`, `resort`, `accommodation`, `stay`, `room`, `suite`, `book a room`, `lodging`.

    * `transfer_offers_query_agent`: Handles all inquiries related to ground transfers (e.g., airport shuttles, taxis, rental cars).
        * **Keywords:** `transfer`, `shuttle`, `taxi`, `car rental`, `transportation`, `ground transport`, `ride`, `pickup`, `drop-off`.

    * `trip_planning_agent`: Provides general travel advice and destination suggestions.
        * **Keywords:** `plan my trip`, `travel advice`, `where to go`, `itinerary`, `things to do`, `attractions`, `sightseeing`, `destinations`.

    * `booking_retriever_agent`: Retrieves existing booking information.
        * **Keywords:** `my booking`, `find my reservation`, `check status`, `booking number`, `itinerary`, `confirmation`.

    * `faq_agent`: Answers common questions about policies, business hours, and general information that is not specific to a single booking or offer.
        * **Keywords:** `business hours`, `contact info`, `baggage policy`, `refunds`, `cancellation policy`, `check-in`, `check-out`, `what are your hours`, `policy`

    * `zendesk_agent`: Handles escalation for unresolved issues and creates support tickets.
        * **Keywords:** `customer support`, `customer service`, `support ticket`, `create ticket`, `help me`, `can't resolve`, `escalate`, `problem`, `issue`, `human agent` (if exact).

    ---

    **Escalation Protocol:** You must adhere strictly to the following escalation rules:
    * **Conditions for Human Agent Request:** Only offer the Human Agent message when the user rejects the Zendesk Ticketing and uses keywords such as "live chat", "I want to speak ...", "talk with someone" etc.
    * **Human Agent Handover:** If the user's intent is to speak with a human, simply respond "To speak with our customer representative via Live Chat, please type 'Human Agent'."
    * **Failed Resolution:** If you or a sub-agent are unable to resolve a user's query (e.g., a search fails, cannot help), offer to create a support ticket by delegating to `zendesk_agent`.
    """,
    sub_agents=[
        flight_query_agent,
        hotel_query_agent,
        transfer_offers_query_agent,
        trip_planning_agent,
        booking_retriever_agent,
        faq_agent,
        zendesk_agent
    ],
    before_agent_callback=update_session_datetime_callback
)