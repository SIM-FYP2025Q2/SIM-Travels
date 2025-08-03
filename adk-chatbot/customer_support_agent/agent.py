import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from pinecone import Pinecone
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from google.adk.tools import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults
from google.adk.agents import SequentialAgent
from langchain_tavily import TavilySearch  

from . import prompts

load_dotenv()

# Global Memory Dictionary
global_memory = {}

# --- Hotels Data for Multiple Destinations ----
hotels_data = {
    "Kuala Lumpur": [
        {"hotel_id": "HTL001", "name": "The Ritz-Carlton, Kuala Lumpur", "city": "Kuala Lumpur"},
        {"hotel_id": "HTL002", "name": "Mandarin Oriental, Kuala Lumpur", "city": "Kuala Lumpur"},
        {"hotel_id": "HTL003", "name": "Grand Hyatt Kuala Lumpur", "city": "Kuala Lumpur"},
        {"hotel_id": "HTL004", "name": "Shangri-La Hotel Kuala Lumpur", "city": "Kuala Lumpur"},
        {"hotel_id": "HTL005", "name": "Traders Hotel Kuala Lumpur", "city": "Kuala Lumpur"}
    ],
    "Tokyo": [
        {"hotel_id": "HTL006", "name": "Park Hyatt Tokyo", "city": "Tokyo"},
        {"hotel_id": "HTL007", "name": "Shangri-La Hotel Tokyo", "city": "Tokyo"},
        {"hotel_id": "HTL008", "name": "The Peninsula Tokyo", "city": "Tokyo"},
        {"hotel_id": "HTL009", "name": "Mandarin Oriental Tokyo", "city": "Tokyo"},
        {"hotel_id": "HTL010", "name": "The Ritz-Carlton Tokyo", "city": "Tokyo"}
    ],
    "Paris": [
        {"hotel_id": "HTL011", "name": "Le Meurice", "city": "Paris"},
        {"hotel_id": "HTL012", "name": "The Ritz Paris", "city": "Paris"},
        {"hotel_id": "HTL013", "name": "Shangri-La Hotel Paris", "city": "Paris"},
        {"hotel_id": "HTL014", "name": "Four Seasons Hotel George V", "city": "Paris"},
        {"hotel_id": "HTL015", "name": "Hotel Le Bristol", "city": "Paris"}
    ],
    "New York": [
        {"hotel_id": "HTL016", "name": "The Plaza Hotel", "city": "New York"},
        {"hotel_id": "HTL017", "name": "The St. Regis New York", "city": "New York"},
        {"hotel_id": "HTL018", "name": "Four Seasons Hotel New York Downtown", "city": "New York"},
        {"hotel_id": "HTL019", "name": "The Langham, New York", "city": "New York"},
        {"hotel_id": "HTL020", "name": "Conrad New York Downtown", "city": "New York"}
    ],
    "London": [
        {"hotel_id": "HTL021", "name": "The Dorchester", "city": "London"},
        {"hotel_id": "HTL022", "name": "Claridge’s", "city": "London"},
        {"hotel_id": "HTL023", "name": "The Savoy", "city": "London"},
        {"hotel_id": "HTL024", "name": "Four Seasons Hotel London at Park Lane", "city": "London"},
        {"hotel_id": "HTL025", "name": "Shangri-La Hotel at The Shard", "city": "London"}
    ],
    "Bali": [
        {"hotel_id": "HTL026", "name": "Four Seasons Resort Bali at Sayan", "city": "Bali"},
        {"hotel_id": "HTL027", "name": "The St. Regis Bali Resort", "city": "Bali"},
        {"hotel_id": "HTL028", "name": "The Ritz-Carlton Bali", "city": "Bali"},
        {"hotel_id": "HTL029", "name": "Alila Villas Uluwatu", "city": "Bali"},
        {"hotel_id": "HTL030", "name": "Bulgari Resort Bali", "city": "Bali"}
    ],
    "Dubai": [
        {"hotel_id": "HTL031", "name": "Burj Al Arab Jumeirah", "city": "Dubai"},
        {"hotel_id": "HTL032", "name": "Atlantis The Palm", "city": "Dubai"},
        {"hotel_id": "HTL033", "name": "Armani Hotel Dubai", "city": "Dubai"},
        {"hotel_id": "HTL034", "name": "Jumeirah Beach Hotel", "city": "Dubai"},
        {"hotel_id": "HTL035", "name": "The Address Boulevard", "city": "Dubai"}
    ],
    "Rome": [
        {"hotel_id": "HTL036", "name": "Hotel de Russie", "city": "Rome"},
        {"hotel_id": "HTL037", "name": "The St. Regis Rome", "city": "Rome"},
        {"hotel_id": "HTL038", "name": "Hotel Eden", "city": "Rome"},
        {"hotel_id": "HTL039", "name": "Palazzo Naiadi", "city": "Rome"},
        {"hotel_id": "HTL040", "name": "The Westin Excelsior Rome", "city": "Rome"}
    ],
    "Sydney": [
        {"hotel_id": "HTL041", "name": "The Langham, Sydney", "city": "Sydney"},
        {"hotel_id": "HTL042", "name": "Park Hyatt Sydney", "city": "Sydney"},
        {"hotel_id": "HTL043", "name": "Four Seasons Hotel Sydney", "city": "Sydney"},
        {"hotel_id": "HTL044", "name": "Shangri-La Hotel Sydney", "city": "Sydney"},
        {"hotel_id": "HTL045", "name": "The Darling at The Star", "city": "Sydney"}
    ],
    "Barcelona": [
        {"hotel_id": "HTL046", "name": "Hotel Arts Barcelona", "city": "Barcelona"},
        {"hotel_id": "HTL047", "name": "Mandarin Oriental Barcelona", "city": "Barcelona"},
        {"hotel_id": "HTL048", "name": "W Barcelona", "city": "Barcelona"},
        {"hotel_id": "HTL049", "name": "The Serras Hotel Barcelona", "city": "Barcelona"},
        {"hotel_id": "HTL050", "name": "Hotel Omm", "city": "Barcelona"}
    ]
}

