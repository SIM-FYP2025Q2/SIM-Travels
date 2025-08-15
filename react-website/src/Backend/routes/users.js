//Handles user-related routes (Register, Login, Logout and Session Check)
//Import Express library - Web App Framework for NodeJS, Handles Routing Mechanism (GET, POST, PUT, DELETE) - Handles API Request
//Import database connection from db.js
import express from 'express';
import db from '../db.js';

//Creates a new Express router to define the endpoints
const router = express.Router();

//Register function
//Destructure the user input from request
router.post('/register', (req, res) => {
  const { username, password } = req.body;

  //Validation check for user registration
  if (!username || !password) {
    return res.status(400).send('Missing username or password');
  }

  //SQL Query to insert the new user into 'users' table
  const insertUserQuery = 'INSERT INTO users (username, password) VALUES (?, ?)';

  //Execute the query using the parameters
  db.query(insertUserQuery, [username, password], (err, result) => {
    if (err) {
      console.error('Database error:', err);

      //Error handling for duplicate entry (MySQL error code)
      if (err.code === 'ER_DUP_ENTRY') {
        return res.status(409).send('Username already exists. Please use another');
      }

      //General database errors
      return res.status(500).send('Server error');
    }

    //If no error, registers new user
    console.log('New user registered:', username);
    return res.status(201).send('User registered successfully');
  });
});

//Login function
router.post('/login', (req, res) => {
  const { username, password } = req.body;
  //SQL Query to find matching user with both username and password
  const query = 'SELECT id, username FROM users WHERE username = ? AND password = ?';

  //DB Error, usually connection issue, invalid parameters, database constraints
  db.query(query, [username, password], (err, results) => {
    if (err) return res.status(500).send('Server error');

    //If no user matches or password invalid
    if (results.length === 0) {
      return res.status(401).send('Invalid credentials');
    }

    //Extract the user info
    const user = results[0];

    //Save the user info to session (Using session to persist across all request)
    req.session.user = {
      id: user.id,
      username: user.username,
      sessionID: req.sessionID
    };

    //Return session info to the frontend portion
    return res.json({
      success: true,
      id: user.id,
      username: user.username,
      sessionID: req.sessionID
    });
  });
});

//Get session info
router.get('/session', (req, res) => {
  //In the event if user tries to book flights etc.. and not logged in, the system will alert the user they are not logged in
  if (!req.session.user) return res.status(401).send('Not logged in');

  //Otherwise if logged in, return session details
  res.json(req.session.user);
});

//Logout function
router.post('/logout', (req, res) => {
  //After logout, destroys the session
  req.session.destroy((err) => {
    if (err) return res.status(500).send('Logout failed');
    //Clears the session cookies 
    res.clearCookie('connect.sid');
    res.json({ success: true });
  });
});

//For debugging to check if db connected
router.get('/', (req, res) => {
  db.query('SELECT * FROM users', (err, results) => {
    if (err) return res.status(500).send('Database error');
    res.json(results);
  });
});

//Export this router to be used in server.js file
export default router;
