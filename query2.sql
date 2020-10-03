/*
This file: query2.sql
Main file: runParser.sh
Authors: Mitch McClure, Ziwei Ren, Will Hofkamp
Find the number of users from New York (i.e., users whose location is the string "New York").  
*/

SELECT COUNT(*)
FROM Users
WHERE Location = "New York";