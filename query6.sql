/*
This file: query6.sql
Main file: runParser.sh
Authors: Mitch McClure, Ziwei Ren, Will Hofkamp
Find the number of users who are both sellers and bidders.
*/

SELECT count(DISTINCT Seller_ID)
FROM Items
WHERE Seller_ID IN (
    SELECT DISTINCT UserID
    FROM Bids)
