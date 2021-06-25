import wx
class Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(-1, -1))
        self.panel = wx.Panel(self)
        #self.Show()

    def GetName(self):

        dlg = wx.TextEntryDialog(self.panel, 'Ingresa el criterio de prioridad\n arr, abj, der, izq',"Criterio de prioridad","", 
                style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return dlg.GetValue()

    def OnCloseWindow(self, e):
        self.Destroy()