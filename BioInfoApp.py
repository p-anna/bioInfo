import style
import AbyssPopUp as apu
import VelvetPopUp as vpu
from tkinter import *
from tkinter import ttk


class BioInfoApp():

    def __init__(self, master):
        style.styleTheWindow()
        rowcount = 0 # row index for grid of main frame
        self.master = master
        
        frame = ttk.Frame(master, style="M.TFrame")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="MainWindow", style="N.TLabel").grid(row=rowcount, columnspan=2, sticky='w')
        rowcount += 1
        
        ttk.Label(frame, text="Run the Abyss assembly:", style="C.TLabel").grid(row=rowcount, column=0, sticky='w')
        self.abyssInputButt = ttk.Button(frame, text='Abyss', command=self.openAbyss)
        self.abyssInputButt.grid(row=rowcount, column=1, sticky='w', padx=20)
        rowcount += 1

        ttk.Label(frame, text="Run the Velvet assembly:", style="C.TLabel").grid(row=rowcount, column=0, sticky='w')
        self.abyssInputButt = ttk.Button(frame, text='Velvet', command=self.openVelvet)
        self.abyssInputButt.grid(row=rowcount, column=1, sticky='w', padx=20)
        rowcount += 1



    def openAbyss(self):
        root2 = Toplevel(self.master)
        myAppAbyss = apu.AbyssPopUp(root2)

    def openVelvet(self):
        root3 = Toplevel(self.master)
        myAppVelvet = vpu.VelvetPopUp(root3)
