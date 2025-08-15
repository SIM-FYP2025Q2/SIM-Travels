//Login page component
import React, { useState } from 'react';            //Import react tools
import { useNavigate } from 'react-router-dom';     //For routing


import { useSession } from '../../Services/SessionContext';  //Get session data (user)
import axios from '../../Services/axios';                    //Custom Axios with session support


function LoginPage() {
  //State for form inputs
  const [username, setUsername] = useState('');   //Store username input
  const [password, setPassword] = useState('');   //Store password input
  const [errorMsg, setErrorMsg] = useState('');   //Store error message to display
  const navigate = useNavigate();                 //Hook for navigation

  const { setUser } = useSession();               //Destructure setUser function and update user session after login

  const handleLogin = async (e) => {
    e.preventDefault();                           //Prevent default form submission behaviour
    setErrorMsg('');                              //Clear previous error messages

    //Validation to check if username and password provided
    if (!username || !password) {
      return setErrorMsg('Please enter both username and password.');
    }

    //Send POST request to login API with username and password
    try {
      const res = await axios.post('/api/users/login', {
        username,
        password
      }, { withCredentials: true }); //Enable cookies for session

      
      if (res.data.success) {
        //Update user session state with response data
        setUser(res.data);
        setTimeout(() => {
          navigate('/account');
        }, 10); //Let React finish re-rendering context
      }
    } catch (err) {
      if (err.response && err.response.status === 401) {
        setErrorMsg('Invalid username or password.');
      } else {
        setErrorMsg('Server error. Please try again later.');
      }
    }
  };
  
  return (
    <div className="container mt-5">
      <h2>Login</h2>
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
      <form onSubmit={handleLogin}>
        <input type="text" className="form-control" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} /><br />
        <input type="password" className="form-control" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} /><br />
        <button type="submit" className="btn btn-primary me-2">Login</button>
        <button type="button" className="btn btn-secondary" onClick={() => navigate('/register')}>Create Account</button>
      </form>
    </div>
  );
}

export default LoginPage;
