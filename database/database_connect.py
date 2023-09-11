import psycopg2
import csv
from database.user_auth import UserAuth


class DatabaseConnect:
    '''
    To provide utilites to connect to our postgresql server
    '''
    def __init__(self):
        usr=UserAuth()
        self.__db_config = {
            'dbname': 'postgres',
            'user': usr.getUserName(),
            'password': usr.getPassword(),
            'host': 'localhost',  
            'port': '5432',       
        }
        pass


    def createTable(self):
        '''
        @brief: Creates table for storing scrapping data
        '''
        try:
            conn = psycopg2.connect(**self.__db_config) # establishing the connection
            cursor = conn.cursor() # creating a cursor object
            drop_table_sql = '''
            DROP TABLE IF EXISTS PropertyDetails;
            '''
            query = '''CREATE TABLE PropertyDetails(
            id serial PRIMARY KEY,
            docno NUMERIC not null,
            doctype text not null,
            Office text,
            year DATE,
            Buyername text,
            Sellername text,
            otherinfo text,
            listno varchar(255)
            );'''
            cursor.execute(drop_table_sql)
            cursor.execute(query) # Executing the sql query
            conn.commit() # Commit changes in the database
            conn.close() # Closing the connection
        except Exception as e:
            print(f"ERROR: {e}")


    def insertIntoTable(self, data):
        '''
        @brief: This function inserts data into table 
        @param: data = [ [ ] ]
        '''
        try:
            conn = psycopg2.connect(**self.__db_config) # establishing the connection
            cursor = conn.cursor() # creating a cursor object
            for row in data:
                cursor.execute(
                    "INSERT into PropertyDetails(docno, doctype,Office,year,Buyername,Sellername,otherinfo,listno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",
                    (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                )
            conn.commit() # Commit changes in the database
            conn.close() # Closing the connection
        except Exception as e:
            print(f"ERROR: {e}")
    
    def executeQuery(self, query):
        try:
            conn = psycopg2.connect(**self.__db_config) # establishing the connection
            cursor = conn.cursor() # creating a cursor object
            cursor.execute(query) # Executing the query
            data = cursor.fetchall()

            conn.commit() # Commit changes in the database
            conn.close() # Closing the connection
            return data
        except Exception as e:
            print(f"ERROR: {e}")



        

