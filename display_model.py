import wx
import wx.adv
import pandas as pd
import matplotlib.pyplot as plt

BORDER = 5


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))

        self.SetMinSize(wx.Size(500, 500))
        notebook = wx.Notebook(self)
        notebook.SetSizer(wx.BoxSizer(wx.VERTICAL))

        # Create and add notebook pages
        notebook.AddPage(HomePanel(notebook), "Home")
        notebook.AddPage(AccInfoPanel(notebook), "Accident Info")
        notebook.AddPage(MapPanel(notebook), "Map")

        self.Centre()
        self.Show(True)


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
        super().__init__(parent)

        # Create and display the graph or chart for "Time of Day" here
        # For example, you can use matplotlib to create and display the chart


class SearchPanel(wx.Panel): # Might put this in a different file
    def __init__(self, parent):
        super(SearchPanel, self).__init__(parent, style=wx.BORDER_SIMPLE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, wx.ID_ANY, "Select Options:")
        sizer.Add(label, 0, wx.ALL | wx.EXPAND, BORDER)

        self.list_box = wx.ListBox(self, wx.ID_ANY,
                                   choices=["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"],
                                   style=wx.LB_MULTIPLE)
        sizer.Add(self.list_box, 0, wx.ALL | wx.EXPAND, BORDER)

        self.clear_button = wx.Button(self, label="Clear")
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
        date_sizer.Add(self.generate_report_button, 0, wx.ALL | wx.EXPAND, BORDER)

        sizer.Add(date_sizer, 0, wx.ALL | wx.EXPAND, BORDER)
        self.SetSizer(sizer)


class MapPanel(wx.Panel): # Might put this in a different file
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


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "VSADS Visualisation Tool")
    app.MainLoop()
