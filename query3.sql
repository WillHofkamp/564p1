/*
This file: query3.sql
Main file: runParser.sh
Authors: Mitch McClure, Ziwei Ren, Will Hofkamp
Find the number of auctions belonging to exactly four categories
*/

WITH categoryCountSq AS(
	SELECT ItemID, COUNT(*) as CategorySize 
	FROM Category
	GROUP BY ItemID
)
SELECT COUNT(*)
FROM categoryCountSq
WHERE CategorySize=4; 