import os
import json
import logging
import re
import requests

# Get Logger
logger = logging.getLogger(__name__)


def truncate_address(address):
    if len(address) > 80:
        # Find the last comma or space within the limit
        last_comma = address.rfind(',', 0, 80)
        if last_comma != -1:
            truncated = address[:last_comma]
        else:
            # Fallback to simple slicing if no comma is found
            truncated = address[:80]

        return truncated
    else:
        return address


def get_geocode(address) -> dict:
    """
    Get the geocode (latitude and longitude) of an address using the Google Geocoding API

    Required Parameters:
        address: The address to geocode

    Returns:
        A dictionary containing the status and results of the geocoding request
    """
    logging.info("---- [get_geocode] ----")
    logging.info(f"Input address: {address}")

    # Trim Excess Whitecases and Special Characters (except Commas)
    search_address = re.sub(pattern="/[^.a-zA-Z0-9]/g", repl="", string=address)
    search_address = re.sub(pattern="\s+", repl=" ", string=search_address)
    search_address = search_address.replace(" ", "%20")

    logging.info(f"Sanitized search address: {search_address}")
    API_REQUEST = f'https://maps.googleapis.com/maps/api/geocode/json?address={search_address}&key={os.getenv("GEOLOCATION_API_KEY")}'
    logging.info(f"Google Geocoding API request: {API_REQUEST}")
    
    response = requests.get(API_REQUEST)
    data = response.json()
    
    logging.info(f"Google Geocoding API response status code: {response.status_code}")
    logging.debug(f"Google Geocoding API response data: {json.dumps(data, indent=4)}")

    if response.status_code == 200:
        if data['status'] != "OK":
            logging.error(f"Error retrieving address via Geocoding API: [{data['status']}]")
            logging.info("---- [end_get_geocode] ----")
            return {"status": "error", "results": f"Unable to retrieve address"}

        logging.info("Successfully retrieved geocode from Google Geocoding API.")
        if 'geometry' in data['results'][0].keys():
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            result = {
                "status": "success",
                "results": {
                    "lat": lat,
                    "lng": lng
                }
            }
            logging.info(f"Extracted geocode: lat={lat}, lng={lng}")
            logging.info("---- [end_get_geocode] ----")
            return result
        else:
            logging.error("Could not find 'geometry' in Geocoding API response.")
            logging.info("---- [end_get_geocode] ----")
            return {"status": "error", "results": f"Unable to retrieve address"}
    else:
        logging.error(f"Geocoding API Request Error {response.status_code}")
        logging.info("---- [end_get_geocode] ----")
        return {"status": "error", "results": f"Unable to retrieve address"}

def reverse_search_postcode(lat, lng):
    logging.info("---- [reverse_search_postcode] ----")
    logging.info(f"Input: lat={lat}, lng={lng}")
    API_REQUEST = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&result_type=postal_code&key={os.getenv("GEOLOCATION_API_KEY")}'
    response = requests.get(API_REQUEST)
    data = response.json()
    
    logging.info(f"Google Geocoding API response status code: {response.status_code}")
    logging.debug(f"Google Geocoding API response data: {json.dumps(data, indent=4)}")

    if response.status_code == 200:
        if data['status'] != "OK":
            logging.error(f"Error retrieving address via Geocoding API: [{data['status']}]")
            logging.info("---- [end_reverse_search_postcode] ----")
            return None

        logging.info("Successfully retrieved postcode details from Google Geocoding API.")
        address_components = data['results'][0]['address_components']
        logging.debug(f"Address components: {json.dumps(address_components, indent=4)}")

        for component in address_components:
            if 'postal_code' in component['types']:
                logging.info("Successfully found postcode details from Google Geocoding API.")
                return component['long_name']
    else:
        logging.error(f"Geocoding API Request Error {response.status_code}")
        logging.info("---- [end_reverse_search_postcode] ----")
        return None

