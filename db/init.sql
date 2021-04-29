CREATE DATABASE fake_blok;
use fake_blok;

#Create tables

CREATE TABLE assignments (
  id INT NOT NULL AUTO_INCREMENT, 
  customer_name VARCHAR(255) NOT NULL, 
  min_floor_number INT NOT NULL, 
  max_floor_number INT NOT NULL, 
  post_numbers VARCHAR(255) NOT NULL, 
  min_area_living FLOAT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE realties (
  id INT NOT NULL AUTO_INCREMENT, 
  location_street_address VARCHAR(255) NOT NULL, 
  location_specifier VARCHAR(255) NOT NULL, 
  location_postcode VARCHAR(255) NOT NULL, 
  area_living FLOAT NOT NULL, 
  floor_number INT NOT NULL,
  PRIMARY KEY (id)
);


#Load data

LOAD DATA LOCAL INFILE './db/assignments.csv' 
  INTO TABLE assignments 
  FIELDS TERMINATED BY ',' 
  LINES TERMINATED BY '\n' 
  IGNORE 1 ROWS 
  (customer_name, min_floor_number, max_floor_number, post_numbers, min_area_living);

LOAD DATA LOCAL INFILE './db/realties.csv' 
  INTO TABLE realties 
  FIELDS TERMINATED BY ',' 
  LINES TERMINATED BY '\n' 
  IGNORE 1 ROWS 
  (location_street_address, location_specifier, location_postcode, area_living, floor_number);