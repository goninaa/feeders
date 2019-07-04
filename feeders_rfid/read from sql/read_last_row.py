import psycopg2
from config import config

import psycopg2
# def getMobileDetails(mobileID):
    # try:
    #     params = config()
    #     connection = psycopg2.connect(**params)
    #     print("Using Python variable in PostgreSQL select Query")
    #     cursor = connection.cursor()
    #     postgreSQL_select_Query = "select * from mobile where id = %s"
    #     cursor.execute(postgreSQL_select_Query, (mobileID,))
    #     mobile_records = cursor.fetchall()
    #     for row in mobile_records:
    #         print("Id = ", row[0], )
    #         print("Model = ", row[1])
    #         print("Price  = ", row[2])
    # except (Exception, psycopg2.Error) as error:
    #     print("Error fetching data from PostgreSQL table", error)
    # finally:
    #     # closing database connection
    #     if (connection):
    #         cursor.close()
    #         connection.close()
    #         print("PostgreSQL connection is closed \n")
try:
    params = config()
    connection = psycopg2.connect(**params)

    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from bats_feeders"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from bats_feeders table using cursor.fetchall")
    records = cursor.fetchall() 
    
    print("Print each row and it's columns values")
    for row in records:
        print("A = ", row[0], )
        print("B = ", row[1])
        print("C  = ", row[2], "\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
# getMobileDetails(2)
# getMobileDetails(3)