# --- Tools ----
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


def hotels_search(location: str, checkin_date: str, checkout_date: str, num_guests: int, num_rooms: int, tool_context: ToolContext = None) -> dict:
    """
    Searches for hotels in the given location and returns sample hotel data.
    """
    if location not in hotels_data:
        return {"status": "error", "message": "Sorry, we don't have hotels available for that location."}

    # Retrieve the sample hotels data for the specific location
    sample_hotels = hotels_data.get(location, [])
    
    # Store both hotel ID and name in global memory
    global_memory["recent_hotels"] = {h["name"].lower(): {"hotel_id": h["hotel_id"], "name": h["name"]} for h in sample_hotels}

    # Store all available hotel names in global memory for future use
    global_memory["available_hotels"] = [h["name"] for h in sample_hotels]

    return {"status": "success", "hotel_offers": sample_hotels}

def handle_user_query_for_hotel_options(location: str, checkin_date: str, checkout_date: str, num_guests: int, num_rooms: int) -> str:
    # Get all hotels for the selected location
    hotels_list = hotels_data.get(location, [])
    
    # Show the first 3 hotels and store them in global memory as shown hotels
    if hotels_list:
        hotel_names = [hotel['name'] for hotel in hotels_list]
        global_memory["shown_hotels"] = hotel_names[:3]  # Store the first 3 shown hotels
        hotel_response = "\n".join(hotel_names[:3])  # Only show the first 3 hotels initially
        
        return f"I found several hotel options in {location} for your dates ({checkin_date} - {checkout_date}) for {num_guests} guest(s) and {num_rooms} room(s):\n\n{hotel_response}\n\nWould you like to check the room availability for any of these hotels?"
    else:
        return f"Sorry, we don't have any available hotels for {location}."

