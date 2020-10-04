/*
This file: query5.sql
Main file: runParser.sh
Authors: Mitch McClure, Ziwei Ren, Will Hofkamp
Find the number of sellers whose rating is higher than 1000. 
*/

SELECT count(UserID)
FROM Users
WHERE UserID IN (
    SELECT Seller_ID
    FROM Items
)
AND Rating > 1000
