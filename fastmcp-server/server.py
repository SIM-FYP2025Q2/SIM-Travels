import os
import json
import logging
from typing import Annotated

import uvicorn
from amadeus import Client, ResponseError
from dotenv import load_dotenv
from fastmcp import FastMCP

from tools import get_geocode, get_full_address

logger = logging.basicConfig(level=logging.DEBUG, filename="server.log", filemode="a")
mcp = FastMCP(name="TravelAssistantServer")


@mcp.tool()
def search_flight_offers(
    originLocationCode: Annotated[str, "City/airport IATA code from which the traveler will depart, (e.g. BOS for Boston)"],
    destinationLocationCode: Annotated[str, "IATA code of the destination city/airport (e.g., BKK for Bangkok)"],
    departureDate: Annotated[str, "Departure date in ISO 8601 format (YYYY-MM-DD, e.g., 2023-05-02)"],
    adults: Annotated[int, "Number of adult travelers (age 12+), must be 1-9", {"ge": 1, "le": 9}],
    returnDate: Annotated[str, "Return date in ISO 8601 format (YYYY-MM-DD), if round-trip is desired"] = None,
    children: Annotated[int, "Number of child travelers (age 2-11)"] = None,
    infants: Annotated[int, "Number of infant travelers (age <= 2)"] = None,
    travelClass: Annotated[str, "Travel class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)"] = None,
    nonStop: Annotated[bool, "If true, only non-stop flights are returned"] = None,
    currencyCode: Annotated[str, "ISO 4217 currency code (e.g., EUR for Euro)"] = 'SGD'
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
    logging.info("---- [search_flight_offers] ----")
    logging.info(f"Input parameters: originLocationCode={originLocationCode}, destinationLocationCode={destinationLocationCode}, departureDate={departureDate}, adults={adults}, returnDate={returnDate}, children={children}, infants={infants}, travelClass={travelClass}, nonStop={nonStop}, currencyCode={currencyCode}")

    if adults and not (1 <= adults <= 9):
        logging.error("Invalid number of adults.")
        return json.dumps({"error": "Adults must be between 1 and 9"})

    if children and infants and adults and (adults + children > 9):
        logging.error("Total number of seated travelers exceeds 9.")
        return json.dumps({"error": "Total number of seated travelers (adults + children) cannot exceed 9"})

    if infants and adults and (infants > adults):
        logging.error("Number of infants exceeds number of adults.")
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

    # Non Stop Preference (default: False)
    if (nonStop is not None):
        if nonStop is True:
            params["nonStop"] = "true"

    params["currencyCode"] = currencyCode

    # Return more offers is 'returnDate' is provided
    if returnDate is not None:
        params["max"] = 6
    else:
        params["max"] = 3

    # Search Flight Offers
    logging.info(f"Constructed Amadeus API params: {json.dumps(params, indent=4)}")
    try:
        response = amadeus_client.shopping.flight_offers_search.get(**params)
        logging.info("Successfully received flight offers from Amadeus API.")
        logging.debug(f"Amadeus API response body: {response.body}")
        logging.info("---- [end_search_flight_offers] ----")
        return json.dumps(response.body)
    except ResponseError as error:
        logging.error(f"Amadeus API error: {str(error)}")
        logging.info("---- [end_search_flight_offers] ----")
        return json.dumps({"error": "No flight offers found, please try a different route or date."})
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        logging.info("---- [end_search_flight_offers] ----")
        return json.dumps({"error": "No flight offers found, please try a different route or date."})


@mcp.tool()
def search_hotel_offers(
    cityCode: Annotated[str, "City IATA code (e.g., BOS for Boston)"],
    checkInDate: Annotated[str, "Check In Date in ISO 8601 format (YYYY-MM-DD, e.g., 2023-05-02)"],
    checkOutDate: Annotated[str, "Check Out Date in ISO 8601 format (YYYY-MM-DD, e.g., 2023-05-02), must be greater than check-in date"],
    occupants: Annotated[int, "Number of travelers staying, must be 1-9", {"ge": 1, "le": 9}] = 1,
    roomQuantity: Annotated[int, "Number of rooms, must be 1-9", {"ge": 1, "le": 9}] = 1,
    address: Annotated[str, "Address/Name of the Place, optional"]= None,
    currencyCode: Annotated[str, "ISO 4217 currency code (e.g., EUR for Euro)"] = None
) -> str:
    """
    Search for hotel offers using the Amadeus API

    Required Parameters:
        cityCode: City IATA code (e.g., BOS for Boston)
        checkInDate: Check In Date in ISO 8601 format (YYYY-MM-DD, e.g., 2023-05-02)
        checkOutDate: Check Out Date in ISO 8601 format (YYYY-MM-DD, e.g., 2023-05-02), must be greater than check-in date
        occupants: Number of occupants, must be 1-9

    Optional Parameters:
        address: Address/Name of the Place, optional but improves search hit rate
        roomQuantity: Number of rooms, must be 1-9
        currencyCode: ISO 4217 currency code (e.g., EUR for Euro)

    Returns:
        dict: A JSON dict containing the list of hotels found, or an error message.
    """
    logging.info("---- [search_hotel_offers] ----")
    logging.info(f"Input parameters: cityCode={cityCode}, address={address}, checkInDate={checkInDate}, checkOutDate={checkOutDate}, adults={occupants}, roomQuantity={roomQuantity}, currencyCode={currencyCode}")

    amadeus_client = Client(client_id=os.getenv('API_KEY'), client_secret=os.getenv('API_SECRET'))

    if occupants and not (1 <= occupants <= 9):
        logging.error("Invalid number of adults.")
        return json.dumps({"error": "Adults must be between 1 and 9"})

    if roomQuantity and not (1 <= roomQuantity <= 9):
        logging.error("Invalid room quantity.")
        return json.dumps({"error": "Room Quantity must be between 1 and 9"})

    # Room Quantity should not be greater than number of adults
    if roomQuantity > occupants:
        roomQuantity = occupants

    # Search Hotels by Geo Code Address
    api_call_success = False
    response = None
    logging.info(f"Attempting to find hotels by address: {address}")
    try:
        geocode_dict = get_geocode(address)
        if geocode_dict["status"] == "error":
            logging.error("Failed to get geocode for address.")
        else:
            lat = geocode_dict["results"]["lat"]
            lng = geocode_dict["results"]["lng"]
            logging.info(f"Geocode found: lat={lat}, lng={lng}. Attempting to find hotels by geocode.")
            response = amadeus_client.reference_data.locations.hotels.by_geocode(
                longitude=lng,
                latitude=lat
            )
            logging.debug(f"Amadeus API response (by_geocode): {response.data}")
            if response.data:
                api_call_success = True
                logging.info("Successfully found hotels by geocode.")

    except ResponseError as error:
        logging.warning(f"Amadeus API error (by_geocode): {str(error)}")
        pass
    except Exception as e:
        logging.error(f"Unexpected error (by_geocode): {str(e)}")
        pass
    
    # If Fail, Search Hotels By City IATA Code instead
    if not api_call_success:
        logging.info(f"Could not find hotels by geocode, attempting to find by city code: {cityCode}")
        try:
            response = amadeus_client.reference_data.locations.hotels.by_city.get(cityCode=cityCode)
            logging.debug(f"Amadeus API response (by_city): {response.data}")
            if response.data:
                api_call_success = True
                logging.info("Successfully found hotels by city code.")
        except ResponseError as error:
            logging.warning(f"Amadeus API error (by_city): {str(error)}")
            pass
        except Exception as e:
            logging.error(f"Unexpected error (by_city): {str(e)}")
            pass
    
    # If Empty Reponse, Failed Response or API Fail, return an error
    # Else Retrieve Hotel IDs
    if not api_call_success or not response or not response.data:
        logging.error("No hotels found for the given location.")
        logging.info("---- [end_search_hotel_offers] ----")
        return json.dumps({"error": "No hotels found in this location, please try a different address."})
    else:
        hotel_ids = []
        count = 0
        for hotel in response.data:
            hotel_ids.append(hotel['hotelId'])
            count = count + 1
            if count == 5:
                break

        logging.info(f"Found {len(hotel_ids)} hotel(s): {hotel_ids}")

        # Create Hotel Offer Search Parameters
        params = {}
        params['hotelIds'] = hotel_ids
        params['checkInDate'] = checkInDate
        params['checkOutDate'] = checkOutDate
        params['adults'] = occupants

        if currencyCode is not None:
            params["currencyCode"] = currencyCode

        if roomQuantity is not None:
            params["roomQuantity"] = roomQuantity

        # Search for Hotel Offers
        logging.info(f"Constructed Amadeus API params for hotel offers: {json.dumps(params, indent=4)}")
        try:
            response = amadeus_client.shopping.hotel_offers_search.get(**params)
            logging.debug(f"Amadeus API response (hotel_offers): {response.body}")

            if not response.data:
                logging.warning("No hotel offers found for the given hotels.")
                logging.info("---- [end_search_hotel_offers] ----")
                return json.dumps({"error": "No Hotel Offers Found"})
            else:
                logging.info("Successfully received hotel offers from Amadeus API.")
                logging.info("---- [end_search_hotel_offers] ----")
                return json.dumps(response.body)

        except ResponseError as error:
            logging.error(f"Amadeus API error (hotel_offers): {str(error)}")
            logging.info("---- [end_search_hotel_offers] ----")
            return json.dumps({"error": "No hotels found in this location, please try a different address."})
        except Exception as e:
            logging.error(f"Unexpected error (hotel_offers): {str(e)}")
            logging.info("---- [end_search_hotel_offers] ----")
            return json.dumps({"error": "No hotels found in this location, please try a different address."})


@mcp.tool()
def search_airport_transfers(
    startAddress: Annotated[str, "The starting address for the transfer"],
    endAddress: Annotated[str, "The ending address for the transfer"],
    startDatetime: Annotated[str, "The start date and time for the transfer in ISO 8601 format (YYYY-MM-DDThh:mm:ss)"],
    num_of_passengers: Annotated[int, "The number of passengers for the transfer, must be between 1 and 9", {"ge": 1, "le": 9}],
    currency_code: Annotated[str, "ISO 4217 currency code (e.g., EUR for Euro)"] = "SGD"
) -> str:
    """
    Search for airport transfers using the Amadeus API

    Required Parameters:
        startAddress: The starting address for the transfer
        endAddress: The ending address for the transfer
        startDatetime: The start date and time for the transfer in ISO 8601 format (YYYY-MM-DDThh:mm:ss)
        num_of_passengers: The number of passengers for the transfer, must be between 1 and 9
        currency_code: ISO 4217 currency code (e.g., EUR for Euro)

    Returns:
        A JSON string containing the transfer offers or an error message
    """
    logging.info("---- [search_airport_transfers] ----")
    logging.info(f"Input parameters: startAddress={startAddress}, endAddress={endAddress}, startDatetime={startDatetime}, num_of_passengers={num_of_passengers}, currency_code={currency_code}")

    if num_of_passengers and not (1 <= num_of_passengers <= 9):
        logging.error("Invalid number of passengers.")
        return {"error": "Number of passengers must be between 1 and 9"}

    # Search Addresses
    logging.info("Getting full address for start location.")
    startAddressResult = get_full_address(address=startAddress, type_of_address="start")
    logging.info("Getting full address for end location.")
    endAddressResult = get_full_address(address=endAddress, type_of_address="end")

    # If unable to form address, return an error
    if startAddressResult["status"] == "error" and endAddressResult["status"] == "error":
        logging.error("Failed to get full address for both start and end locations.")
        logging.info("---- [end_search_airport_transfers] ----")
        return json.dumps({"error": "Unable to find offers, please try different addresses for starting and ending location"})
    elif startAddressResult["status"] == "error":
        logging.error("Failed to get full address for start location.")
        logging.info("---- [end_search_airport_transfers] ----")
        return json.dumps({"error": "Unable to find offers, please try a different starting address."})
    elif endAddressResult["status"] == "error":
        logging.error("Failed to get full address for end location.")
        logging.info("---- [end_search_airport_transfers] ----")
        return json.dumps({"error": "Unable to find offers, please try a different ending address."})

    # Load Address Data
    startAddressData = json.loads(startAddressResult["results"])
    endAddressData = json.loads(endAddressResult["results"])
    logging.info(f"Start address data: {json.dumps(startAddressData, indent=4)}")
    logging.info(f"End address data: {json.dumps(endAddressData, indent=4)}")

    params = {
        "startDateTime": startDatetime,
        "passengers": num_of_passengers,
        "transferType": "PRIVATE",
        "currency": currency_code
    }

    for key, val in startAddressData.items():
        params[key] = val
    for key, val in endAddressData.items():
        params[key] = val

    logging.info(f"Constructed Amadeus API params for airport transfers: {json.dumps(params, indent=4)}")

    # Search Airport Transfer
    amadeus_client = Client(client_id=os.getenv('API_KEY'), client_secret=os.getenv('API_SECRET'))
    try:
        response = amadeus_client.shopping.transfer_offers.post(params)
        response_json = json.loads(response.body)
        logging.info("Successful response from Amadeus API for airport transfers.")
        logging.debug(f"Amadeus API response body: {json.dumps(response_json, indent=4)}")
        
        if "errors" in response_json.keys():
            logging.error(f"Amadeus API returned errors: {json.dumps(response_json['errors'])}")
            logging.info("---- [end_search_airport_transfers] ----")
            return json.dumps({"error": "Unable to retrieve transfer offers, please try again later."})
        else:
            logging.info("Successfully retrieved transfer offers.")
            logging.info("---- [end_search_airport_transfers] ----")
            return json.dumps({"success": json.dumps(response_json)})

    except ResponseError as error:
        logging.error(f"Amadeus API error: {str(error)}")
        logging.info("---- [end_search_airport_transfers] ----")
        return json.dumps({"error": "Unable to retrieve transfer offers, please try again later."})
    except Exception as e:
        logging.error(f"Unknown Exception has occured: {str(e)}")
        logging.info("---- [end_search_airport_transfers] ----")
        return json.dumps({"error": "Unable to retrieve transfer offers, please try again later."})


# Main Server
if __name__ == "__main__":
    load_dotenv()
    http_app = mcp.http_app()
    uvicorn.run(http_app, host="0.0.0.0", port=7000)
