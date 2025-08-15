//Starts and configures backend server
import express from 'express';                                    //Import Express library - Web App Framework for NodeJS, Handles Routing Mechanism (GET, POST, PUT, DELETE) - Handles API Request
import cors from 'cors';                                          //Cross Origin Resource Sharing - Middleware to enable or restrict resources, (E.g. allow request from specific origins) Allow Frontend/Backend communication
import dotenv from 'dotenv';                                      //Use to load environment variables from .env file, for configuration settings, database connection etc
import session from 'express-session';                            //Manage Sessions in Express apps, store user session data on server side => Maintain user state across multiple requests (Usage; Authentication)
import userRoutes from './routes/users.js';                       //Import users.js file
import flightBookingRoutes from './routes/flightBookings.js';     //Import flightBookings.js file
import db from './db.js';                                         //Import db.js file for local testing

//Load .env variables into process.env
dotenv.config();
//Create instance of Express, constant for usage throughout code
const app = express();

//Allow cross-origin requests from deployed frontend (Render.com)
app.use(cors({
  origin: 'https://sim-travels-deployment.onrender.com',
  //Allow cookies and headers
  credentials: true
}));
//Parse JSON bodies
app.use(express.json());

app.use(session({
  secret: 'supersecretkey',   //Key used to sign the session ID cookie ; prevent tempering of data
  resave: false,              //Don't save session if nothing changed. False = save session if modified, true = save session on every request 
  saveUninitialized: false,   //Don't save empty/unmodified sessions. (GDPR Compliance), True = save all sessions, even empty session. *Ensure not storing personal data/session identifiers for users*
  cookie: { secure: false }   //True = sends cookies over HTTPS (Essential for deployment/production) / Prevent session hijacking and MITM, False = sends cookies over HTTP (For local deployment)
}));

//Routes accordingly 
app.use('/api/users', userRoutes);
app.use('/api/bookings', flightBookingRoutes);

//Debugging to test if server is running
app.get('/', (req, res) => {
  res.send('Backend server is running');
});

//Starting server
const PORT = process.env.SERVER_PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
