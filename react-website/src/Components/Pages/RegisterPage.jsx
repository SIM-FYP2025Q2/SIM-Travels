//Component for Register page
import React, { useState } from 'react';              //Import React
import { useNavigate, Link } from 'react-router-dom'; //For navigatin routing
import axios from '../../Services/axios';             //Custom Axios with session support

const RegisterPage = () => {
  const navigate = useNavigate();                     //Hook for navigation

  //State to manage form data for registration
  const [formData, setFormData] = useState({
    //Initialize username and password as empty string
    username: '', 
    password: '',
  });

  //State to manage error and success, initialize as empty string
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  //Handle input changes in form
  const handleChange = (e) => {
    //Update formData state with new value for input field
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  //Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();         //Prevent default form submission behavior
    setError('');               //Clear previous error message
    setSuccess('');             //Clear previous success message

    //Destructure username and password from formData
    const { username, password } = formData;

    //Data validations
    if (!username || !password) {
      setError('Please fill in both username and password.');
      return;
    }

    try {
      //Send registration request to server
      const res = await axios.post('/api/users/register', { username, password });

      if (res.status === 201) {
        setSuccess('User registered successfully. Redirecting...');
        setTimeout(() => {
          navigate('/login');  //redirect to login page after 1.5s
        }, 1500);
      }
    } catch (err) {
      if (err.response && err.response.status === 409) {
        setError('Username already exists.');
      } else {
        setError('An error occurred. Please try again.');
      }
    }
  };

  return (
    <div className="container mt-5">
      <h2>Register new User</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Username:</label><br />
          <input type="text" className="form-control" name="username" value={formData.username} onChange={handleChange} autoComplete="username"/>
        </div>
        <div className="mb-3">
          <label>Password:</label><br />
          <input type="password" className="form-control" name="password" value={formData.password} onChange={handleChange} autoComplete="new-password"/>
        </div>
        <button type="submit" className="btn btn-primary">Register</button>
        <p className="mt-3">Already have an account? <Link to="/login">Login here</Link></p>
      </form>
    </div>
  );
};

export default RegisterPage;
