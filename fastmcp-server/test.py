import os
import re
import logging
import requests
from dotenv import load_dotenv
import json
import pprint
from amadeus import Client, ResponseError

load_dotenv()

logger = logging.basicConfig(level=logging.DEBUG, filename="server.log", filemode="a")

def search_flight_offers(
    originLocationCode,
    destinationLocationCode,
    departureDate,
    adults,
    returnDate,
    children,
    infants,
    travelClass,
    nonStop,
    currencyCode
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

    if returnDate is not None:
        params["max"] = 6
    else:
        params["max"] = 3

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


def get_full_address(address:str, type_of_address:str) -> dict:
    
    # Trim Excess Whitecases and Special Characters (except Commas)
    search_address = re.sub(pattern="/[^.a-zA-Z0-9]/g", repl="", string=address)
    search_address = re.sub(pattern="\s+", repl=" ", string=search_address)
    search_address = search_address.replace(" ", "%20")

    # Initialize Variables
    street_number = None
    endAddressLine = None
    endCityName = None
    endZipCode = None
    endCountryCode = None
    endGeoCode = None

    logging.info(f"[Search Address]: {search_address}")
    API_REQUEST = f'https://maps.googleapis.com/maps/api/geocode/json?address={search_address}&key={os.getenv("GEOLOCATION_API_KEY")}'
    response = requests.get(API_REQUEST)
    data = response.json()
    logging.info(f"Response Status Code: {response.status_code}") 
    if response.status_code == 200:
        if data['status'] != "OK":
            logging.error(f"Error retrieving address via Geocoding API: [{data['status']}]")
            return {"status":"error", "results": f"Unable to retrieve {type_of_address} address"}
        
        logging.info(f"[Search Success]: Extracting JSON Data")
        logging.info(data)
        address_components = data['results'][0]['address_components']
        for component in address_components:
            
            if 'street_address' in component['types']:
                endAddressLine = component['long_name']

            if 'street_number' in component['types']:
                street_number = component['long_name']
            
            if 'route' in component['types']:
                if street_number is not None:
                    endAddressLine = f'{street_number} {component["long_name"]}'
                else:
                    endAddressLine = component["long_name"]

            # Attempt to Get CityName via locality, Else via administrative_area_level
            if 'locality' in component['types']:
                endCityName = component['long_name']
            for i in range(1, 7): 
                area_lvl = f'administrative_area_level_{i}'
                if (area_lvl in component['types']) and (endCityName is None):
                    endCityName = component['long_name']
                    break
                elif endCityName is not None:
                    break
            
            if 'postal_code' in component['types']:
                endZipCode = component['long_name']
            if 'country' in component['types']:
                endCountryCode = component['short_name']

        if 'geometry' in data['results'][0].keys():
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            endGeoCode = f"{lat},{lng}"

        # Last Resort Address Line is None
        logging.warning("Unable to form an address line, using formatted address instead")
        if endAddressLine is None:
            if 'formatted_address' in data['results'][0].keys():
                endAddressLine = data['results'][0]['formatted_address']

        if type_of_address == "start":
            results = {
                "startAddressLine": endAddressLine,
                "startCityName": endCityName,
                "startZipCode": endZipCode,
                "startCountryCode": endCountryCode,
                "startGeoCode": endGeoCode
            }
        else:
            results = {
                "endAddressLine": endAddressLine,
                "endCityName": endCityName,
                "endZipCode": endZipCode,
                "endCountryCode": endCountryCode,
                "endGeoCode": endGeoCode    
            }

        for _, value in results.items():
            if value is None:
                logging.error(f"Unable to form complete address, {json.dumps(results, indent=4)}")
                return {
                    "status":"error",
                    "results": f"Unable to form complete {type_of_address} address\n{json.dumps(results, indent=4)}"
                }
        
        return {"status":"success", "results": json.dumps(results, indent=4)}
    else:
        logging.error(f"Geocoding API Request Error {response.status_code}")
        return {"status":"error", "results": f"Unable to retrieve {type_of_address} address"}

def search_airport_transfers(
    startAddress:str,
    endAddress:str,
    startDatetime:str, # [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) YYYY-MM-DDThh:mm:ss
    num_of_passengers:int
) -> str:
    
    if num_of_passengers and not (1 <= num_of_passengers <= 9):
        return {"error": "Number of passengers must be between 1 and 9"}

    # Search Addresses
    startAddress = get_full_address(address=startAddress, type_of_address="start")
    endAddress = get_full_address(address=endAddress, type_of_address="end")

    if startAddress["status"] == "error" and endAddress["status"] == "error":
        return json.dumps({"error": "Unable to find offers, please try different addresses for starting and ending location"})
    elif startAddress["status"] == "error":
        return json.dumps({"error": "Unable to find offers, please try a different starting address."})
    elif endAddress["status"] == "error":
        return json.dumps({"error": "Unable to find offers, please try a different ending address."})

    # Load Data
    startAddress = json.loads(startAddress["results"])
    endAddress = json.loads(endAddress["results"])

    params = {
        "startDateTime": startDatetime,
        "passengers": num_of_passengers,
        "transferType": "PRIVATE",
        "currency": "SGD"
    }

    for key, val in startAddress.items():
        params[key] = val
    for key, val in endAddress.items():
        params[key] = val

    logging.info("Searching Params:")
    logging.info(params)
    # Search Airport Transfer
    amadeus_client = Client(client_id=os.getenv('API_KEY'), client_secret=os.getenv('API_SECRET'))
    try:
        response = amadeus_client.shopping.transfer_offers.post(params)
        response_json = json.loads(response.body)
        logging.info("Successful response from Amadeus API")
        logging.info(response_json)
        if "errors" in response_json.keys():
            logging.error(json.dumps({"error": json.dumps(response_json)}))
            return({"error": "Unable to retieve transfer offers, please try again later."})
        else:
            logging.info("Successfully retrieved transfer offers")
            return json.dumps({"success": json.dumps(response_json)})
        
    except ResponseError as error:
        logging.error(f"Amadeus API error: {str(error)}")
        return json.dumps({"error": "Unable to retieve transfer offers, please try again later."})
    except Exception as e:
        logging.error(f"Unknown Exception has occured: {str(error)}")
        return json.dumps({"error": "Unable to retieve transfer offers, please try again later."})

if __name__ == "__main__":
    data = search_flight_offers(originLocationCode='SYD', destinationLocationCode='TYO', departureDate='2025-08-15', adults=1, returnDate=None, children=None, infants=None, travelClass=None, nonStop=True, currencyCode='SGD')
    pprint.pp(data)

# if __name__ == "__main__":
#     test_cases = [
#         {"startAddress": "KLIA", "endAddress": "MPalace Hotel KL", "startDatetime": "2025-08-12T10:00:00", "num_of_passengers": 2},
#         {"startAddress": "paris airport", "endAddress": "ibis hotel cdg", "startDatetime": "2025-08-14T15:00:00", "num_of_passengers": 1},
#         {"startAddress": "london kengsinton gardens hotel", "endAddress": "baywaters station", "startDatetime": "2025-08-21T08:30:00", "num_of_passengers": 4},
#         {"startAddress": "mbs hotel singapore", "endAddress": "changi airport", "startDatetime": "2025-08-16T08:30:00", "num_of_passengers": 2},
#         {"startAddress": "JFK Airport new york", "endAddress": "jfk plaza hotel", "startDatetime": "2025-08-15T10:30:00", "num_of_passengers": 1},
#     ]
 
#     logging.info("[Running Test Cases]")
#     for i, case in enumerate(test_cases, 1):
#         logging.info(f"--- Running Test Case {i}: {case['startAddress']} to {case['endAddress']} ---")
#         try:
#             results = search_airport_transfers(**case)
#             logging.info(f"--- Result for Test Case {i} ---")
#             try:
#                 # Pretty print if it's JSON
#                 parsed_results = json.loads(results)
#                 logging.info(json.dumps(parsed_results, indent=4, sort_keys=True))
#             except (json.JSONDecodeError, TypeError):
#                 # Log as-is if not valid JSON
#                 logging.info(results)
#             pprint.pp(str(results)[0:100])
#         except Exception as e:
#             logging.error(f"Test case {i} failed during execution: {e}")
#         logging.info("-" * 20)