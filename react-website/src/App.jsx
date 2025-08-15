//This file defines main application structure and routing logic for navigating between pages
//Import React (Required for JSX and components)
import React, { useEffect } from 'react'
/*Import Reac Router to handle page navigation w/o refreshing page
Router: Wraps app to enable routing
Routes: Wraps all <Route> definitions
Route: Defines one route (e.g. /login to LoginPage)
*/
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'


//Navbar and Footer components
import Navbar from './Components/Navbar/Navbar'
import Footer from './Components/Navbar/Footer'

//Web Pages
import HomePage from './Components/Pages/HomePage'
import FlightsPage from './Components/Pages/FlightsPage'
import HotelsPage from './Components/Pages/HotelsPage'
import AirportTransfersPage from './Components/Pages/AirportTransfersPage'
import RegisterPage from './Components/Pages/RegisterPage'
import LoginPage from './Components/Pages/LoginPage'
import AccountPage from './Components/Pages/AccountPage'



function App() {

  return (
    // Main App Component
    // Using BrowserRouter to handle routing 
    <>
    <Router>
      <Navbar/>
      <div className="container mt-5 pt-5">
        <Routes>
          <Route path="/" element={<HomePage/>}/>
          <Route path="/flights" element={<FlightsPage/>}/>
          <Route path="/hotels" element={<HotelsPage/>}/>
          <Route path="/airport-transfers" element={<AirportTransfersPage/>}/>
          <Route path="/login" element={<LoginPage/>}/>
          <Route path="/register" element={<RegisterPage/>}/>
          <Route path="/account" element={<AccountPage/>}/>
        </Routes>
      </div>
      <Footer/>
    </Router>
    </>
  );
};

//Export and used in main.jsx
export default App;
