//Homepage component
import React from 'react';  //import React Tools
import './HomePage.css';    //Homepage CSS 
import CarouselCards from '../CarouselCards/CarouselCards'; //Import CarouselCards component for display

const HomePage = () => {
  return (
    <div className="container mt-5">

      <CarouselCards/>

      <h2 className="text-center mb-4">Welcome to SIM TRAVELS</h2>

      <div className="row">
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card shadow-sm h-100">
              <img src="https://images.pexels.com/photos/8257936/pexels-photo-8257936.jpeg" className="card-img-top" alt="Travel Destination"/>
              <div className="card-body d-flex flex-column">
                <h5 className="card-title">Membership</h5>
                <p className="card-text">Sign up for SIM TRAVELS member and get exlusive benefits and rewards when you reserve your holidays with us!</p>
                <a href="/register" className="btn btn-primary mt-auto">Register here</a>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card shadow-sm h-100">
              <img src="https://images.pexels.com/photos/8937438/pexels-photo-8937438.jpeg" className="card-img-top" alt="Shopping Offers"/>
              <div className="card-body d-flex flex-column">
                <h5 className="card-title">Elevate your lifestyle</h5>
                <p className="card-text">Looking for booking offers? Check out our seasonal and monthly promotions, treat yourself or your loved ones.</p>
                <a href="/" className="btn btn-primary mt-auto">Enjoy Promotions</a>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card shadow-sm h-100">
              <img src="https://images.pexels.com/photos/221164/pexels-photo-221164.jpeg" className="card-img-top" alt="Frequently Asked Questions"/>
              <div className="card-body d-flex flex-column">
                <h5 className="card-title">Frequently Asked Questions (FAQs)</h5>
                <p className="card-text">Do you have questions? Find your answers here!</p>
                <a href="/" className="btn btn-primary mt-auto">Browse FAQ</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

