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