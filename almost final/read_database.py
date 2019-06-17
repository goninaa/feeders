import psycopg2

# conn = psycopg2.connect("dbname=suppliers user=postgres password=postgres")

# host='localhost'
# database='suppliers'
# user='postgres'
# password='postgres'

conn = psycopg2.connect(host="localhost",database="suppliers", user="postgres", password="postgres")