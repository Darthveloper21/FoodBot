CREATE DATABASE IF NOT EXISTS FindFood;

USE FindFood;

DROP TABLE IF EXISTS timetable;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS diners;

CREATE TABLE diners (
	id INT(20) NOT NULL AUTO_INCREMENT,
	name TEXT  NOT NULL COLLATE 'utf16_vietnamese_ci',
	address TEXT NOT NULL COLLATE 'utf16_vietnamese_ci',
	city TEXT NOT NULL COLLATE 'utf16_vietnamese_ci',
	district TEXT COLLATE 'utf16_vietnamese_ci',
	pricemin DECIMAL(12, 2) NOT NULL,
	pricemax DECIMAL(12, 2) NOT NULL,
	website TEXT COLLATE 'utf16_vietnamese_ci',
	qualityPoint FLOAT(5, 2),
	pricePoint FLOAT(5, 2),
	servicePoint FLOAT(5, 2),
	destinationPoint FLOAT(5, 2),
	spacePoint FLOAT(5, 2),
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE menu (
	foodID INT(20) NOT NULL AUTO_INCREMENT,
	name TEXT NOT NULL COLLATE 'utf16_vietnamese_ci',
	price VARCHAR(20) NOT NULL,
	details TEXT COLLATE 'utf16_vietnamese_ci',
	dinerID INT(20) NOT NULL,
	PRIMARY KEY (foodID),
	CONSTRAINT myfood FOREIGN KEY (dinerID) REFERENCES diners(id) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE timetable (
	dinerID INT(20) NOT NULL,
	time_start TIME NOT NULL,
	time_close TIME NOT NULL,
	CONSTRAINT mytime FOREIGN KEY (dinerID) REFERENCES diners(id) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
