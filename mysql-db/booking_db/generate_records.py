

import json
import pprint
import random

import mysql.connector
from faker import Faker

fake = Faker()

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="User123",
    password="Password123",
    database="Database Name"
)
cursor = conn.cursor()

# Booking types
booking_types = ['Flight', 'Hotel', 'Airport Transfer']
flight_types = ['One-Way', 'Two-Way']

for _ in range(100):
    user_id = random.randint(1, 9999)
    first_name = fake.first_name()
    last_name = fake.last_name()
    full_name = f"{first_name} {last_name}"

    booking_id = fake.uuid4()[:8]
    booking_type = random.choice(booking_types)

    # Create JSON details based on type
    if booking_type == 'Flight':
        details = {
            "type": "Flight",
            "flight_type": random.choice(flight_types),
            "from": fake.city(),
            "to": fake.city(),
            "departure": fake.date_time_this_year().isoformat(),
            "return": fake.date_time_this_year().isoformat() if flight_types == "Two-Way" else None
        }
    elif booking_type == 'Hotel':
        details = {
            "type": "Hotel",
            "hotel_name": fake.company() + " Hotel",
            "check_in": fake.date_this_year().isoformat(),
            "check_out": fake.date_this_year().isoformat(),
            "city": fake.city()
        }
    else:  # Airport Transfer
        details = {
            "type": "Airport Transfer",
            "pickup_location": fake.address(),
            "dropoff_location": fake.address(),
            "pickup_time": fake.date_time_this_year().isoformat()
        }

    # Insert into database
    record = {user_id, full_name, last_name, booking_id, booking_type, json.dumps(details)}
    pprint.pp(f"Inserted: {record}")
    cursor.execute("""
        INSERT INTO bookings (user_id, full_name, last_name, booking_id, booking_type, booking_details)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, full_name, last_name, booking_id, booking_type, json.dumps(details)))

conn.commit()
cursor.close()
conn.close()

print("Successfully inserted 100 fake records inserted.")
