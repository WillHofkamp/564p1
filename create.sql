/*
This file: create.sql
Main file: runParser.sh
Authors: Mitch McClure, Ziwei Ren, Will Hofkamp
Create the users, items, bids, and category tables for the ebay data
to be inserted into. If those tables already exist, they will be dropped
*/

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS Category;

CREATE TABLE Users(
	UserID		VARCHAR,
	Rating		INT,
	Location	VARCHAR,
	Country		VARCHAR,
	PRIMARY KEY (UserID)
); 

CREATE TABLE Items(
	ItemID		INT NOT NULL,
	Ends		DATE NOT NULL,
	First_Bid	DOUBLE NOT NULL,
	Name		VARCHAR NOT NULL,
	Started		DATE NOT NULL, 
	Number_of_Bids	INT NOT NULL,
	Currently	DOUBLE NOT NULL,
	Seller_ID	VARCHAR NOT NULL,
	Description	VARCHAR NOT NULL,
	Buy_Price	DOUBLE,
	PRIMARY KEY (ItemId),
	FOREIGN KEY (Seller_ID) REFERENCES Users(UserID)
);

CREATE TABLE Bids(
	UserID		VARCHAR,
	ItemID		INT NOT NULL,
	Time		DATE NOT NULL,
	Amount		DOUBLE NOT NULL,
	PRIMARY KEY (UserID, Time, Amount, ItemID), --maybe can be reduce to 3
	FOREIGN KEY (UserID) REFERENCES Users(UserID),
	FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Category(
	ItemID		INT,
	Name		VARCHAR,
	PRIMARY KEY (Name, ItemID),
	FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);