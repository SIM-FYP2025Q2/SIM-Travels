//Nabar component file
import React, { useEffect, useState } from 'react';           //Import React
import { Link } from 'react-router-dom';                      //Import Link to be used for routing
import axios from 'axios';                                    //Axios
import brandlogo from '../../assets/brandlogo.png';           //The brand logo for the image

import { useSession } from '../../Services/SessionContext';   //Get session data (user)

//Navbar component
const Navbar = () => {

  //Read current session user from context
  const { user } = useSession();
  //Debugging in console
  console.log('Navbar re-rendered. Current user:', user);

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light fixed-top shadow-sm">
      <div className="container-fluid">
        {/*When clicking the image, will link to the homepage*/}
        <Link className="navbar-brand" to="/">
          <img src={brandlogo} alt="SIM TRAVELS" width="250" height="50" />
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse"data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        {/*When the webpage is opened in mobile, menu becomes hamburger*/}
        <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item"><Link className="nav-link" to="/">Home</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/flights">Flights</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/hotels">Hotels</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/airport-transfers">Airport Transfers</Link></li>
            <li className="nav-item">
              {/*If user is logged in, navbar will show their username and redirect to /Account (AccountPage), if not show "Login"*/}
              {user?.username ? (
                <Link className="nav-link" to="/account">{user.username}</Link>
              ) : (
                <Link className="nav-link" to="/login">Login</Link>
              )}
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
