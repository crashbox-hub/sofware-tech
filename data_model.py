import sqlite3
import pandas as pd


class DataModel:
    def __init__(self, db_file_path):

        self.db_file_path = db_file_path
        self.connection = sqlite3.connect(db_file_path)

    def get_relevant_data(self, query):
        try:
            # Pandas execute a SQL query and retrieve data as a DataFrame
            relevant_data = pd.read_sql_query(query, self.connection)
            return relevant_data
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    db_file_path = "vsads.db"
    data_model = DataModel(db_file_path)

    # Example Query !!! Change once Middle Layer is implemented
    query = "SELECT * FROM your_table WHERE your_condition"

    # Access relevant data by executing the query
    relevant_data = data_model.get_relevant_data(query)
    data_model.close_connection()