def handle_follow_up_for_more_hotels(location: str) -> str:
    # Get all hotels for the selected location
    hotels_list = hotels_data.get(location, [])
    
    # Get hotels already shown from global memory
    shown_hotels = global_memory.get("shown_hotels", [])
    
    # Filter out the hotels already shown
    remaining_hotels = [hotel['name'] for hotel in hotels_list if hotel['name'] not in shown_hotels]
    
    # If there are remaining hotels, show them
    if remaining_hotels:
        remaining_hotels_response = "\n".join(remaining_hotels)
        # Update global memory with the remaining shown hotels
        global_memory["shown_hotels"].extend(remaining_hotels)  # Add the remaining hotels to the shown list
        return f"Here are the remaining hotel options in {location}:\n\n{remaining_hotels_response}\n\nWould you like to check the room availability for any of these hotels?"
    else:
        return "There are no more hotels available in this location."

def handle_specific_hotel_request(location: str, hotel_name: str) -> str:
    # Check if the requested hotel is available in the location
    available_hotels = global_memory.get("available_hotels", [])
    if hotel_name in available_hotels:
        return f"Let me check room availability for {hotel_name} in {location}."
    else:
        return f"I'm sorry, I couldn't find {hotel_name} in {location}. Would you like me to search for other hotels?"

# Main conversation flow for initial and follow-up requests
def main_interaction_flow(location: str, checkin_date: str, checkout_date: str, num_guests: int, num_rooms: int):
    # Show the initial list of hotels (3 hotels)
    initial_response = handle_user_query_for_hotel_options(location, checkin_date, checkout_date, num_guests, num_rooms)
    
    # Display the initial response to the user (show 3 hotels)
    print(initial_response)  # For testing: you might return this in your actual code
    
    # Simulate a user asking for more options:
    user_query_for_more_hotels = "Are there any other hotels available?"  # Simulated user query
    
    if "other hotels" in user_query_for_more_hotels.lower():
        follow_up_response = handle_follow_up_for_more_hotels(location)
        
        # Display the follow-up response
        print(follow_up_response)  # For testing: you might return this in your actual code
    
    # Simulate user requesting a specific hotel:
    user_query_for_specific_hotel = "Show me rooms at The Peninsula Tokyo"  # Simulated query
    
    if "peninsula tokyo" in user_query_for_specific_hotel.lower():
        hotel_response = handle_specific_hotel_request(location, "The Peninsula Tokyo")
        print(hotel_response)  # For testing: you might return this in your actual code

