#!/usr/bin/python3

# Import the libraries
from optparse import OptionParser
import psycopg2
import pandas as pd
import json

class DBConnect:
    def __init__(self):
         pass
		
    def read_options(self):
        parser = OptionParser()
        parser.add_option("-f", "--inputfile", dest="input_filename", help="input file path", metavar="FILE")
        parser.add_option("-t", "--filetype", action="store_false", dest="file_type", default="csv", help="don't print status messages to stdout")
		
        (options, args) = parser.parse_args()
        self.input_file = options.input_filename
        self.original_file = self.input_file
        self.file_type = options.file_type
	
	
    def conn_database(self):
        # Connect to postgres database
        try:
            self.conn = psycopg2.connect("dbname='accounts' user='sqluser' host='172.31.8.214' password='sqlpass' port='5432'")
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print("Connected Successfully")
        except:
            print("Cannot connect to database")

    def create_table(self):
        # Create table if not exists
        create_table_cmd = "CREATE TABLE IF NOT EXISTS users(ID serial PRIMARY KEY, Firstname varchar(120), Lastname varchar(120))"
        self.cursor.execute(create_table_cmd)

    def insert_record(self):
        # insert records in table
        try:
            namelist = pd.read_csv(self.input_file)
            print(namelist)
            for i in namelist.index:
                idss = namelist.iloc[i, 0]
                idss = int(idss)
                fname = namelist.iloc[i, 1]
                lname = namelist.iloc[i, 2]
                sql = "INSERT INTO users (id, firstname, lastname) VALUES (%s, %s, %s)"
                val = (idss, fname, lname)
                self.cursor.execute(sql, val)
        except:
            print("Data exists, please check")

    def read_data(self):
        # Get the data from table in json format
        self.cursor.execute("SELECT * FROM users;")
        users = self.cursor.fetchall()
        user_df = pd.DataFrame(users, columns=['id', 'firstname', 'lastname'])
        result = user_df.set_index('id').to_json(orient="table")
        parsed = json.loads(result)
        with open('users.txt', 'w') as json_file:
            json.dump(parsed, json_file)

    def conn_close(self):
        # Close the database connection
        try:
            self.cursor.close()
            self.conn.close()
        except:
            print("Connection is closed")


if __name__ == '__main__':
    DBConnection = DBConnect()
    DBConnection.read_options()
    DBConnection.conn_database()
    DBConnection.create_table()
    DBConnection.insert_record()
    DBConnection.read_data()
    DBConnection.conn_close()

