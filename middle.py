import sqlite3
import datetime
import pandas as pd
import display_model as dm
import data_model as dtm
import matplotlib.pyplot as plt


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
        return dtm.count_vsads_by_date_range(start_date, end_date)

    def vsads_by_date_range(self, start_date, end_date):
        return dtm.vsads_by_date_range(start_date, end_date)

    # Define a function that plots the 'ACCIDENT_TYPE' column of the DataFrame as the y-axis and the number of
    # occurrences of each accident type as the x-axis

    def plot_accident_types(self, start_date, end_date):
        try:
            # Call the vsads_by_date_range() function to get the data
            data = self.vsads_by_date_range(start_date, end_date)


            if not data:
                print("No data found for the specified date range.")
                return

            # Extract the 'ACCIDENT_TYPE' values from the data
            accident_types = [row[7] for row in data]

            # Create a DataFrame from the extracted values
            df = pd.DataFrame(accident_types, columns=['ACCIDENT_TYPE'])

            # Plot the DataFrame as a bar chart with the number of occurrences on the x-axis
            df['ACCIDENT_TYPE'].value_counts().plot(kind='barh')

            #Change the Title of the plot to 'Accident Types'
            plt.title('Accident Types')
            # Add in grid Lines
            plt.grid(True)








            # Display the plot
            plt.show()
        except Exception as e:
            print("Error:", e)





















if __name__ == "__main__":
    db_filename = 'crash_data.db'

    # Use the DataProcessor as a context manager
    with DataProcessor(db_filename) as data_processor:
        start_date = datetime.datetime(2013, 10, 4)
        end_date = datetime.datetime(2016, 1, 2)


        # Testing
        print("Start Date:", start_date)
        print("End Date:", end_date)

        data_processor.count_vsads_by_date_range(start_date, end_date)
        print(data_processor.count_vsads_by_date_range(start_date, end_date))







