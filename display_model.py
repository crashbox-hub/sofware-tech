import wx
import wx.adv
import datetime
import pandas as pd
import matplotlib.pyplot as plt

BORDER = 5

# Custom class from wx.Frame
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetMinSize(wx.Size(500, 500))
        notebook = wx.Notebook(self)

        # notebook for multiple tabs
        notebook.SetSizer(sizer)
        home_panel = HomePanel(notebook)
        notebook.AddPage(home_panel, "Home")
        accident_info_panel = AccInfoPanel(notebook)
        notebook.AddPage(accident_info_panel, "Accident Info")
        map_panel = MapPanel(notebook)
        notebook.AddPage(map_panel, "Map")

        self.Centre()
        self.Show(True)

# Define HomePanel class for notebook
class HomePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Headline Text
        self.headline_text = wx.StaticText(self, style=wx.ALIGN_CENTER,
                                           label="Accident Information")
        sizer.Add(self.headline_text, 0, wx.ALL | wx.EXPAND, BORDER)

        # Load and display the image centered in the panel, resizes to the window size
        vic_graphic = wx.Image('state_vic_graphic.jpg', wx.BITMAP_TYPE_ANY).Scale(200, 200)
        graphic_bitmap = wx.StaticBitmap(self, -1, vic_graphic.ConvertToBitmap(), (0, 0),
                                         (vic_graphic.GetWidth(), vic_graphic.GetHeight()))
        sizer.Add(graphic_bitmap, 0, wx.ALL | wx.CENTER, BORDER)

        self.SetSizer(sizer)

# Define AccInfoPanel class for notebook
class AccInfoPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Search bar with magnifying glass icon in the top left corner
        search_panel = SearchPanel(self)
        sizer.Add(search_panel, 0, wx.ALL, BORDER)

        # Right side content
        content_sizer = wx.BoxSizer(wx.VERTICAL)

        # Headline Text
        self.headline_text = wx.StaticText(self, style=wx.ALIGN_CENTER,
                                           label="Accident Information")
        content_sizer.Add(self.headline_text, 0, wx.ALL | wx.EXPAND, BORDER)

        sizer.Add(content_sizer, 1, wx.EXPAND)
        self.SetSizer(sizer)

# Define SearchPanel class for the search bar and date picker
# Define SearchPanel class for the search bar and date picker
class SearchPanel(wx.Panel):
    def __init__(self, parent):
        super(SearchPanel, self).__init__(parent, style=wx.BORDER_SIMPLE)

        # Set up vertical box sizer for the search bar
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Dropdown menu with options
        options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
        self.choice = wx.Choice(self, choices=options)
        sizer.Add(self.choice, 0, wx.ALL | wx.EXPAND, BORDER)

        # Create a sizer for date selections
        date_sizer = wx.BoxSizer(wx.VERTICAL)

        # Config calendar to parameters
        lower_date = wx.DateTime()
        lower_date.Set(1, wx.DateTime.Jul, 2013)
        upper_date = wx.DateTime()
        upper_date.Set(1, wx.DateTime.Feb, 2019)

        # Create a text field for start date
        self.start_date_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        date_sizer.Add(self.start_date_text, 0, wx.ALL | wx.EXPAND, BORDER)

        # Create a calendar icon button for start date
        cal_graphic = wx.Image('calendar.jpg', wx.BITMAP_TYPE_ANY).Scale(10, 10)
        start_date_calendar_icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(cal_graphic, wx.BITMAP_TYPE_PNG))
        date_sizer.Add(start_date_calendar_icon, 0, wx.ALL, BORDER)

        # Create a date picker control for start date
        self.start_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, dt=lower_date, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        date_sizer.Add(self.start_date_picker, 0, wx.ALL | wx.EXPAND, BORDER)

        # Create a text field for end date
        self.end_date_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        date_sizer.Add(self.end_date_text, 0, wx.ALL | wx.EXPAND, BORDER)

        # Create a calendar icon button for end date
        end_date_calendar_icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(cal_graphic, wx.BITMAP_TYPE_PNG))
        date_sizer.Add(end_date_calendar_icon, 0, wx.ALL, BORDER)

        # Create a date picker control for end date
        self.end_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, dt=upper_date, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        date_sizer.Add(self.end_date_picker, 0, wx.ALL | wx.EXPAND, BORDER)

        # Create "Alcohol Related?" checkbox
        self.alcohol_related_checkbox = wx.CheckBox(self, label="Alcohol Related?")
        date_sizer.Add(self.alcohol_related_checkbox, 0, wx.ALL | wx.EXPAND, BORDER)

        # Create "Generate Report" button
        self.generate_report_button = wx.Button(self, label="Generate Report")
        date_sizer.Add(self.generate_report_button, 0, wx.ALL | wx.EXPAND, BORDER)

        sizer.Add(date_sizer, 0, wx.ALL | wx.EXPAND, BORDER)

        self.SetSizer(sizer)



# Define MapPanel class for notebook
class MapPanel(wx.Panel):
    def __init__(self, parent):
        super(MapPanel, self).__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

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
        sizer.Add(graphic_bitmap, 0, wx.ALL | wx.CENTER, BORDER)

        self.SetSizer(sizer)

# Entry Point
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "VSADS Visualisation Tool")
    app.MainLoop()
