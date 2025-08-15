/*Handles Axios Library to make our own
Allow for easier handling of asynchronous operations such as requests (GET POST PUT DELETE PATCH)
Can automatically transform JSON data and parse JSON responses to JavaScript Objects
Configure requests, fine-tune how requests are made and responses are handled.
*/
import axios from 'axios';

//All request using this instance will use this baseURL
const instance = axios.create({
  baseURL: 'https://sim-travels-backend.onrender.com',
  //Allows session cookies to be included in requests, essential for session-based authentication
  withCredentials: true
});

//Export custom Axios instance to be reused across websites
export default instance;
