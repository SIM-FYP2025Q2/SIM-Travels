import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
from pinecone import Pinecone
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from . import prompts

load_dotenv()


# --- Tools ----
def rag_search(user_query:str) -> dict:
    """Embeds texts with Text Embedding Model, then queries Pinecone Index 

    Returns:
        A list of lists containing the embedding vectors for each input text
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


def hotels_search(
    location:str,
    checkin_date:str,
    checkout_date:str,
    num_guests:int,
    num_rooms:int
) -> dict:
    """
    Simulates a successful search for hotels in Kuala Lumpur and returns sample hotel data.

    Args:
        checkin_date (str): The desired check-in date in 'YYYY-MM-DD' format. Defaults to today + 7 days.
        checkout_date (str): The desired check-out date in 'YYYY-MM-DD' format. Defaults to checkin_date + 3 days.
        num_guests (int): The number of guests.
        num_rooms (int): The number of rooms.

    Returns:
        dict: A dictionary containing the search status and sample hotel offers.
    """

    # Sample hotel data for Kuala Lumpur
    sample_hotels = [
        {
            "hotel_id": "HTL001",
            "name": "Traders Hotel Kuala Lumpur",
            "city": "Kuala Lumpur",
            "country": "Malaysia",
            "price_per_night_currency": "MYR",
            "price_per_night_amount": 450.00,
            "stars": 5,
            "rating": 8.9,
            "amenities": ["Pool", "Gym", "Restaurant", "Spa", "Free WiFi"],
            "description": "Luxury hotel with stunning views of the Petronas Twin Towers."
        },
        {
            "hotel_id": "HTL002",
            "name": "Shangri-La Kuala Lumpur",
            "city": "Kuala Lumpur",
            "country": "Malaysia",
            "price_per_night_currency": "MYR",
            "price_per_night_amount": 580.00,
            "stars": 5,
            "rating": 9.1,
            "amenities": ["Pool", "Gym", "Multiple Restaurants", "Bar", "Spa", "Free WiFi"],
            "description": "Award-winning hotel offering exceptional service and amenities."
        },
        {
            "hotel_id": "HTL003",
            "name": "Holiday Inn Express Kuala Lumpur City Centre",
            "city": "Kuala Lumpur",
            "country": "Malaysia",
            "price_per_night_currency": "MYR",
            "price_per_night_amount": 220.00,
            "stars": 3,
            "rating": 8.2,
            "amenities": ["Free Breakfast", "Free WiFi", "Gym"],
            "description": "Convenient and modern hotel in the heart of the city."
        }
    ]

    return {
        "status": "success",
        "hotel_offers": sample_hotels
    }


def airport_transfer_search(
    pickup_datetime:str,
    airport_code:str,
    destination_address_line:str,
    destination_zip:str,
    destination_city_name:str,
    destination_country_code:str,
    selected_vehicle:str
) -> dict:
    """
    Generates a sample airport transfer record mimicking a successful search
    for Kuala Lumpur, based on a provided JSON structure.

    Args:
        pickup_datetime (str): The desired pickup date and time in ISO format (e.g., "YYYY-MM-DDTHH:MM:SS").
                                          Defaults to 7 days from today at 10:30 AM.
        airport_code (str): The IATA code for the airport. Defaults to "KUL".
        destination_address_line (str): The street address or landmark for the destination.
                                                  Defaults to "KLCC, Kuala Lumpur City Centre".
        destination_zip (str): The postal code of the destination. Defaults to "50088".
        destination_city_name (str): The city name of the destination. Defaults to "Kuala Lumpur".
        destination_country_code (str): The country code of the destination. Defaults to "MY".
        vehicle_type (str): The type of vehicle (e.g., "SEDAN", "VAN", "SUV"). Defaults to "SEDAN".

    Returns:
        dict: A dictionary containing a sample airport transfer offer for Kuala Lumpur.
    """

    airport_code = "KUL",
    destination_address_line = "KLCC, Kuala Lumpur City Centre",
    destination_zip = "50088",
    destination_city_name = "Kuala Lumpur",
    destination_country_code = "MY",
    vehicle_type = "VAN"

    # Generate a default pickup_datetime if not provided
    future_date = datetime.now() + timedelta(days=7)
    pickup_datetime = future_date.strftime("%Y-%m-%dT%H:%M:%S")

    sample_record = [
    {
        "id": "transfer_1_xyz",
        "provider": "Local Taxis",
        "vehicle_type": selected_vehicle,
        "price": {
            "amount": 75.00,
            "currency": "MYR"
        },
        "duration_minutes": 45,
        "distance_km": 60,
        "pickup_details": {
            "datetime": pickup_datetime,
            "airport_code": airport_code,
            "terminal": "KLIA1"
        },
        "destination_details": {
            "address_line": destination_address_line,
            "zip": destination_zip,
            "city_name": destination_city_name,
            "country_code": destination_country_code
        },
        "notes": "Meet and greet service at arrival hall."
    },
    {
        "id": "transfer_2_abc",
        "provider": "RideShare Premium",
        "vehicle_type": "SUV",
        "price": {
            "amount": 110.00,
            "currency": "MYR"
        },
        "duration_minutes": 50,
        "distance_km": 60,
        "pickup_details": {
            "datetime": pickup_datetime,
            "airport_code": airport_code,
            "terminal": "KLIA1"
        },
        "destination_details": {
            "address_line": destination_address_line,
            "zip": destination_zip,
            "city_name": destination_city_name,
            "country_code": destination_country_code
        },
        "notes": "Luxury SUV with professional driver."
    },
    {
        "id": "transfer_3_def",
        "provider": "Airport Shuttle",
        "vehicle_type": "VAN",
        "price": {
            "amount": 50.00,
            "currency": "MYR"
        },
        "duration_minutes": 65,
        "distance_km": 60,
        "pickup_details": {
            "datetime": pickup_datetime,
            "airport_code": airport_code,
            "terminal": "KLIA2"
        },
        "destination_details": {
            "address_line": destination_address_line,
            "zip": destination_zip,
            "city_name": destination_city_name,
            "country_code": destination_country_code
        },
        "notes": "Shared ride, multiple stops possible."
    }
]
    # Return the sample record
    return {
        "status": "success",
        "airport_transfer_offers": sample_record
    }

# --- Agents ---- 
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

flight_offers_agent=Agent(
    model='gemini-2.0-flash',
    name='flight_offers_agent',
    description='A helpful AI assistant that can search flight offers',
    instruction=prompts.FLIGHT_OFFERS_AGENT,
    tools=[
        MCPToolset(connection_params=
            SseConnectionParams(
                url=f"{os.getenv('MCP_SERVER_URL')}",
                timeout=10,
                sse_read_timeout=60))]
)

hotel_offers_agent = Agent(
    model='gemini-2.0-flash',
    name='hotel_offers_agent',
    description='A specialized agent for searching and providing information about hotel accommodations.',
    instruction=prompts.HOTEL_OFFERS_AGENT,
    tools=[hotels_search]
)

airport_transfer_agent = Agent(
    model='gemini-2.0-flash',
    name='airport_transfer_agent',
    description='A specialized agent for searching and providing information about airport transfers.',
    instruction=prompts.AIRPORT_TRANSFER_AGENT,
    tools=[airport_transfer_search]
)


flight_offers_tool = AgentTool(agent=flight_offers_agent)
hotel_offers_tool = AgentTool(agent=hotel_offers_agent)
airport_transfer_tool = AgentTool(agent=airport_transfer_agent)
faq_tool = AgentTool(agent=faq_agent)

root_agent=Agent(
    model='gemini-2.5-flash',
    name='customer_support_agent',
    description="Friendly AI Agent that answers customer's questions about SIM Travels services, including flights, hotels, airport transfers, and general FAQs.",
    instruction=prompts.CUSTOMER_SUPPORT_ROUTER,
    tools=[
        flight_offers_tool,
        hotel_offers_tool,
        airport_transfer_tool,
        faq_tool
    ],
)