import os
import sys
import logging
import json
import mysql.connector

from amadeus import Client, ResponseError
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Current Datetime
dt = datetime.now().strftime('%Y%m%d')

# Ensure the logs directory exists
if not os.path.exists('./logs'):
    os.makedirs('./logs')

# Set up basic logging
logging.basicConfig(
    filename=f"./logs/{dt}_flight_offers.log",
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Log INFO level onwards 
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

logger.info("Script Started @ Datetime %(date)s", {"date": dt})

# Load Environment Variables
load_dotenv()


# Get Next 7-14 Time Delta Days' Dates
def getFutureDates() -> list:

    today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    dates = []
    for i in range(7, 15):
        dates.append((today + timedelta(days=i)).strftime('%Y-%m-%d'))
    
    return dates

def getConnection():
    try:
        # Check if the environment variables are set
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')
        database = os.getenv('DB_NAME')

        if not all([host, user, password, database]):
            raise ValueError("Missing required environment variables for DB connection.")

        # Create database connection
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if conn.is_connected():
            logger.info("Successfully connected to the database.")
            return conn
        else:
            raise Exception("Failed to connect to the database.")

    except mysql.connector.Error as mysql_e:
        logger.error(f"MySQL Error: {mysql_e}")
        return None
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def insert_data(cursor, data) -> None:

    n_count = len(data)
    for offer in data:
        try:
            segment = offer["itineraries"][0]["segments"][0]
            departure = segment["departure"]
            arrival = segment["arrival"]
            checked_bags = offer["travelerPricings"][0]["fareDetailsBySegment"][0].get("includedCheckedBags", {})
            included_checked_bags = checked_bags.get("quantity", 0)
            included_checked_bags_only = included_checked_bags > 0

            row = (
                offer["source"],
                departure["iataCode"],
                departure["at"].replace("T", " "),
                arrival["iataCode"],
                arrival["at"].replace("T", " "),
                str(offer.get("numberOfBookableSeats", "0")),
                segment["carrierCode"],
                f"{segment['carrierCode']} {segment['number']}",
                offer["itineraries"][0]["duration"],
                len(offer["itineraries"][0]["segments"]) - 1,
                offer["price"]["currency"],
                float(offer["price"]["total"]),
                offer["pricingOptions"]["fareType"][0],
                included_checked_bags_only,
                json.dumps(offer)
            )
            
            # SQL Statement
            sql = """
                INSERT INTO flight_offers (
                    source,
                    departure_airport_iata_code,
                    departure_datetime,
                    arrival_airport_iata_code,
                    arrival_datetime,
                    num_bookable_seats,
                    carrier_code,
                    flight_number,
                    itinerary_duration,
                    number_of_stops,
                    price_currency,
                    total_price,
                    fare_type,
                    included_checked_bags_only,
                    data
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Execute Statement
            cursor.execute(sql, row)
        except Exception as e:
            n_count = n_count - 1
            logger.error("Error executing Insert Statement %s", e, exc_info=True)

        logger.info("Successfully inserted %d Records.", n_count)

def get_flight_offers(paramDates, paramData) -> None:
    
    # Warn Flag
    warnings = False

    # Instantiate Client & DB Connection
    amadeus = Client(
        client_id=os.getenv('API_KEY'),
        client_secret=os.getenv('API_SECRET')
    )
    
    # SQL Connection
    conn = getConnection()
    if (conn is None):
        logger.error(f"Unable to establish Database Connection, exiting")
        return None

    cursor = conn.cursor() # Cursor Object

    # GET Request Flight Offers
    for depDate in paramDates:
        for options in paramData:
            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=options['originLocationCode'],
                    destinationLocationCode=options['destinationLocationCode'],
                    departureDate=depDate,
                    adults=int(options['adults']),
                    currencyCode=options['currencyCode'],
                    max=10)
                data = response.data
                insert_data(cursor, data)
            except ResponseError as e:
                warnings=True
                logger.warning("Error Retrieving Flight Offer: %s", e, exc_info=True)
                logger.warning(
                    "departureDate: %(departureDate)s, "
                    "originLocationCode: %(originLocationCode)s, "
                    "destinationLocationCode: %(destinationLocationCode)s, "
                    "adults: %(adults)s, "
                    "currencyCode: %(currencyCode)s", 
                    {
                        'departureDate': depDate,
                        'originLocationCode': options['originLocationCode'],
                        'destinationLocationCode': options['destinationLocationCode'],
                        'adults': options['adults'],
                        'currencyCode': options['currencyCode']
                    }
                )
                continue
            except Exception as e:
                logger.error(f"Unexpected Error Occured: {e}")
                logger.error("Comitting and Disconnecting from DB ...")
                conn.commit()
                cursor.close()
                conn.close()
                return None

    # Close Connection
    logger.info("Comitting and Disconnecting from DB ...")
    conn.commit()
    cursor.close()
    conn.close()
    if (warnings):
        logger.warning("get_flight_offers(...) completed with warnings")
    return None

def main():

    # Load Configuration
    logger.info("Reading Configuration ...")
    config:dict = {}
    try:
        with open('flight_offers_config.json', 'r') as f:
            config = json.load(f)
        logger.info("Read Successful!")
    except Exception as e:
        logger.critical("Failed to Read Config, Exiting Program %s", e)
        sys.exit(1)

    paramDates = getFutureDates()
    paramData = config['data']

    get_flight_offers(paramDates, paramData)
    logger.info("Script Ended")

if __name__ == "__main__":
    main()