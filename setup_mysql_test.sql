-- This script prepares a MySQL test server for the project hbnb clone
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
use hbnb_test_db
GRANT SELECT ON performance_schema.* TO 'root'@'localhost';
