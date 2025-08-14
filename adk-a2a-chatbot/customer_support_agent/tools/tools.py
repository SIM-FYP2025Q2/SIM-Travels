import logging
import os
import json
import requests
from requests.auth import HTTPBasicAuth

from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults
from mysql.connector import (connection)
from pinecone import Pinecone
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

logger = logging.getLogger(__name__)


# --- Custom Tools ----
def rag_search(user_query:str) -> dict:
    """Embeds texts with Text Embedding Model, then queries Pinecone Index

    Returns:
        "status" and "responses"
    """

    # Specify Embedding Model & Parameters
    model = TextEmbeddingModel.from_pretrained("text-embedding-005")
    kwargs = dict(output_dimensionality=768)

    # Get Embeddings
    embeddings = []
    text_input = TextEmbeddingInput(text=user_query, task_type="QUESTION_ANSWERING")
    embedding = model.get_embeddings([text_input], **kwargs)
    embeddings.append(embedding[0].values)

    if len(embeddings[0]) != 768:
        return {"status": "error"}

    # Query Pinecone Index
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    index = pc.Index(host=os.getenv('PINECONE_INDEX_HOST'))
    response = index.query(
        vector=embeddings,
        top_k=5,
        include_metadata=True
    )

    # Return Top 5 Matches
    matches = response.to_dict()
    return({'status':'success', 'response': matches})

def zd_create_ticket(
    customer_name: str,
    customer_email: str,
    title: str,
    description: str,
    priority: str
) -> dict:

    url = os.getenv('ZENDESK_API_URL')
    
    # Default `priority` to 'normal' if incorrectly provided
    priority = priority.lower()
    if priority not in ['low', 'normal', 'high', 'urgent']:
        priority = 'normal'

    # Ticket Headers and Payloads
    headers = {"Content-Type": "application/json"}
    payload = {
        "ticket": {
            "subject": title,
            "comment": {
                "body": description
            },
            "priority": priority.lower(),
            "requester": {
                "name": customer_name,
                "email": customer_email
            }
        }
    }

    # Authentication
    zd_email = os.getenv('ZENDESK_EMAIL')
    token = os.getenv('ZENDESK_API_KEY')
    auth = HTTPBasicAuth(f'{zd_email}/token', token)

    # POST Request (Create Ticket)
    response = requests.request(
        "POST",
        url,
        auth=auth,
        headers=headers,
        json=payload
    )

    # Response Handling
    if response.status_code == 201:
        return {"status": "success"}
    else:
        return {"status": "Error, Please email support@simtravels.com for further assistance."}



def get_booking(booking_id: str, last_name: str) -> dict:
    """Retrieves travel booking information from the database.

    This tool securely fetches details for a specific travel booking (which can be a
    flight, hotel, or airport transfer) by requiring both the unique booking ID and
    the last name of the lead traveler. This two-factor approach ensures that only
    the legitimate owner can access the information.

    Args:
        booking_id (str): The unique reference number for the booking (e.g., 'R8XYZP').
        last_name (str): The last name of the lead traveler associated with the booking.

    Returns:
        dict: A dictionary containing the booking information if a match is found.
            The dictionary will have the following keys: 'booking_id', 'last_name',
            'booking_type', and 'booking_details'. Returns None if no matching
            booking is found.
    """

    if len(booking_id) != 8:
        return "I'm sorry, that is an invalid booking ID."
    else: 
        booking_id = booking_id.lower()

    # Title Case Last Name
    last_name = last_name.strip()
    last_name = last_name.title()

    if last_name.count(' ') > 0:
        return "I'm sorry, that is an invalid last name."
    
    # MySQL Connection
    cnx = connection.MySQLConnection(
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWD'),
            host=os.getenv('MYSQL_SERVER_URL'),
            database='bookings')
    
    cursor = cnx.cursor()
    query = ("SELECT booking_id, last_name, booking_type, booking_details "
              "FROM bookings "
              "WHERE booking_id = %s AND last_name = %s")
    cursor.execute(query, (booking_id, last_name))

    # Retrieve Data
    row = cursor.fetchone()
    returnVal = None
    if not row:
        returnVal = {"status":"error", "results": "Error, no matching booking found."}
    else:
        columns = cursor.column_names
        booking_dict = dict(zip(columns, row))
        logging.info("Found Booking!")
        logging.info(booking_dict)
        returnVal = {"status":"success", "results": json.dumps(booking_dict, indent=4)}

    # Close Connection
    cursor.close()
    cnx.close()

    return returnVal

# --- 3rd Party Tools (Tavily Search) ---
tavily_tool_instance = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
)
tavily_search_tool = LangchainTool(tool=tavily_tool_instance)

transport_tavilyToolInstance = TavilySearchResults(
    max_results=3,
    search_depth="basic",
    include_answer=True,
    include_raw_content=False,
    include_images=False,
)
ground_transportation_search_tool = LangchainTool(tool=transport_tavilyToolInstance)