def get_full_address(address, type_of_address) -> dict:
    """
    Get the full address details of a location using the Google Geocoding API

    Required Parameters:
        address: The address to get full details for
        type_of_address: The type of address (start or end)

    Returns:
        A dictionary containing the status and results of the geocoding request
    """
    logging.info("---- [get_full_address] ----")
    logging.info(f"Input address: {address}, type_of_address: {type_of_address}")

    # Trim Excess Whitecases and Special Characters (except Commas)
    search_address = re.sub(pattern="/[^.a-zA-Z0-9]/g", repl="", string=address)
    search_address = re.sub(pattern="\s+", repl=" ", string=search_address)
    search_address = search_address.replace(" ", "%20")

    logging.info(f"Sanitized search address: {search_address}")

    # Initialize Variables
    street_number = None
    endAddressLine = None
    endCityName = None
    endZipCode = None
    endCountryCode = None
    endGeoCode = None

    API_REQUEST = f'https://maps.googleapis.com/maps/api/geocode/json?address={search_address}&key={os.getenv("GEOLOCATION_API_KEY")}'
    logging.info(f"Google Geocoding API request: {API_REQUEST}")
    
    response = requests.get(API_REQUEST)
    data = response.json()
    
    logging.info(f"Google Geocoding API response status code: {response.status_code}")
    logging.debug(f"Google Geocoding API response data: {json.dumps(data, indent=4)}")

    if response.status_code == 200:
        if data['status'] != "OK":
            logging.error(f"Error retrieving address via Geocoding API: [{data['status']}]")
            logging.info("---- [end_get_full_address] ----")
            return {"status": "error", "results": f"Unable to retrieve {type_of_address} address"}

        logging.info("Successfully retrieved address details from Google Geocoding API.")
        address_components = data['results'][0]['address_components']
        logging.debug(f"Address components: {json.dumps(address_components, indent=4)}")

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

            if 'sublocality' in component['types'] and endAddressLine is not None:
                if street_number is not None:
                    endAddressLine = f'{street_number} {component["long_name"]}'
            
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

        if endAddressLine is None:
            if 'formatted_address' in data['results'][0].keys():
                endAddressLine = data['results'][0]['formatted_address']

        if type_of_address == "start":
            results = {
                "startAddressLine": truncate_address(endAddressLine),
                "startCityName": endCityName,
                "startZipCode": endZipCode,
                "startCountryCode": endCountryCode,
                "startGeoCode": endGeoCode
            }
        else:
            results = {
                "endAddressLine": truncate_address(endAddressLine),
                "endCityName": endCityName,
                "endZipCode": endZipCode,
                "endCountryCode": endCountryCode,
                "endGeoCode": endGeoCode
            }
        
        logging.info(f"Extracted address details: {json.dumps(results, indent=4)}")

        for key, value in results.items():
            if value is None:
                logging.error(f"Unable to form complete address, missing {key}. Full results: {json.dumps(results, indent=4)}")

                if (key == "startZipCode"):
                    logging.info("Reverse searching postcode...")
                    lat, lng = results["startGeoCode"].split(",")
                    results[key] = reverse_search_postcode(lat, lng)
                    
                    if results[key] is None:
                        return {"status": "error", "results": f"Unable to form complete {type_of_address} address"}
                elif (key == "endZipCode"):
                    logging.info("Reverse searching postcode...")
                    lat, lng = results["endGeoCode"].split(",")
                    results[key] = reverse_search_postcode(lat, lng)

                    if results[key] is None:
                        return {"status": "error", "results": f"Unable to form complete {type_of_address} address"}
                else:
                    logging.info("---- [end_get_full_address] ----")
                    return {"status": "error", "results": f"Unable to form complete {type_of_address} address"}

        logging.info("Successfully formed complete address.")
        logging.info("---- [end_get_full_address] ----")
        return {"status": "success", "results": json.dumps(results, indent=4)}
    else:
        logging.error(f"Geocoding API Request Error {response.status_code}")
        logging.info("---- [end_get_full_address] ----")
        return {"status": "error", "results": f"Unable to retrieve {type_of_address} address"}
