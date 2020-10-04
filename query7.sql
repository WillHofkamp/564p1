/*
This file: query7.sql
Main file: runParser.sh
Authors: Mitch McClure, Ziwei Ren, Will Hofkamp
Find the number of categories that include at least one item with a bid of more than $100
*/

SELECT count(DISTINCT Name)
FROM Category
WHERE ItemID IN(
    SELECT ItemID
    FROM Items
    WHERE ItemID IN(
        SELECT ItemID
        FROM Bids
        WHERE Amount > 100
    )
)
