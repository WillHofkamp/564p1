/*
This file: query4.sql
Main file: runParser.sh
Authors: Mitch McClure, Ziwei Ren, Will Hofkamp
Find the ID(s) of auction(s) with the highest current price. 
*/

WITH maxBid AS(
	SELECT ItemID, MAX(Currently) 
	FROM Items
)
SELECT ItemID
FROM maxBid;