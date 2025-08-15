//Handles booking-related routes
//Import Express library - Web App Framework for NodeJS, Handles Routing Mechanism (GET, POST, PUT, DELETE) - Handles API Request
//Import database connection from db.js
import express from 'express';
import db from '../db.js';

//Creates a new Express router to define the endpoints
const router = express.Router();

//POST /api/bookings/
router.post('/', (req, res) => {
  //Check if user is logged in (Session must exist)
  if (!req.session.user) {
    return res.status(401).json({ message: 'Unauthorized: Please log in.' });
  }

  //Get logged-in user ID
  const userId = req.session.user.id;
  //Object destructuring, extract properties and assign them to variables
  const { id: flightId, from, to, date, time, duration } = req.body;

  //Validation to ensure all flight fields are present
  if (!flightId || !from || !to || !date || !time || !duration) {
    return res.status(400).json({ message: 'Missing flight data.' });
  }

  //SQL Query to insert the booking into the Database
  const insertQuery = `
    INSERT INTO flight_bookings 
    (user_id, flight_id, flight_from, flight_to, date, time, duration)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `;

  //Execute the Query with the provided values
  db.query(insertQuery, [userId, flightId, from, to, date, time, duration], (err, result) => {
    if (err) {
      //Prompts error if missing values
      console.error('Booking error:', err);
      return res.status(500).json({ message: 'Failed to book flight.' });
    }

    //Else, successfully inserted values into DB
    res.status(200).json({ message: 'Flight booked successfully.' });
  });
});

// GET /api/bookings/
router.get('/', (req, res) => {
  //Check if user is logged in (Session must exist)
  if (!req.session.user) {
    return res.status(401).json({ message: 'Unauthorized' });
  }

  //Gets user's ID from session 
  const userId = req.session.user.id;

  //SQL Query
  const selectQuery = `
    SELECT flight_id, flight_from, flight_to, date, time, duration
    FROM flight_bookings
    WHERE user_id = ?
    ORDER BY date, time
  `;

  //Query fetch the flight details 
  db.query(selectQuery, [userId], (err, results) => {
    if (err) {
      console.error('Error fetching bookings:', err);
      return res.status(500).json({ message: 'Failed to fetch bookings' });
    }
    //Then sends to the frontend
    res.status(200).json(results);
  });
});

//Export router to be used in server.js
export default router;
