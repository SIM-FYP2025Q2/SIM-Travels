//Footer Component files
import React from 'react' //Import React
import './Footer.css'     //CSS file for styling

//Footer component
const Footer = () => {
  return (
    <footer className="footer bg-dark text-white pt-5 pb-4 mt-5">
      <div className="container text-center text-md-start">
        <div className="row">

          <div className="col-md-3 col-sm-6 mb-4">
            <h5 className="text-uppercase">SIM TRAVELS</h5>
            <p>Lorem ipsum dolor sit amet consectetur adipiscing elit.</p>
          </div>

          <div className="col-md-3 col-sm-6 mb-4">
            <h5 className="text-uppercase">Company</h5>
            <ul className="no-bullets">
                <li>About Us</li>
                <li>The Team</li>
                <li>Partners</li>
                <li>Blogs</li>
            </ul>
          </div>

          <div className="col-md-3 col-sm-6 mb-4">
            <h5 className="text-uppercase">Social</h5>
            <ul className="no-bullets">
                <li>About Us</li>
                <li>Facebook</li>
                <li>Instagram</li>
            </ul>
          </div>

          <div className="col-md-3 col-sm-6 mb-4">
            <h5 className="text-uppercase">Contact Us</h5>
            <ul className="no-bullets">
                <li>461 Clementi Rd, Singapore 599491</li>
                <li>(+65) 9123 4567</li>
                <li>simtravels@mail.com.sg</li>
            </ul>
          </div>

        </div>

        <hr className="border-secondary" />

        <div className="text-center mt-3">
            {/*Copyright symbol & JS to get current year*/}
          <small>&copy; {new Date().getFullYear()} SIM TRAVELS. All rights reserved.</small>
        </div>
      </div>
    </footer>
  )
}

export default Footer
