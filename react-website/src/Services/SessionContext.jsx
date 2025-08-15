//File that uses React Context API to manage current logged-in user session across whole app.
//import React tools for context creation and handling state/lifecycle
import { createContext, useContext, useState, useEffect } from 'react';
//Import axios to fetch session info on page load
import axios from 'axios';

//Create context object (Global state container)
const SessionContext = createContext();

//Custom hook so components can easily access session data like: const { user } = useSession();
export const useSession = () => useContext(SessionContext);

//Manage user session state
export const SessionProvider = ({ children }) => {
  const [user, setUser] = useState(null);       //Hold current logged-in user (null if logged out)
  const [loading, setLoading] = useState(true); //Prevents app from loading before session check complete

  //Check session on load
  //Asks backend if session exist in browser, "withCredentials" = ensure browser includes session cookies
  useEffect(() => {
  axios.get('/api/users/session', { withCredentials: true })
    .then(res => {
      //Save session to local state
      console.log('Session loaded from server:', res.data);  
      setUser(res.data);
    })
    //Else no valid session, user stays logged out
    .catch((err) => {
      console.log('Failed to load session:', err);  
      setUser(null);
    })
    //Whether session success or fail, done loading
    .finally(() => setLoading(false));
}, []);

  //Debugging, checks current user whenever session changes
  useEffect(() => {
  console.log('Session loaded from server: ', user);
}, [user]);

  //Prevents rendering of app components until we know if user is logged in or not
  if (loading) return null; 

  //Provide user data to the whole application
  return (
    <SessionContext.Provider value={{ user, setUser }}>
      {children}
    </SessionContext.Provider>
  );
};
