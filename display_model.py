# The model to display the data for the user.

"""
Display Requirements:

For a user-selected period, display the information of all accidents that happened in the period.
For a user-selected period, produce a chart to show the number of accidents in each hour of the day (on average).
For a user-selected period, retrieve all accidents caused by an accident type that contains a keyword (user entered),
e.g. collision, pedestrian.

Allow the user to analyze the impact of alcohol in accidents – ie: trends over time, accident types involving alcohol,
etc.
One other ‘insight’ or analysis tool of your choice - Data Visualisation

"""

import wx
import wx.adv
import datetime


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

        # Load and display the image
        vic_graphic = wx.Image('state_vic_graphic.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        graphic_bitmap = wx.StaticBitmap(self, -1, vic_graphic, (10, 5), (vic_graphic.GetWidth(), vic_graphic.GetHeight()))
        sizer.Add(graphic_bitmap, 0, wx.ALL | wx.CENTER, BORDER)



# Define AccInfoPanel class for notebook
class AccInfoPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Headline Text
        self.headline_text = wx.StaticText(self, style=wx.ALIGN_CENTER,
                                           label="Accident Information")
        sizer.Add(self.headline_text, 0, wx.ALL | wx.EXPAND, BORDER)

        # Config calendar to parameters
        lower_date = wx.DateTime()
        lower_date.Set(1, wx.DateTime.Jul, 2013)
        upper_date = wx.DateTime()
        upper_date.Set(1, wx.DateTime.Feb, 2019)

        # Calendar under the text
        self.cal = wx.adv.CalendarCtrl(self, wx.ID_ANY, lower_date)
        sizer.Add(self.cal, 0, wx.ALL | wx.CENTER, BORDER)

        self.SetSizer(sizer)


# Define MapPanel class for notebook
class MapPanel(wx.Panel):
    def __int__(self, parent):
        super(MapPanel, self).__init__(parent)


# Entry Point
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "VSADS Visualisation Tool")
    app.MainLoop()
