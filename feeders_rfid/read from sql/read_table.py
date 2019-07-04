import psycopg2
from config import config

class READER:

try:
    params = config()
    connection = psycopg2.connect(**params)

    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from bats_feeders"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from bats_feeders table using cursor.fetchall")
    records = cursor.fetchall() 
    # only_one = cursor.fetchone()
    
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