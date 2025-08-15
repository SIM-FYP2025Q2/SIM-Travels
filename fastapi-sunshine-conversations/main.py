import os
import logging
from datetime import datetime as dt

import requests
import sunshine_conversations_client
from sunshine_conversations_client.rest import ApiException
from dotenv import load_dotenv
from fastapi import Request, FastAPI


logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Zendesk Sunshine Authentication
# Defining the host is optional and defaults to https://api.smooch.io
# See configuration.py for a list of all supported configuration parameters.
ZENDESK_SUBDOMAIN = os.environ.get("ZENDESK_SUBDOMAIN")
KEY_ID = os.environ.get("KEY_ID")
KEY_SECRET = os.environ.get("KEY_SECRET")

# ADK Agent Endpoint
url = "http://localhost:8080"
appName = "apps/customer_support_agent"

REPLY_ACTIONS = [
    {"type":"reply", "text":"✈️ Flight Offers", "payload":"What flight offers are there?"},
    {"type":"reply", "text":"🏨 Hotel Offers", "payload":"What hotel offers are there?"},
    {"type":"reply", "text":"🚗 Transfer Offers", "payload":"What transfer offers are there?"},
    {"type":"reply", "text":"🏖️ Trip Planning", "payload":"Plan me a trip"},
    {"type":"reply", "text":"📄 My Bookings", "payload":"I want to retrieve my booking."},
    {"type":"reply", "text":"❓ I have an issue.", "payload":"I have an issue."}
]

configuration = sunshine_conversations_client.Configuration(
    host = f"https://{ZENDESK_SUBDOMAIN}/sc"
)
# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration.username = KEY_ID
configuration.password = KEY_SECRET

def chat_with_agent(msg, conversation_id):
    response = requests.post(
        url=f"{url}/run",
        headers={"Content-Type": "application/json"},
        json={
            "app_name": "customer_support_agent",
            "user_id": conversation_id,
            "session_id": conversation_id,
            "new_message": {
                "role": "user",
                "parts": [{ "text": msg }]
            }
        }
    )

    data = response.json()
    return extract_adk_response_text(data)

def extract_adk_response_text(data):
    """
    Extracts the final response text from an ADK response object.

    Args:
        response: The ADK response object, which can be in various formats.

    Returns:
        The extracted text string, or None if no text could be found.
    """
    logging.error(f'Attempting to Extract Text from ADK Response: {data}')
    
    # If Message is Type List, extract last event ['content'] for Response
    if isinstance(data, list) and data:
        
        last_event = data[-1]
        content = last_event.get('content')

        if isinstance(content, list):
            # Multiple Message Response
            last_message = content[-1]
            return last_message.get('parts', [{}])[0].get('text', None)
        elif content:
            # Single Message Response
            return content.get('parts', [{}])[0].get('text', None)

    # If Response Format is A2A Message Type, Extract as A2A Response
    if data and isinstance(data, dict) and data.get('kind') == 'task' and isinstance(data.get('messages'), list):
        messages = data.get('messages')
        if messages:
            last_message = messages[-1]
            if isinstance(last_message.get('parts'), list) and last_message.get('parts'):
                return last_message['parts'][0].get('text', None)

    # Return None if Response Extraction Fail
    logging.error('Could not extract text from the ADK response.')
    return None


def greetUser(app_id, conversation_id) -> None:
    with sunshine_conversations_client.ApiClient(configuration) as api_client:
        api_instance = sunshine_conversations_client.MessagesApi(api_client)
        message_post = sunshine_conversations_client.MessagePost(
                    author=sunshine_conversations_client.Author(
                        type="business",
                        avatar_url="https://2.gravatar.com/avatar/4db80f1d503fa685df4666148aa4d19001b2ada2495ffc5ccb68bbba927df965?size=256&d=initials"
                    ),
                    content=sunshine_conversations_client.Content(
                        type="text",
                        text=f"Hello! I'm SIM Travels AI Assistance. How can I help you?",
                        actions=REPLY_ACTIONS
                    )
        )
        api_response = api_instance.post_message(app_id, conversation_id, message_post)

