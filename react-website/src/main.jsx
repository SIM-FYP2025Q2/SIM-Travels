//Main.jsx file, app gets inserted into HTML Page
//Import tools to render React into browser
import React from 'react';
import ReactDOM from 'react-dom/client';

//Import App.jsx file
import App from './App.jsx';

//StrictMode helps catch potential bugs/ createRoot allows creation of root container for rendering React components
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'   //Allows React to work on multiple tasks simultaneously, improve performance and responsiveness

//App Styling and Components
import 'bootstrap/dist/css/bootstrap.min.css'       // Import for use of Bootstrap CSS 
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Import for use of Bootstrap JS

//Makes user session info available globally
import { SessionProvider } from './Services/SessionContext.jsx';

//Tells React to render app into root in index.html
createRoot(document.getElementById('root')).render(
  /*StrictMode = Catch common bugs during dev
   SessionProdiver = Wraps whole app so any component can access session info like user and setUser using useSession() hook*/
  <React.StrictMode>
      <SessionProvider>
        <App />
      </SessionProvider>
  </React.StrictMode>
);
