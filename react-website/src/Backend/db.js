//Handles connection to MySQL Db (In this case the Azure SQL DB)
//Import mysql package 
import mysql from 'mysql2';

//Create connection to SQL with environment variables
const db = mysql.createConnection({
  host: process.env.DB_HOST,            //DB Server Address
  user: process.env.DB_USER,            //DB User
  password: process.env.DB_PASSWORD,    //DB User's PW
  database: process.env.DB_NAME,        //DB Name to use
  port: process.env.DB_PORT             //DB Port (usually 3306) for MySQL
});

//Connect to DB and log results in terminal
db.connect((err) => {
  if (err) {
    //If error, prompts error code
    console.error('Database connection failed:', err);
    return;
  }
  console.log('Database connected successfully');
});

//Export connection for use in other files
export default db;
