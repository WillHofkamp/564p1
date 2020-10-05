
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Author: Will Hofkamp, Zeiwei Ren, Mitch McClure
Modified: 10/4/2020

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

#initialize global lists for duplicate checking of users and items
userIDs = []
itemIDs = []

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Goes char by char of a string and checks if each char is a quote, if so it escapes it accordingly
"""
def escapeQuotes(strg):
    charCount = 0
    for i, c in enumerate(strg):
        if c == "\"":
            charCount+=1
            strg = strg[:(i+charCount)]+"\""+strg[(i+charCount):]
    strg = "\""+strg+"\""
    return strg

"""
Writes to the users table if the user id is not a duplicate with the users id, rating, location, and country
"""
def printSeller(value, item, usersTable):
    #add to usersTable only if the user doesn't exist
    if value['UserID'] not in userIDs:
        userIDs.append(value['UserID'])
        usersTable.write(escapeQuotes(str(value["UserID"]))+"|"+value["Rating"]+"|"+escapeQuotes(item["Location"])+"|"+escapeQuotes(item["Country"]) +"\n")

"""
Writes to the bids table based on the time, amount, user id, and items
"""
def printBid(value, item, usersTable, bidsTable):
 if value:
     for bid in value:
         bidTime = transformDttm(bid["Bid"]["Time"])
         bidAmount = transformDollar(bid["Bid"]["Amount"])
         #add userID and itemID
         bidUserId = bid["Bid"]["Bidder"]['UserID']
         bidsTable.write(escapeQuotes(bidUserId)+"|"+str(item["ItemID"])+"|"+bidTime+"|"+bidAmount+"\n")
         #add to user table
         if bidUserId not in userIDs:
             if "Location" not in bid["Bid"]["Bidder"].keys():
                 location = "NULL"
             else:
                 location = bid["Bid"]["Bidder"]["Location"]
                 location = escapeQuotes(location)
             if "Country" not in bid["Bid"]["Bidder"].keys():
                 country = "NULL"
             else:
                 country = bid["Bid"]["Bidder"]["Country"]
                 country = escapeQuotes(country)

             usersTable.write(escapeQuotes(bidUserId)+"|"+bid["Bid"]["Bidder"]["Rating"]+"|"+location+"|"+country+"\n")

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        #Open .dat file for each table used
        itemsTable = open("itemsTable.dat","a")
        bidsTable = open("bidsTable.dat","a")
        usersTable = open("usersTable.dat","a")
        categoryTable = open("categoryTable.dat","a")

        #Initialize variables for duplicate checking
        for item in items:
            if item["ItemID"] not in itemIDs:
                itemIDs.append(item["ItemID"])
                for key, value in item.items():
                    
                    if key == "Seller":
                        printSeller(value, item, usersTable)
                        itemsTable.write(str(value["UserID"])+"|")
                    elif key == "Bids":
                        printBid(value, item, usersTable, bidsTable)
                    elif key  == "Category":
                        for category in value:
                            categoryTable.write(str(item["ItemID"])+ "|" + category+"\n")
                    elif key in {"Currently", "First_Bid"}:
                        value = transformDollar(value)
                        itemsTable.write(str(value)+"|")
                    elif key in {"Started", "Ends"}:
                        value = transformDttm(value)
                        itemsTable.write(str(value)+"|")
                    elif key in {"Description", "Name"}:
                        value = value.replace('"', '""') if value is not None else ""
                        value = "\"" + value + "\""
                        itemsTable.write(str(value)+"|")
                    elif key in {"Location", "Country", "Buy_Price"}:
                        pass
                    else:
                        value = escapeQuotes(value)
                        itemsTable.write(str(value)+"|")

                #last column is the buy price since it is optional and a new line
                if "Buy_Price" not in item.keys():
                    itemsTable.write("NULL"+"\n")
                else:
                    itemsTable.write(transformDollar(item["Buy_Price"])+"\n")

            pass
        #close all tables/files after we are finished using them
        itemsTable.close()
        bidsTable.close()
        usersTable.close()
        categoryTable.close()

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
