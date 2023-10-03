# Middle layer switches between the data model and the display model
# Takes inputs from the display model and passes them to the data model
# Serves the query results from the data model to the display model
# The display model is not aware of the data model
# The data model is not aware of the display model
# Use a switch statement to determine which method to call in the data model

import numpy as np
import pandas as pd
import wx
import wx.adv
from matplotlib import pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

import data_model


class DataProcessor:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    # A switch statement to determine which method to call from the data model
    def process_data(self, method, *args):
        from data_model import (count_vsads_by_date_range,
                                calculate_average_by_hour_of_day, filter_vsads_by_keywords,
                                filter_vsads_by_alcohol)

        #
        # from display_model import class
        if method == "count_vsads_by_date_range":
            return count_vsads_by_date_range(*args)
        elif method == "calculate_average_by_hour_of_day":
            return calculate_average_by_hour_of_day()
        elif method == "filter_vsads_by_keywords":
            return filter_vsads_by_keywords(*args)
        elif method == "filter_vsads_by_alcohol":
            return filter_vsads_by_alcohol(*args)
        else:
            return "Invalid method"
            # cursor.close()

    # A bar chart that displays the number of accidents by accident type for the parameters selected
    def TypeOfAccidentBarChart(self, keywords):
        data = self.process_data("filter_vsads_by_keywords", keywords)
        df = pd.DataFrame(data, columns=['ACCIDENT_TYPE', 'INJ_OR_FATAL'])
        df = df.groupby('ACCIDENT_TYPE')['INJ_OR_FATAL'].sum()
        df.plot.bar()
        plt.show()

    # A Heatmap that displays the number of accidents by hour of day for the parameters selected
    def HourOfDayHeatmap(self, keywords):
        data = self.process_data("filter_vsads_by_keywords", keywords)
        df = pd.DataFrame(data, columns=['ACCIDENT_TYPE', 'INJ_OR_FATAL', 'ACCIDENT_TIME'])
        df['ACCIDENT_TIME'] = pd.to_datetime(df['ACCIDENT_TIME'])
        df['hour'] = df['ACCIDENT_TIME'].dt.hour
        df = df.groupby('hour')['INJ_OR_FATAL'].sum()
        df.plot.bar()
        plt.show()

    # Create a scatter plot of the parameters selected against the longitude and latitude of the accidents
    def LocationScatterPlot(self, keywords):
        data = self.process_data("filter_vsads_by_keywords", keywords)
        df = pd.DataFrame(data, columns=['ACCIDENT_TYPE', 'INJ_OR_FATAL', 'LONGITUDE', 'LATITUDE'])
        plt.scatter(df['LONGITUDE'], df['LATITUDE'])
        plt.show()

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
