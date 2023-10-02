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

from Constants import BORDER


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


class MapPanel(wx.Panel):  # Might put this in a different file
    def __init__(self, parent):
        super(MapPanel, self).__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a SearchPanel instance
        search_panel = SearchPanel(self)

        # Create a horizontal box sizer to hold the SearchPanel and the plot
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add the SearchPanel to the horizontal sizer
        horizontal_sizer.Add(search_panel, 0, wx.ALL, BORDER)

        # Load data from the CSV file
        data = pd.read_csv('Crash Statistics Victoria.csv')

        # Extract longitude and latitude coordinates
        longitude = data['LONGITUDE']
        latitude = data['LATITUDE']

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
        graphic_bitmap = wx.StaticBitmap(self, -1, accident_locations.ConvertToBitmap(), (0, 0),
                                         (accident_locations.GetWidth(), accident_locations.GetHeight()))

        # Add the plot to the horizontal sizer
        horizontal_sizer.Add(graphic_bitmap, 1, wx.ALL | wx.CENTER, BORDER)

        # Add the horizontal sizer to the main vertical sizer
        sizer.Add(horizontal_sizer, 1, wx.EXPAND)

        self.SetSizer(sizer)


class SearchPanel(wx.Panel):
    def __init__(self, parent):
        super(SearchPanel, self).__init__(parent, style=wx.BORDER_SIMPLE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, wx.ID_ANY, "Accident Types:")
        sizer.Add(label, 0, wx.ALL | wx.EXPAND, BORDER)

        self.list_box = wx.ListBox(self, wx.ID_ANY,
                                   choices=["Struck Pedestrian", "Collision with vehicle",
                                            "Collision with a fixed object", "No collision and no object struck",
                                            "Struck animal", "Vehicle overturned (no collision)",
                                            "Collision with some other object", "Fall from or in moving vehicle",
                                            "Other accident"],

                                   style=wx.LB_MULTIPLE)
        sizer.Add(self.list_box, 0, wx.ALL | wx.EXPAND, BORDER)

        self.clear_button = wx.Button(self, label="Clear")
        self.clear_button.Bind(wx.EVT_BUTTON, self.on_clear_button_click)  # Binding to event
        sizer.Add(self.clear_button, 0, wx.ALL | wx.EXPAND, BORDER)

        date_sizer = wx.BoxSizer(wx.VERTICAL)

        lower_date = wx.DateTime()
        lower_date.Set(1, wx.DateTime.Jul, 2013)
        upper_date = wx.DateTime()
        upper_date.Set(1, wx.DateTime.Feb, 2019)

        self.start_date_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        date_sizer.Add(self.start_date_text, 0, wx.ALL | wx.EXPAND, BORDER)

        self.start_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, dt=lower_date,
                                                       style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        date_sizer.Add(self.start_date_picker, 0, wx.ALL | wx.EXPAND, BORDER)

        self.end_date_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        date_sizer.Add(self.end_date_text, 0, wx.ALL | wx.EXPAND, BORDER)

        self.end_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, dt=upper_date,
                                                     style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        date_sizer.Add(self.end_date_picker, 0, wx.ALL | wx.EXPAND, BORDER)

        self.alcohol_related_checkbox = wx.CheckBox(self, label="Alcohol Related?")
        date_sizer.Add(self.alcohol_related_checkbox, 0, wx.ALL | wx.EXPAND, BORDER)

        self.generate_report_button = wx.Button(self, label="Generate Report")
        self.generate_report_button.Bind(wx.EVT_BUTTON, self.on_generate_report_button_click)  # Bind the event handler
        sizer.Add(self.generate_report_button, 0, wx.ALL | wx.EXPAND, BORDER)

        sizer.Add(date_sizer, 0, wx.ALL | wx.EXPAND, BORDER)
        self.SetSizer(sizer)

    # Event handler for the clear button being pressed by the user.
    def on_clear_button_click(self, event):
        self.list_box.SetSelection(wx.NOT_FOUND)

    # Event handler for the Generate Report button being pressed by the user.
    def on_generate_report_button_click(self, event):
        selected_options = self.list_box.GetSelections()
        start_date = self.start_date_picker.GetValue()
        end_date = self.end_date_picker.GetValue()
        alcohol_related = self.alcohol_related_checkbox.GetValue()

        # Create a report message
        report_message = "Report generated with the following options:\n"
        report_message += f"Selected Options: {selected_options}\n"
        report_message += f"Start Date: {start_date}\n"
        report_message += f"End Date: {end_date}\n"
        report_message += f"Alcohol Related: {alcohol_related}"

        # Create and display a message dialog with the report
        dlg = wx.MessageDialog(self, report_message, "Report", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class HomePanel(wx.Panel):  # Might put this in a different file
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.headline_text = wx.StaticText(self, style=wx.ALIGN_CENTER, label="Accident Information")
        sizer.Add(self.headline_text, 0, wx.ALL | wx.EXPAND, BORDER)

        vic_graphic = wx.Image('state_vic_graphic.jpg', wx.BITMAP_TYPE_ANY).Scale(200, 200)
        graphic_bitmap = wx.StaticBitmap(self, -1, vic_graphic.ConvertToBitmap(), (0, 0),
                                         (vic_graphic.GetWidth(), vic_graphic.GetHeight()))
        sizer.Add(graphic_bitmap, 0, wx.ALL | wx.CENTER, BORDER)

        self.SetSizer(sizer)


class AccInfoPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create a SearchPanel on the left-hand side
        search_panel = SearchPanel(self)
        sizer.Add(search_panel, 0, wx.ALL, BORDER)

        # Create a container for the content on the right-hand side
        content_container = wx.Panel(self)
        content_container.SetSizer(wx.BoxSizer(wx.VERTICAL))

        self.headline_text = wx.StaticText(content_container, style=wx.ALIGN_CENTER, label="Accident Information")
        content_container.GetSizer().Add(self.headline_text, 0, wx.ALL | wx.EXPAND, BORDER)

        # Create a notebook for "Type of Accident" and "Time of Day" tabs
        acc_info_notebook = wx.Notebook(content_container)
        type_of_accident_panel = TypeOfAccidentPanel(acc_info_notebook)
        time_of_day_panel = TimeOfDayPanel(acc_info_notebook)

        # Add tabs to the notebook
        acc_info_notebook.AddPage(type_of_accident_panel, "Type of Accident")
        acc_info_notebook.AddPage(time_of_day_panel, "Time of Day")

        # Add the notebook to the content container
        content_container.GetSizer().Add(acc_info_notebook, 1, wx.EXPAND | wx.ALL, BORDER)

        # Add the content container to the sizer
        sizer.Add(content_container, 1, wx.EXPAND)

        self.SetSizer(sizer)


class TypeOfAccidentPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Create and display the graph or chart for "Type of Accident" here
        # For example, you can use matplotlib to create and display the chart


class TimeOfDayPanel(wx.Panel):
    def __init__(self, parent):
        super(TimeOfDayPanel, self).__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(6, 4))

        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def create_bar_graph(self, labels, counts):
        self.ax.clear()
        x = np.arange(len(labels))
        self.ax.bar(x, counts)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels)
        self.ax.set_xlabel("Day of the Week")
        self.ax.set_ylabel("Accident Count")
        self.ax.set_title("Accidents by Day of the Week")
        self.figure.tight_layout()
        self.canvas.draw()

    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()