# The model to display the data for the user.

"""" Display Requirements:

For a user-selected period, display the information of all accidents that happened in the period.
For a user-selected period, produce a chart to show the number of accidents in each hour of the day (on average).
For a user-selected period, retrieve all accidents caused by an accident type that contains a keyword (user entered), e.g. collision, pedestrian.
Allow the user to analyze the impact of alcohol in accidents – ie: trends over time, accident types involving alcohol, etc.
One other ‘insight’ or analysis tool of your choice

"""

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        button = wx.Button(panel, label="Click Me!")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.on_button_click, button)

        self.Centre()
        self.Show(True)

    def on_button_click(self, event):
        wx.MessageBox("Button clicked!")

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "Basic wxPython UI")
    app.MainLoop()




