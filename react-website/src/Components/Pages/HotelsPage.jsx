//Hotel page component
import React, { useState, useEffect } from 'react'    //Import React tools

//Hardcoded data for prototyping
const hotelData = [
  {id:1, destination: 'Singapore', name: 'Fullerton Hotel', availableFrom: '2025-06-20', availableTo: '2025-06-25', pax:'1' },
  {id:2, destination: 'Singapore', name: 'Fullerton Hotel', availableFrom: '2025-06-20', availableTo: '2025-06-25', pax:'2' },
  {id:3, destination: 'Singapore', name: 'Hilton Hotel Singapore', availableFrom: '2025-06-22', availableTo: '2025-06-27', pax:'1' },
  {id:4, destination: 'Singapore', name: 'Hilton Hotel Singapore', availableFrom: '2025-06-22', availableTo: '2025-06-27', pax:'2' },

  {id:5, destination: 'Kuala Lumpur', name: 'Hilton Hotel Kuala Lumpur', availableFrom: '2025-06-20', availableTo: '2025-06-25', pax:'1' },
  {id:6, destination: 'Kuala Lumpur', name: 'Hilton Hotel Kuala Lumpur', availableFrom: '2025-06-20', availableTo: '2025-06-25', pax:'2' },
  {id:7, destination: 'Kuala Lumpur', name: 'Sunway Putra Hotel', availableFrom: '2025-06-21', availableTo: '2025-06-26', pax:'4' },
  {id:8, destination: 'Kuala Lumpur', name: 'Sunway Putra Hotel', availableFrom: '2025-06-21', availableTo: '2025-06-26', pax:'4' },

  {id:9, destination: 'Bangkok', name: 'Berkelely Hotel Pratunam', availableFrom: '2025-06-20', availableTo: '2025-06-25', pax:'2' },
  {id:10, destination: 'Bangkok', name: 'Berkelely Hotel Pratunam', availableFrom: '2025-06-20', availableTo: '2025-06-25', pax:'2' },
  {id:11, destination: 'Bangkok', name: 'Carlton Hotel Bangkok Sukhumvit', availableFrom: '2025-06-21', availableTo: '2025-06-25', pax:'2' },
  {id:12, destination: 'Bangkok', name: 'Carlton Hotel Bangkok Sukhumvit', availableFrom: '2025-06-22', availableTo: '2025-06-25', pax:'2' },
];

//Utility function to formate date as yyyy-mm-dd
const formatDate = (date) => date.toISOString().split('T')[0];

const HotelsPage = () => {
  //State to store inputs
  const [keyword, setKeyword] = React.useState('');             //Store searched keyword (destination/hotel name)
  const [checkIn, setCheckIn] = React.useState('');             //Store check-in date
  const [checkOut, setCheckOut] = React.useState('');           //Store check-out date
  const [searchResults, setSearchResults] = React.useState([]); //Store search results from API
  const [showResults, setShowResults] = React.useState(false);  //Control visibility of results

  //Function to reset the dates
  useEffect(() => {
    resetDates();
  }, []); //Empty dependency array = runs only on initial render

  //Compute today's and tomorrow's date on initial render and set as default dates on page load
  const resetDates = () => {
    const today = new Date();                 //Get today's date
    const tomorrow = new Date(today);         //Create new date object for tomorrow
    tomorrow.setDate(tomorrow.getDate() + 1); //Set tomorrow date, today + 1 day 
    setCheckIn(formatDate(today));            //Set check-in to today's date
    setCheckOut(formatDate(tomorrow));        //Set check-out to tomorrow's date
  };
  
  //Search button
  const handleSearch = () => {
    //Validation data: all fields are compulsory to fill in
    if (!keyword.trim() || !checkIn || !checkOut) {
      alert("Please fill in all fields.");
      return;
    }

    //Validation: check-out must be after check-in
    if (checkOut <= checkIn) {
      alert("Check-out date must be after check-in date.");
      return;
    }

    /*Filter logic
    Checks if:
      The destination or hotel name 
      The check-in and check-out date matches with hotelData

      If matches = sets the filtered data into filteredHotels and displays the results
    */
    const filteredHotels = hotelData.filter((hotel) => {
      const keywordLower = keyword.toLowerCase();
      const destinationMatch = hotel.destination.toLowerCase().includes(keywordLower);
      const hotelNameMatch = hotel.name.toLowerCase().includes(keywordLower);

      const checkInDate = new Date(checkIn);
      const availableFromDate = new Date(hotel.availableFrom);
      const availableToDate = new Date(hotel.availableTo);

      //Filter logic: Check-in must fall within hotel's availability
      const dateMatch = checkInDate >= availableFromDate && checkInDate <= availableToDate;

      return (destinationMatch || hotelNameMatch) && dateMatch;
    });

    setSearchResults(filteredHotels);
    setShowResults(true);
  };


   //Clear fields button
  const handleClear = () => {
    setKeyword('');
    resetDates();
    setSearchResults([]);
    setShowResults(false);
  };

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Hotel Search</h1>

      {/*Search Form*/}
      <div className="card p-4 mb-4 shadow">
        <div className="row mb-3">
          {/*Destination or Hotel Name Input*/}
          <div className="col-md-6">
            <label>Where do you want to stay?</label>
            <input type="text" className="form-control" placeholder="Enter destination or hotel name" value={keyword} onChange={(e) => setKeyword(e.target.value)}/>
          </div>

          {/*Check-in Input*/}
          <div className="col-md-3">
            <label>Check-In</label>
            <input type="date" className="form-control" value={checkIn} onChange={(e) => setCheckIn(e.target.value)}/>
          </div>

          {/*Check-out Input*/}
          <div className="col-md-3">
            <label>Check-Out</label>
            <input type="date" className="form-control" value={checkOut} onChange={(e) => setCheckOut(e.target.value)}/>
          </div>
        </div>

        {/*Search and Clear Buttons*/}
        <div className="text-center">
          <button className="btn btn-primary mx-2" onClick={handleSearch}>Search</button>
          <button className="btn btn-secondary mx-2" onClick={handleClear}>Clear</button>
        </div>
      </div>

      {/*Display Search Results*/}
      {showResults && (
        <div className="mt-4">
          {searchResults.length > 0 ? (
            <table className="table table-bordered text-center">
              <thead>
                <tr>
                  <th>Destination</th>
                  <th>Hotel Name</th>
                  <th>Available From</th>
                  <th>Available To</th>
                  <th>Pax</th>
                </tr>
              </thead>
              <tbody>
                {searchResults.map((hotel, idx) => (
                  <tr key={idx}>
                    <td>{hotel.destination}</td>
                    <td>{hotel.name}</td>
                    <td>{hotel.availableFrom}</td>
                    <td>{hotel.availableTo}</td>
                    <td>{hotel.pax}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No hotels found matching your criteria.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default HotelsPage;
