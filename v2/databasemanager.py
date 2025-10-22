import requests
import os
from typing import List, Any

import sqlite3
from typing import List, Any

class DatabaseManager:
    def __init__(self, db_path: str = 'lab_seg.db'): #"/Users/ashleylutz/Documents/agent_based_products/lab_seg.db"):
        self.db_path = db_path
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            print(f"Connected to SQLite database at {self.db_path}")
            return conn
        except sqlite3.Error as e:
            raise Exception(f"Error connecting to database: {str(e)}")

    # def get_schema(self) -> str:
    #     """Retrieve the database schema."""
    #     try:
    #         cursor = self.connection.cursor()
    #         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #         tables = cursor.fetchall()
    #         print(tables)
    #         schema = ""
    #         for (table_name,) in tables:
    #             cursor.execute(f"PRAGMA table_info({table_name});")
    #             columns = cursor.fetchall()
    #             schema += f"Table: {table_name}\n"
    #             for col in columns:
    #                 schema += f"  {col[1]} ({col[2]})\n"
    #             schema += "\n"
    #         print(schema)
    #         return schema.strip()
    #     except sqlite3.Error as e:
    #         raise Exception(f"Error fetching schema: {str(e)}")

    def get_schema(self) -> str:
        """Retrieve the schema for the 'labseg' table in lab_seg.db."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("PRAGMA table_info(labseg);")
            columns = cursor.fetchall()

            if not columns:
                return "Table 'labseg' does not exist or has no columns."

            schema = "Table: labseg\n"
            for col in columns:
                # col[1] = column name, col[2] = data type
                schema += f"  {col[1]} ({col[2]})\n"

            return schema.strip()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching schema: {str(e)}")

    

    def execute_query(self, query: str) -> List[dict]:
        """Execute SQL query and return results as list of dictionaries (like response.json()['results'])."""
        try:
            cursor = self.connection.cursor()
            print("connected")
            cursor.execute(query)
            print("executed")
            columns = [desc[0] for desc in cursor.description]  # Get column names
            rows = cursor.fetchall()  # Get all rows
            results = [dict(zip(columns, row)) for row in rows]  # Convert to list of dicts
            return results
        except sqlite3.Error as e:
            raise Exception(f"Error executing query: {str(e)}")


    def close_connection(self):
        if self.connection:
            self.connection.close()