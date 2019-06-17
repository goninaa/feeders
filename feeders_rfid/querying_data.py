import psycopg2
from config import config

	
# conn = psycopg2.connect(dsn)

# # create a new cursor, The cursor object is used to execute SELECT statements	
# cur = conn.cursor()


	
# cur.close()
# conn.close()
	
def bat_antenna():
    """ query data from the bats table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
 
        while row is not None:
            print(row)
            row = cur.fetchone()
 
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# exmple:
# def get_vendors():
#     """ query data from the vendors table """
#     conn = None
#     try:
#         params = config()
#         conn = psycopg2.connect(**params)
#         cur = conn.cursor()
#         cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
#         print("The number of parts: ", cur.rowcount)
#         row = cur.fetchone()
 
#         while row is not None:
#             print(row)
#             row = cur.fetchone()
 
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

if __name__ == "__main__":
    bat_antenna ()