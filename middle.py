# Middle layer switches between the data model and the display model
# Takes inputs from the display model and passes them to the data model
# Serves the query results from the data model to the display model
# The display model is not aware of the data model
# The data model is not aware of the display model
# Use a switch statement to determine which method to call in the data model
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd
import wx
import wx.adv
from matplotlib import pyplot as plt

import data_model


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
        return data_model.count_vsads_by_date_range(start_date, end_date)

    def vsads_by_date_range(self, start_date, end_date):
        return data_model.vsads_by_date_range(start_date, end_date)

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

    @staticmethod
    def generate_map():
        # Extract longitude and latitude coordinates
        longitude = data_model.fetch_longitude()
        latitude = data_model.fetch_latitude()

        # Create a scatter plot
        plt.figure(figsize=(8, 6))
        plt.scatter(longitude, latitude, s=10, alpha=0.5)
        plt.title('Accident Locations')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        # Save the plot as a PNG file
        plt.savefig('accident_locations.png')
        # Load the PNG file and display it in the panel
        accident_locations = wx.Image('accident_locations.png', wx.BITMAP_TYPE_ANY).Scale(200, 200)
        return accident_locations

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


    # A bar chart that displays the number of accidents by accident type for the parameters selected
    def TypeOfAccidentBarChart(self, keywords):
        data = data_model.filter_vsads_by_keywords(keywords)
        df = pd.DataFrame(data, columns=['ACCIDENT_TYPE', 'INJ_OR_FATAL'])
        df = df.groupby('ACCIDENT_TYPE')['INJ_OR_FATAL'].sum()
        df.plot.bar()
        plt.show()

    # A Heatmap that displays the number of accidents by hour of day for the parameters selected
    def HourOfDayHeatmap(self, keywords):
        data = data_model.filter_vsads_by_keywords(keywords)
        df = pd.DataFrame(data, columns=['ACCIDENT_TYPE', 'INJ_OR_FATAL', 'ACCIDENT_TIME'])
        df['ACCIDENT_TIME'] = pd.to_datetime(df['ACCIDENT_TIME'])
        df['hour'] = df['ACCIDENT_TIME'].dt.hour
        df = df.groupby('hour')['INJ_OR_FATAL'].sum()
        df.plot.bar()
        plt.show()

    # Create a scatter plot of the parameters selected against the longitude and latitude of the accidents
    def LocationScatterPlot(self, keywords):
        data = data_model.filter_vsads_by_keywords(keywords)
        df = pd.DataFrame(data, columns=['ACCIDENT_TYPE', 'INJ_OR_FATAL', 'LONGITUDE', 'LATITUDE'])
        plt.scatter(df['LONGITUDE'], df['LATITUDE'])
        plt.show()