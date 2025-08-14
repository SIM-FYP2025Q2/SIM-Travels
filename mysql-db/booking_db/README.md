# Database (Booking)

This file provides a simple way to create and populate a MySQL database with fake booking data for SIM-Travels.

## Files

### `generate_records.py`

This script generates 100 fake booking records and inserts them into a MySQL database. It uses the `Faker` library to create realistic data for fields like names, cities, and addresses.

The script creates records for three types of bookings:
- Flights
- Hotels
- Airport Transfers

### `booking_schema.sql`

This SQL script defines the schema for the `bookings` table. It includes columns for booking details, which are stored as JSON.

```sql
DROP TABLE IF EXISTS bookings;
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    booking_id VARCHAR(20) UNIQUE NOT NULL,
    booking_type VARCHAR(50) NOT NULL,
    booking_details JSON NOT NULL
);
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip
- MySQL 8.0+ Server

### Installation

1.  **Clone the repository or download the files.**
2.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```


### Alternative: MySQL Dump

Alternatively, you can use the `bookings_mysql_dump.sql` file to create the database and populate it with sample data in one command.

```bash
mysql -u your_username -p < bookings_mysql_dump.sql
```

### Configuration

You'll need to modify the MySQL Connection to your database's actual credentials

```python
# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="User123",
    password="Password123",
    database="Database Name"
)
```

## Usage

Once the database is set up and the configuration is correct, you can run the script to populate the database:

```bash
python generate_records.py
```

The script will print the records as they are inserted and a confirmation message upon completion.
