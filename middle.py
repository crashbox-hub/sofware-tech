import sqlite3
import datetime
import pandas as pd
import display_model as dm
import data_model as dtm
import matplotlib as plot


class DataProcessor:
    def __init__(self, db_filename):
        self.db_filename = db_filename


    # A method to close DataProcessor's connection to the database, not guaranteed to be called
    # The with in the main handles this for us
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_filename)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, 'conn'):
            self.conn.close()

# Call the query vsads_by_date_range() in data_model.py to get the number of VSADS in the date range 04/09/2013 to
# 02/01/2016

    def count_vsads_by_date_range(self, start_date, end_date):
        dtm.count_vsads_by_date_range(start_date, end_date)
        return dtm.count_vsads_by_date_range(start_date, end_date)

















if __name__ == "__main__":
    db_filename = 'crash_data.db'

    # Use the DataProcessor as a context manager
    with DataProcessor(db_filename) as data_processor:
        start_date = datetime.datetime(2013, 10, 4)
        end_date = datetime.datetime(2016, 1, 2)

        print("Start Date:", start_date)
        print("End Date:", end_date)

        data_processor.count_vsads_by_date_range(start_date, end_date)
        print(data_processor.count_vsads_by_date_range(start_date, end_date))







