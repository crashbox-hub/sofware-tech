import wx
import wx.adv

from middle import MapPanel, HomePanel, AccInfoPanel


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


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "VSADS Visualisation Tool")
    app.MainLoop()