def get_rooms_for_hotel(
    hotel_name: str,
    tool_context: ToolContext = None 
) -> dict:
    hotel_info = None

    # Retrieve hotel info from global memory based on the hotel name
    hotel_info = global_memory.get("recent_hotels", {}).get(hotel_name.lower())

    if not hotel_info:
        return {
            "status": "error",
            "message": f"Hotel '{hotel_name}' not found in recent memory. Please search for hotels first."
        }

    hotel_id = hotel_info["hotel_id"]
    
    # Sample rooms data
    sample_rooms = {
    "HTL001": [  # The Ritz-Carlton, Kuala Lumpur
        {"room_type": "Deluxe King", "price_per_night": 500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Twin Room", "price_per_night": 480.0, "available": True, 
         "bed_config": "2 Single Beds", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Club Room", "price_per_night": 650.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Executive Suite", "price_per_night": 950.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL002": [  # Mandarin Oriental, Kuala Lumpur
        {"room_type": "Superior Room", "price_per_night": 540.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Deluxe Room", "price_per_night": 600.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Premier Room", "price_per_night": 780.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Executive Suite", "price_per_night": 1100.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL003": [  # Grand Hyatt Kuala Lumpur
        {"room_type": "Grand King Room", "price_per_night": 550.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Grand Twin Room", "price_per_night": 520.0, "available": True, 
         "bed_config": "2 Twin Beds", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Grand Executive Suite", "price_per_night": 1100.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL004": [  # Shangri-La Hotel Kuala Lumpur
        {"room_type": "Deluxe Room", "price_per_night": 420.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Premier Room", "price_per_night": 550.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Shangri-La Suite", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL005": [  # Traders Hotel Kuala Lumpur
        {"room_type": "Superior Room", "price_per_night": 350.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Deluxe Room", "price_per_night": 400.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Executive Room", "price_per_night": 650.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL006": [  # Park Hyatt Tokyo
        {"room_type": "Park Deluxe Room", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Park Suite", "price_per_night": 2000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL007": [  # Shangri-La Hotel Tokyo
        {"room_type": "Deluxe Room", "price_per_night": 1500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Shangri-La Suite", "price_per_night": 3000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL008": [  # The Peninsula Tokyo
        {"room_type": "Deluxe King Room", "price_per_night": 1800.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Executive Suite", "price_per_night": 3500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL009": [  # Mandarin Oriental Tokyo
        {"room_type": "Superior Room", "price_per_night": 1700.0, "available": True, 
         "bed_config": "1 Queen Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Mandarin Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL010": [  # The Ritz-Carlton Tokyo
        {"room_type": "Club Room", "price_per_night": 2200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Ritz-Carlton Suite", "price_per_night": 5000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL011": [  # Le Meurice
        {"room_type": "Deluxe Room", "price_per_night": 950.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Signature Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL012": [  # The Ritz Paris
        {"room_type": "Deluxe Room", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Ritz Paris Suite", "price_per_night": 5000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL013": [  # Shangri-La Hotel Paris
        {"room_type": "Superior Room", "price_per_night": 950.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Shangri-La Suite", "price_per_night": 3500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL014": [  # Four Seasons Hotel George V
        {"room_type": "Premier Room", "price_per_night": 1500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Royal Suite", "price_per_night": 8000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL015": [  # Hotel Le Bristol
        {"room_type": "Deluxe Room", "price_per_night": 1300.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Imperial Suite", "price_per_night": 7000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL016": [  # The Plaza Hotel
        {"room_type": "Deluxe Room", "price_per_night": 1500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Grand Luxe Room", "price_per_night": 2500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL017": [  # The St. Regis New York
        {"room_type": "St. Regis Room", "price_per_night": 1800.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "St. Regis Suite", "price_per_night": 4500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL018": [  # Four Seasons Hotel New York Downtown
        {"room_type": "Superior Room", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Deluxe Room", "price_per_night": 1600.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL019": [  # The Langham, New York
        {"room_type": "Superior Room", "price_per_night": 900.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Langham Suite", "price_per_night": 2000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL020": [  # Conrad New York Downtown
        {"room_type": "King Room", "price_per_night": 1000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Executive Suite", "price_per_night": 2200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL021": [  # The Dorchester
        {"room_type": "Superior Room", "price_per_night": 1300.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Deluxe Room", "price_per_night": 1700.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL022": [  # Claridge’s
        {"room_type": "Classic Room", "price_per_night": 1300.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Claridge’s Suite", "price_per_night": 3500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL023": [  # The Savoy
        {"room_type": "River View Room", "price_per_night": 1600.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "The Savoy Suite", "price_per_night": 5000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL024": [  # Four Seasons Hotel London at Park Lane
        {"room_type": "Superior Room", "price_per_night": 2000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Park Lane Suite", "price_per_night": 5000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL025": [  # Shangri-La Hotel at The Shard
        {"room_type": "Shangri-La Suite", "price_per_night": 2500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Deluxe Room", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL026": [  # Four Seasons Resort Bali at Sayan
        {"room_type": "Garden View Room", "price_per_night": 900.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Pool Villa", "price_per_night": 1500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL027": [  # The St. Regis Bali Resort
        {"room_type": "St. Regis Suite", "price_per_night": 2000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True},
        {"room_type": "Ocean View Room", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL028": [  # The Ritz-Carlton Bali
        {"room_type": "Ocean Front Room", "price_per_night": 1300.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Royal Villa", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL029": [  # Alila Villas Uluwatu
        {"room_type": "Ocean View Villa", "price_per_night": 1500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Alila Villa", "price_per_night": 3000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL030": [  # Bulgari Resort Bali
        {"room_type": "Ocean View Room", "price_per_night": 1800.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Bulgari Villa", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL031": [  # Burj Al Arab Jumeirah
        {"room_type": "Ocean Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Royal Suite", "price_per_night": 8000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL032": [  # Atlantis The Palm
        {"room_type": "Ocean View Room", "price_per_night": 1000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Atlantis Suite", "price_per_night": 5000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL033": [  # Armani Hotel Dubai
        {"room_type": "Armani Classic Room", "price_per_night": 1500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Armani Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL034": [  # Jumeirah Beach Hotel
        {"room_type": "Ocean Deluxe Room", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Beachfront Suite", "price_per_night": 2500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL035": [  # The Address Boulevard
        {"room_type": "Classic Room", "price_per_night": 900.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Palace Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL036": [  # Hotel de Russie
        {"room_type": "Superior Room", "price_per_night": 1000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "De Russie Suite", "price_per_night": 3500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL037": [  # The St. Regis Rome
        {"room_type": "St. Regis Room", "price_per_night": 1300.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "St. Regis Suite", "price_per_night": 3000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL038": [  # Hotel Eden
        {"room_type": "Deluxe Room", "price_per_night": 1600.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Hotel Eden Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL039": [  # Palazzo Naiadi
        {"room_type": "Classic Room", "price_per_night": 800.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Palazzo Suite", "price_per_night": 2200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL040": [  # The Westin Excelsior Rome
        {"room_type": "Deluxe Room", "price_per_night": 950.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Excelsior Suite", "price_per_night": 3200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL041": [  # The Langham, Sydney
        {"room_type": "Superior Room", "price_per_night": 1100.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Deluxe Room", "price_per_night": 1400.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True}
    ],
    "HTL042": [  # Park Hyatt Sydney
        {"room_type": "Park Room", "price_per_night": 1800.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Opera Suite", "price_per_night": 5000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL043": [  # Four Seasons Hotel Sydney
        {"room_type": "City View Room", "price_per_night": 1300.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Harbour Suite", "price_per_night": 3500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL044": [  # Shangri-La Hotel Sydney
        {"room_type": "Deluxe Room", "price_per_night": 1200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Shangri-La Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL045": [  # The Darling at The Star
        {"room_type": "Superior Room", "price_per_night": 1100.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": False},
        {"room_type": "Sky Suite", "price_per_night": 3000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL046": [  # Hotel Arts Barcelona
        {"room_type": "Superior Room", "price_per_night": 800.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Presidential Suite", "price_per_night": 3500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL047": [  # Mandarin Oriental Barcelona
        {"room_type": "Superior Room", "price_per_night": 1000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Mandarin Suite", "price_per_night": 4000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL048": [  # W Barcelona
        {"room_type": "Wonderful Room", "price_per_night": 650.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Extreme Wow Suite", "price_per_night": 3000.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL049": [  # The Serras Hotel Barcelona
        {"room_type": "Deluxe Room", "price_per_night": 900.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Serras Suite", "price_per_night": 3200.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ],
    "HTL050": [  # Hotel Omm
        {"room_type": "Superior Room", "price_per_night": 750.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 2, "breakfast_included": True},
        {"room_type": "Executive Suite", "price_per_night": 2500.0, "available": True, 
         "bed_config": "1 King Bed", "max_occupancy": 3, "breakfast_included": True}
    ]
    }

    # Get available rooms
    available_rooms = sample_rooms.get(hotel_id, [])
    
    # Format room details for response
    if not available_rooms:
        return {
            "status": "error",
            "message": f"No rooms available for {hotel_name} during your selected dates."
        }

    # Format the room details as a response
    room_details = []
    for room in available_rooms:
        if room["available"]:
            room_details.append(f"- **{room['room_type']}**: {room['price_per_night']} MYR per night\n"
                                f"   - Bed Configuration: {room['bed_config']}\n"
                                f"   - Max Occupancy: {room['max_occupancy']} person(s)\n"
                                f"   - Breakfast Included: {'Yes' if room['breakfast_included'] else 'No'}")

    return {
        "status": "success",
        "rooms": "\n".join(room_details)
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

#=====================================================================================
def initialize_tavily_search_tool():
    """Initialize TavilySearch directly, no AgentTool wrapping."""
    tavily_search = TavilySearch(
        max_results=5,                # Number of results to return
        search_depth="advanced",      # Advanced search depth
        include_answer=True,          # Include direct answers in response
        include_raw_content=True,     # Include raw content of results
        include_images=True           # Include images in results
    )
    return tavily_search  # Return the tool directly

    
# Handle user query for trip planning
def handle_trip_planning_query(user_query: str):
    if "plan a trip" in user_query.lower() or "recommend a trip" in user_query.lower():
        # Call the travel_recommendation_agent
        return travel_recommendation_agent.run_async(query=user_query)
    else:
        return "I can help with that. What type of trip are you looking for?"

#=====================================================================================


# --- Agents ----
faq_agent = Agent(
    model='gemini-2.0-flash',
    name='faq_agent',
    description=""" 
    A friendly and helpful AI agent that answers customer questions using information retrieved from
    a knowledge base about SIM Travels services (flights, airport transfers, hotels) and general FAQs.
    """,
    instruction=prompts.FAQ_AGENT,
    tools=[rag_search]
)


flight_offers_agent = Agent(
    model='gemini-2.0-flash-lite',
    name='flight_offers_agent',
    description='AI Assistant that searches for flight offers',
    instruction=prompts.FLIGHT_OFFERS_AGENT,
    tools=[ 
        MCPToolset(connection_params=StreamableHTTPConnectionParams(url=os.getenv('MCP_SERVER_URL')),
                   tool_filter=["search_flight_offers"])
    ]
)

hotel_offers_agent = Agent(
    model='gemini-2.0-flash',
    name='hotel_offers_agent',
    description='A specialized agent for searching and providing information about hotel accommodations.',
    instruction=prompts.HOTEL_OFFERS_AGENT,
    tools=[hotels_search, get_rooms_for_hotel],
)

airport_transfer_agent = Agent(
    model='gemini-2.0-flash',
    name='airport_transfer_agent',
    description='A specialized agent for searching and providing information about airport transfers.',
    instruction=prompts.AIRPORT_TRANSFER_AGENT,
    tools=[airport_transfer_search]
)

# --Travel recommendation agent--
travel_recommendation_agent = Agent(
    model='gemini-2.0-flash',
    name='travel_recommendation_agent',
    description="Agent that helps recommend trips using the Tavily search tool.",
    instruction=prompts.TRAVEL_RECOMMENDATION_AGENT,
    tools=[initialize_tavily_search_tool()]  # Pass the tool directly, not wrapped
)

planning_agent = Agent(
    model='gemini-2.0-flash',
    name='planning_agent',
    description="Agent for planning trips using Tavily Search results.",
    instruction=prompts.PLANNING_AGENT,
    tools=[initialize_tavily_search_tool()]  # Pass the tool directly
)

writing_agent = Agent(
    model='gemini-2.0-flash',
    name='writing_agent',
    description="Agent for writing a trip summary after planning.",
    instruction=prompts.WRITING_AGENT,
    tools=[rag_search]  # Assuming this tool helps summarize the trip
)

# Initialize the tools for SequentialAgent (pass them directly)
travel_recommendation_tool = travel_recommendation_agent.tools[0]  # Direct tool, not wrapped
planning_tool = planning_agent.tools[0]  # Direct tool, not wrapped
writing_tool = writing_agent.tools[0]  # Direct tool

# Initialize the Sequential Agent
trip_planning_agent = SequentialAgent(
    name="trip_planner",
    description="Sequential agent to plan trips by searching, planning, and summarizing.",
    tools=[travel_recommendation_tool, planning_tool, writing_tool]  # Pass the tools directly
)

# Log initialization details to ensure the tools are being passed correctly
print(f"Initialized Sequential Agent with tools: {trip_planning_agent.tools}")


flight_offers_tool = AgentTool(agent=flight_offers_agent)
hotel_offers_tool = AgentTool(agent=hotel_offers_agent)
airport_transfer_tool = AgentTool(agent=airport_transfer_agent)
faq_tool = AgentTool(agent=faq_agent)


root_agent = Agent(
    model='gemini-2.5-flash',
    name='customer_support_agent',
    description="Friendly AI Agent that answers customer's questions about SIM Travels services, including flights, hotels, airport transfers, and general FAQs.",
    instruction=prompts.CUSTOMER_SUPPORT_ROUTER,
    tools=[
        flight_offers_tool,
        hotel_offers_tool,
        airport_transfer_tool,
        faq_tool,
        travel_recommendation_agent
    ],
)
