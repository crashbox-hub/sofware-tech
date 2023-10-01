
# Middle layer switches between the data model and the display model
# Takes inputs from the display model and passes them to the data model
# Serves the query results from the data model to the display model
# The display model is not aware of the data model
# The data model is not aware of the display model
# Use a switch statement to determine which method to call in the data model

import sqlite3
import pandas as pd
import datetime


class DataProcessor:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_filename)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def count_accidents_by_date_range(self, start_date, end_date):
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT COUNT(*) FROM crash_data WHERE ACCIDENT_DATE BETWEEN ? AND ?"
                cursor.execute(query, (start_date, end_date))
                count = cursor.fetchone()[0]
                return count
        except Exception as e:
            print(f"Error counting accidents by date range: {e}")
            return None

    def calculate_average_injuries_by_hour(self):
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                query = ("SELECT strftime('%H', ACCIDENT_TIME) AS hour, AVG(INJ_OR_FATAL) AS avg_injuries "
                         "FROM crash_data GROUP BY hour")
                cursor.execute(query)
                data = cursor.fetchall()
                return data
        except Exception as e:
            print(f"Error calculating average injuries by hour: {e}")
            return None

    def filter_accidents_by_keywords(self, keywords):
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM crash_data WHERE ACCIDENT_TYPE IN ({})".format(",".join(["?"] * len(keywords)))
                cursor.execute(query, keywords)
                data = cursor.fetchall()
                return data
        except Exception as e:
            print(f"Error filtering accidents by keywords: {e}")
            return None

    def filter_accidents_by_alcohol(self, alcohol_related):
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM crash_data WHERE ALCOHOL_RELATED = ?"
                cursor.execute(query, (alcohol_related,))
                data = cursor.fetchall()
                return data
        except Exception as e:
            print(f"Error filtering accidents by alcohol-related: {e}")
            return None


if __name__ == "__main__":
    db_filename = 'crash_data.db'
    data_processor = DataProcessor(db_filename)

    start_date = datetime.datetime(2013, 10, 4)
    end_date = datetime.datetime(2016, 1, 2)

    count = data_processor.count_accidents_by_date_range(start_date, end_date)
    if count is not None:
        print("Number of accidents within date range:", count)

    average_injuries_by_hour = data_processor.calculate_average_injuries_by_hour()
    if average_injuries_by_hour is not None:
        print("Average injuries by hour of day:", average_injuries_by_hour)

    selected_keywords = ["Collision with vehicle", "Struck animal"]
    filtered_data = data_processor.filter_accidents_by_keywords(selected_keywords)
    if filtered_data is not None:
        print("Filtered data by keywords:", len(filtered_data), "records found.")

    alcohol_related_data = data_processor.filter_accidents_by_alcohol("No")
    if alcohol_related_data is not None:
        print("Non-alcohol-related data:", len(alcohol_related_data), "records found.")







