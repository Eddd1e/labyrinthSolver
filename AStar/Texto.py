import wx
import copy
from celda import Celda
class Frame(wx.Frame):
    def __init__(self, parent, costos):
        wx.Frame.__init__(self, parent)

        self.panel = wx.Panel(self)     
        self.quote = wx.StaticText(self.panel, label="Mono")
        self.quote2 = wx.StaticText(self.panel, label="Pulpo")

        self.costos = costos

        self.button = wx.Button(self.panel, label="Guardar Costos")

        self.labels = []
        self.costosMono = []
        self.costosPulpo = []

        self.nuevo = "Bosque"
        tiles = ["Montaña", "Tierra", "Agua", "Arena", "Bosque"]
        self.nuevoTile = wx.TextCtrl(self.panel, size=(60, -1))
        self.combo = wx.ComboBox(self,-1,choices=tiles,size=(100,25), style = wx.CB_READONLY)

        self.labels.append(wx.StaticText(self.panel, label="Montaña:"))
        self.costosMono.append(wx.TextCtrl(self.panel, size=(60, -1)))
        self.costosPulpo.append(wx.TextCtrl(self.panel, size=(60, -1)))

        self.labels.append(wx.StaticText(self.panel, label="Tierra:"))
        self.costosMono.append(wx.TextCtrl(self.panel, size=(60, -1)))
        self.costosPulpo.append(wx.TextCtrl(self.panel, size=(60, -1)))

        self.labels.append(wx.StaticText(self.panel, label="Agua:"))
        self.costosMono.append(wx.TextCtrl(self.panel, size=(60, -1)))
        self.costosPulpo.append(wx.TextCtrl(self.panel, size=(60, -1)))

        self.labels.append(wx.StaticText(self.panel, label="Arena:"))
        self.costosMono.append(wx.TextCtrl(self.panel, size=(60, -1)))
        self.costosPulpo.append(wx.TextCtrl(self.panel, size=(60, -1)))

        self.labels.append(wx.StaticText(self.panel, label="Bosque:"))
        self.costosMono.append(wx.TextCtrl(self.panel, size=(60, -1)))
        self.costosPulpo.append(wx.TextCtrl(self.panel, size=(60, -1)))

        self.x_text = wx.StaticText(self.panel, label="x:")
        self.y_text = wx.StaticText(self.panel, label="y:")

        self.x_ctrl = wx.TextCtrl(self.panel, size=(60, -1))
        self.y_ctrl = wx.TextCtrl(self.panel, size=(60, -1))  
        
        for i in range(len(costos)):
            self.costosMono[i].SetValue(str(costos[str(i)][0]))
            self.costosPulpo[i].SetValue(str(costos[str(i)][1]))
        
        # Set sizer for the frame, so we can change frame size to match widgets
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        

        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(10, 5)

        self.sizer.Add(self.quote, (0, 1))
        self.sizer.Add(self.quote2, (0, 2))

        for i in range(1,6):
            self.sizer.Add(self.labels[i-1], (i, 0))
            self.sizer.Add(self.costosMono[i-1], (i, 1))
            self.sizer.Add(self.costosPulpo[i-1], (i, 2))
        
        
        self.sizer.Add(self.button, (6, 0), flag=wx.BOTTOM)

        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 8)

        # Use the sizers
        self.panel.SetSizerAndFit(self.border)  
        self.SetSizerAndFit(self.windowSizer)  

        # Set event handlers
        self.button.Bind(wx.EVT_BUTTON, self.onButton)



    def onButton(self,e):
        for i in range(5):
            self.costos[str(i)]= [int(self.costosMono[i].GetValue()), int(self.costosPulpo[i].GetValue()) ]
        



    def onClose(self, event):
        self.Close()

