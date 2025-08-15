//Component for AccountPage
import React, { useEffect, useState } from 'react';           //Import React tools
import { useNavigate } from 'react-router-dom';               //useNavigate for routing 
import axios from '../../Services/axios';                     //Custom axios with session support

import { useSession } from '../../Services/SessionContext';   //Get session data (user)

function AccountPage() {
  const [userInfo, setUserInfo] = useState(null);             //Hold session user info
  const [bookings, setBookings] = useState([]);               //Hold list of flight bookings
  const navigate = useNavigate();                             //Navigate hook

  const { user, setUser } = useSession(); //Used for logout

  //Fetch session user info
  useEffect(() => { 
    axios.get('/api/users/session', { withCredentials: true })
      .then(res => {
        setUserInfo(res.data);  //Save user info
        fetchBookings();        //Fetch bookings after user info is confirmed
      })
      .catch(() => navigate('/login')); //If no session, redirect to login
  }, []);

  //Fetch bookings function
  const fetchBookings = async () => {
    try {
      const res = await axios.get('/api/bookings/', { withCredentials: true });
      setBookings(res.data); //Expecting array of bookings
    } catch (err) {
      console.error('Failed to load bookings:', err);
    }
  };

  //Logout function
  const handleLogout = async () => {
    await axios.post('/api/users/logout', {}, { withCredentials: true })
    .then(() => setUser(null)); //Clears the session
    alert('You have been logged out successfully');
    navigate('/login');
  };

  //Render the user's info + table of booked flights
  return (
    <div>
      <h2>Account Page</h2>
      {userInfo ? (
        <>
          <p>Welcome {userInfo.username}</p>
          <p>Your session ID is: {userInfo.sessionID}</p>
          <p>Your User ID is: {userInfo.id}</p>

          {bookings.length > 0 ? (
            <>
              <h4 className="mt-4">Your Booked Flights</h4>
              <table className="table table-bordered">
                <thead>
                  <tr>
                    <th>From</th>
                    <th>To</th>
                    <th>Departure Date</th>
                    <th>Departure Time</th>
                    <th>Duration</th>
                  </tr>
                </thead>
                <tbody>
                  {/*Converts the raw UTC time into readable String */}
                  {bookings.map((booking, index) => {
                    const departure = new Date(booking.date);
                    const departureDate = departure.toLocaleDateString();
                    const departureTime = departure.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                    return (
                      <tr key={index}>
                        <td>{booking.flight_from}</td>
                        <td>{booking.flight_to}</td>
                        <td>{departureDate}</td>
                        <td>{booking.time}</td>
                        <td>{booking.duration}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </>
          ) : (
            <p className="mt-4">You have no booked flights.</p>
          )}

          <button className="btn btn-danger mt-3" onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default AccountPage;
