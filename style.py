# Styling of the widgets
from tkinter import ttk
from tkinter import *

def styleTheWindow():
 
      # ---- Button --
      ttk.Style().configure("TButton", background='#3cad5c', font=("MS Serif", 11, "bold"), foreground='#0d471d',
                            height=2, highlightcolor='#bcd3c2', padding=(10, 10, 10, 10), relief='raised')
      ttk.Style().configure("1I.TButton", background='#b0cdfc', font=("MS Serif", 9, "bold"),
                            foreground='#122956', height=0, highlightcolor='#b5c5e5', justify=LEFT,
                            padding=(1, 1, 1, 1), relief='flat')
      ttk.Style().configure("2I.TButton", background='#3ee8a9', font=("MS Serif", 9, "bold"),
                            foreground='#122956', height=0, highlightcolor='#b5c5e5', justify=LEFT,
                            padding=(1, 1, 1, 1), relief='flat')
      ttk.Style().map("TButton", background=[('hover', "#42f462")])
      ttk.Style().map("1I.TButton", background=[('hover', "#ef2809")])
      ttk.Style().map("2I.TButton", background=[('hover', "#ef2809")])

      # ---- Label --
      ttk.Style().configure("TLabel", anchor='w', background='#b8edc0', font=("MS Serif", 11, "bold"),
                            foreground='#0d471d', padding=(10, 10, 10, 10))
      ttk.Style().configure("C.TLabel", background='#b8edc0', font=("MS Serif", 11, "bold"),
                            foreground='#0d471d', padding=(10, 10, 10, 10)) #common label
      ttk.Style().configure("N.TLabel", background='#b8edc0', font=("MS Serif", 16, "bold"),
                            foreground='#0d471d', padding=(10, 10, 10, 10)) #name label
      ttk.Style().configure("P.TLabel", background='#e0f989', font=("MS Serif", 9 , "bold"),
                            foreground='#121c06', padding=(5, 5, 5, 5))     #param label

      # ---- Entry --
      ttk.Style().configure("TEntry", background='#c7e560', font=("MS Serif", 9, "bold"),
                            foreground='#121c06', selectbackground='#6a6ced')

      # ---- Frame --
      ttk.Style().configure("TFrame",  background='#b8edc0', borderwidth=2, relief='ridge', width=max)
      ttk.Style().configure("P.TFrame", background='#e0f989') #param frame
      ttk.Style().configure("M.TFrame", background='#b8edc0') #main frame

      # ---- Progressbar --
      ttk.Style().configure("TProgressbar", background="#b3ef26", foreground='#0d471d')

      # ---- Radiobutton --
      ttk.Style().configure("TRadiobutton", background='#e0f989', font=("MS Serif", 9, "bold"), foreground='#0d471d',
                            height=2, highlightcolor='#bcd3c2', padding=(10, 10, 10, 10), relief='raised')
      ttk.Style().map("1.TRadiobutton", background=[('hover', "#b0cdfc")])
      ttk.Style().map("2.TRadiobutton", background=[('hover', "#3ee8a9")])


   
        
