import os
import json
import logging
import uvicorn

from amadeus import Client, ResponseError
from dotenv import load_dotenv
from fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="TravelAssistantServer")

@mcp.tool()
def search_flight_offers(
    originLocationCode: str,
    destinationLocationCode: str,
    departureDate: str,
    adults: int,
    returnDate: str = None,
    children: int = None,
    infants: int = None,
    travelClass: str = None,
    nonStop: bool = None,
    currencyCode: str = 'SGD',
) -> str:
    """
    Search for flight offers using the Amadeus API

    Required Parameters:
        originLocationCode: city/airport IATA code from which the traveler will depart, (e.g. BOS for Boston
        destinationLocationCode: IATA code of the destination city/airport (e.g., BKK for Bangkok)
        departureDate: Departure date in ISO 8601 format (YYYY-MM-DD, e.g., 2023-05-02)
        adults: Number of adult travelers (age 12+), must be 1-9

    Optional Parameters:
        returnDate: Return date in ISO 8601 format (YYYY-MM-DD), if round-trip is desired
        children: Number of child travelers (age 2-11)
        infants: Number of infant travelers (age <= 2)
        travelClass: Travel class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)
        nonStop: If true, only non-stop flights are returned
        currencyCode: ISO 4217 currency code (e.g., EUR for Euro)

    Returns:
        JSON String containing flight offers
    """
    if adults and not (1 <= adults <= 9):
        return json.dumps({"error": "Adults must be between 1 and 9"})

    if children and infants and adults and (adults + children > 9):
        return json.dumps({"error": "Total number of seated travelers (adults + children) cannot exceed 9"})

    if infants and adults and (infants > adults):
        return json.dumps({"error": "Number of infants cannot exceed number of adults"})

    amadeus_client = Client(client_id=os.getenv('API_KEY'), client_secret=os.getenv('API_SECRET'))
    params = {}

    # Required Parameters
    params["originLocationCode"] = originLocationCode
    params["destinationLocationCode"] = destinationLocationCode
    params["departureDate"] = departureDate
    params["adults"] = adults

    # Optional Parameters
    if returnDate is not None:
        params["returnDate"] = returnDate

    if children is not None:
        params["children"] = children

    if infants is not None:
        params["infants"] = infants

    if travelClass is not None:
        params["travelClass"] = travelClass

    if nonStop is not None:
        params["nonStop"] = nonStop

    params["currencyCode"] = currencyCode
    params["max"] = 10

    try:
        response = amadeus_client.shopping.flight_offers_search.get(**params)
        return json.dumps(response.body)
    except ResponseError as error:
        error_msg = f"Amadeus API error: {str(error)}"
        return json.dumps({"error": error_msg})
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        return json.dumps({"error": error_msg})

# Main Server
if __name__ == "__main__":
    load_dotenv()
    http_app = mcp.http_app()
    uvicorn.run(http_app, host="0.0.0.0", port=7000)