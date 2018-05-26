#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
from tkFileDialog import askopenfilename
from tkMessageBox import *
from detection import test


class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
	self.minsize(width=500, height=500)
        self.maxsize(width=500, height=500)
        self.grid()

        button = Tkinter.Button(self,text=u"Input pcap File",font=("Arial",13),command=self.OnButtonClick)
	button2 = Tkinter.Button(self,text=u"  Developers   ",font=("Arial",13),command=self.OnButtonClick2)
	button.place(x = 170,y = 150)
	button2.place(x = 170,y = 190)
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="Black",font=("Helvetica", 25))
        label.grid(column=2,row=2,columnspan=20,sticky='EW')
        self.labelVariable.set(u"       Backdoor Detection Tool     ")
	var = Tkinter.StringVar()
	var.set(u"Select an input File:")
	label2 = Tkinter.Label(self,textvariable = var ,anchor = "w",fg = "Black",font=("Arial",15))
	label2.place(x=40,y= 100)
	self.grid_columnconfigure(8,weight=5)
	self.resizable(True,False)
	self.update()
	self.geometry(self.geometry())

    def OnButtonClick(self):
	self.filename = askopenfilename()
	test(self.filename)
	
    def OnButtonClick2(self):
        showinfo('Developers','Sindhu Kesaboina-ICM2015004\nAnusha Nimmala-IIT2015116\nVallambatla Niharika-IIT2015118\nSama Praveen-IIT2015137\nRathod Veerender-IWM2015006')
    def OnPressEnter(self,event):
	self.a = self.entryVariable.get()
	


def Run():
    app = simpleapp_tk(None)
    app.title('Backdoor Detection Tool')
    app.mainloop()
Run()
