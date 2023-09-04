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

# Custom class from wc.Frame
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(500, 400))

        # notebook for multiple tabs
        notebook = wx.Notebook(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        notebook.SetSizer(sizer)

        # button = wx.Button(notebook, label="Click Me!")

        home_panel = HomePanel(notebook)
        notebook.AddPage(home_panel, "Home")

        accinfo_panel = AccInfoPanel(notebook)
        notebook.AddPage(accinfo_panel, "Accident Info")

        map_panel = MapPanel(notebook)
        notebook.AddPage(map_panel, "Map")

        self.Centre()
        self.Show(True)

"""
# For the on_button_click function
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.Bind(wx.EVT_BUTTON, self.on_button_click, button)
"""
"""
    # Function on_button_click
    def on_button_click(self, event):
        wx.MessageBox("Button clicked!")
"""

#Define HomePanel class for notebook
class HomePanel(wx.Panel):
    def __int__(self, parent):
        super(HomePanel, self).__init__(parent)
        home_text = wx.StaticText(self, label="Home Tab Welcome Here!")
        sizer = wx.BoxSizer(wx.VERTICAL)

#Define AccInfoPanel class for notebook
class AccInfoPanel(wx.Panel):
    def __int__(self, parent):
        super(AccInfoPanel, self).__init__(parent)
        acc_info_text = wx.StaticText(self, label="Acc Info Tab Welcome Here!")
        sizer = wx.BoxSizer(wx.VERTICAL)

#Define MapPanel class for notebook
class MapPanel(wx.Panel):
    def __int__(self, parent):
        super(MapPanel, self).__init__(parent)
        map_text = wx.StaticText(self, label="Home Tab Welcome Here!")
        sizer = wx.BoxSizer(wx.VERTICAL)



# Entry Point
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "Basic wxPython UI")
    app.MainLoop()




