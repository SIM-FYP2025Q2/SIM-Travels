//Handles HTTP requests related to user registration
//Import Axios HTTP Client to make API Requests, (Handle asynchronous operations) [GET POST PUT DELETE PATCH requests]
import axios from 'axios';

//Base URL of backend user related routes, using all the backend files
const API_URL = 'https://sim-travels-backend.onrender.com/api/users';

//Register function, send POST request to /register
const register = (username, password) => {
  //Sends username nad password as JSON in request body
  return axios.post(`${API_URL}/register`, { username, password });
};

//Create object with one method/property in this case the 'register' function
const AuthService = {
  register,
};

//Export service to use in component pages (RegisterPage.jsx)
export default AuthService;
