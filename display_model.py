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

        # Date Picker for Start Date
        self.start_date_picker = DatePickerPanel(self, label="Select Start Date:", initial_date=lower_date)
        sizer.Add(self.start_date_picker, 0, wx.ALL | wx.EXPAND, BORDER)

        # Date Picker for End Date
        self.end_date_picker = DatePickerPanel(self, label="Select End Date:", initial_date=upper_date)
        sizer.Add(self.end_date_picker, 0, wx.ALL | wx.EXPAND, BORDER)

        # Calendar under the text
        self.cal = wx.adv.CalendarCtrl(self, wx.ID_ANY, lower_date)
        sizer.Add(self.cal, 0, wx.ALL | wx.CENTER, BORDER)

        self.SetSizer(sizer)

# Define MapPanel class for notebook
class MapPanel(wx.Panel):
    def __int__(self, parent):
        super(MapPanel, self).__init__(parent)

# Define DatePickerPanel class
class DatePickerPanel(wx.Panel):
    def __init__(self, parent, label="Select Date:", initial_date=None):
        super(DatePickerPanel, self).__init__(parent)

        # Create a date picker control
        self.date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, dt=initial_date, style=wx.adv.DP_DEFAULT)

        # Create a label for the date picker
        date_label = wx.StaticText(self, label=label)

        # Create a sizer to arrange the label and date picker
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(date_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, BORDER)
        sizer.Add(self.date_picker, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, BORDER)
        self.SetSizer(sizer)

# Entry Point
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "VSADS Visualisation Tool")
    app.MainLoop()
