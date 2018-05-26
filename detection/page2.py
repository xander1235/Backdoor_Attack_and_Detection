
import Tkinter
from tkFileDialog import askopenfilename
from Tkinter import *


def simple(tot,L1,L2,L3):
	master = Tk()
	master.title('Output')

	scrollbar = Scrollbar(master)
	scrollbar.pack(side=RIGHT, fill=Y)
	listbox = Listbox(master,width=500,height=500, yscrollcommand=scrollbar.set)
	listbox.insert(END,'TOTAL BACKDOOR PACKETS :')
	listbox.insert(END,str(tot))
	listbox.insert(END)
	for i in range(len(L1)):
	    listbox.insert(END, L1[i])
	    listbox.insert(END, L2[i])
	    listbox.insert(END, L3[i])
	    
	listbox.pack(side=LEFT, fill=BOTH)

	scrollbar.config(command=listbox.yview)

def page2(tot,L1,L2,L3):
	simple(tot,L1,L2,L3)
	mainloop()
	