def replyUser(app_id, conversation_id, message) -> None:
    with sunshine_conversations_client.ApiClient(configuration) as api_client:
        actions_instance = sunshine_conversations_client.SwitchboardActionsApi(api_client)
        activity_instance =  sunshine_conversations_client.ActivitiesApi(api_client)
        api_instance = sunshine_conversations_client.MessagesApi(api_client)

        if message == "human agent":
            try:
                logging.info(f"POST Message: 'Transferring you to our human agent.'")
                # Post Message
                message_post = sunshine_conversations_client.MessagePost(
                    author=sunshine_conversations_client.Author(
                        type="business",
                        avatar_url="https://2.gravatar.com/avatar/4db80f1d503fa685df4666148aa4d19001b2ada2495ffc5ccb68bbba927df965?size=256&d=initials"
                    ),
                    content=sunshine_conversations_client.Content(type="text", text=f"Transferring you to our human agent.")
                )
                api_response = api_instance.post_message(app_id, conversation_id, message_post)
                actions_instance.pass_control(app_id, conversation_id, sunshine_conversations_client.PassControlBody(switchboard_integration="680dd9871fa4e64eeffbb27e"))
            except ApiException as e:
                logging.error("Exception when calling MessagesApi->post_message: %s\n" % e)
                message_post = sunshine_conversations_client.MessagePost(
                    author=sunshine_conversations_client.Author(
                        type="business",
                        avatar_url="https://2.gravatar.com/avatar/4db80f1d503fa685df4666148aa4d19001b2ada2495ffc5ccb68bbba927df965?size=256&d=initials"
                    ),
                    content=sunshine_conversations_client.Content(type="text", text="I'm sorry, an unknown error ocurred. Please try reaching out later.")
                )
                api_response = api_instance.post_message(app_id, conversation_id, message_post)
                actions_instance.pass_control(app_id, conversation_id, sunshine_conversations_client.PassControlBody(switchboard_integration="680dd9871fa4e64eeffbb27e"))
            finally:
                return None
    
        # Send Typing Activity
        logging.info(f"Typing activity initated")
        typingActivity = {"author":{"type":"business"},"type":"typing:start"}
        activity_instance.post_activity(app_id, conversation_id, typingActivity)

        # Retrieve Agent Response
        logging.info(f"Getting Agent Response")
        agentResponse = chat_with_agent(message, conversation_id)
        try:
            logging.info(f"POST Message (Agent Response): {agentResponse}")
            # Post Message
            message_post = sunshine_conversations_client.MessagePost(
                author=sunshine_conversations_client.Author(
                    type="business",
                    avatar_url="https://2.gravatar.com/avatar/4db80f1d503fa685df4666148aa4d19001b2ada2495ffc5ccb68bbba927df965?size=256&d=initials"
                ),
                content=sunshine_conversations_client.Content(
                    type="text",
                    markdown_text=f"{agentResponse}",
                    actions=REPLY_ACTIONS)
            )
            api_response = api_instance.post_message(app_id, conversation_id, message_post)
        except ApiException as e:
            logging.error("Exception when calling MessagesApi->post_message: %s\n" % e)
            message_post = sunshine_conversations_client.MessagePost(
                author=sunshine_conversations_client.Author(
                    type="business",
                    avatar_url="https://2.gravatar.com/avatar/4db80f1d503fa685df4666148aa4d19001b2ada2495ffc5ccb68bbba927df965?size=256&d=initials"
                ),
                content=sunshine_conversations_client.Content(type="text", text="I'm sorry, an unknown error ocurred. Please try reaching out later.")
            )
            api_response = api_instance.post_message(app_id, conversation_id, message_post)
        finally:
            return None

@app.get("/")
async def root():
    logging.info("Root endpoint was called.")
    return {"message": "FastAPI is working!"}

@app.post("/messages")
async def messages(data: Request):
    request_body = await data.json()
    logging.info(f"Received message with body: {request_body}")

    events = request_body['events'][0]
    payload = events['payload']

    # Author, App ID, Conversation ID
    app_id = request_body['app']['id']
    conversation_id = payload['conversation']['id']
    conversation_source = payload['conversation']['activeSwitchboardIntegration']['integrationType']

    # Do not proceed if event is not message
    if events['type'] == "conversation:create":
        greetUser(app_id, conversation_id)
        return 200
    
    if events['type'] != "conversation:message":
        return 200
    
    if (conversation_source == "custom"):
        logging.info("Checking for existing session")
        # Retrieve Session (if exists)
        sessionResponse = requests.get(
            url=f"{url}/{appName}/users/{conversation_id}/sessions/{conversation_id}",
            headers={"Content-Type": "application/json"}
        )
        logging.info(f"Session Found")

        if sessionResponse.status_code != 200:
            logging.info("Session not Found, creating new session")

            # Create Session
            newSession = requests.post(
                url=f"{url}/{appName}/users/{conversation_id}/sessions/{conversation_id}",
                headers={"Content-Type": "application/json"},
                json={ "state": {
                    "current_timestamp": dt.now().strftime("%Y-%m-%dT%H:%M:%S")} 
                }
            )
            if newSession.status_code == 200:
                logging.warning(f"Successfully Created Session {conversation_id}")
            else:
                logging.warning(f"Failed to Create Session {newSession.status_code} for ID {conversation_id}. Agent may not be able to communicate!")
        
        # Message from User Received
        if (events['type'] == "conversation:message"):
            author = payload['message']['author']['type']
            if (author == 'user'):
                receivedMsg = payload['message']['content']['text']
                receivedMsg = receivedMsg.lower().strip()
                logging.info(f"Received Message: {receivedMsg}")
                replyUser(app_id, conversation_id, receivedMsg)
            return 200
        else:
            return 200