from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *

class AbyssPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)

		#Frame: self.readProperties ----------------------------------------------------------

		# READ CATEGORY LIST
		#("read categ name", "terminalTag")
		self.readCategList = [('single-end reads', "in="),
							  ('paired-end reads', "se=")]

		indexReadCateg = 0        #index of read cateogry frame
		self.readCateg = StringVar()   #variable for radioButtons with read categories
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for rc in self.readCategList:
			# value of the radioButton is the index in self.readCategList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rc[0], variable=self.readCateg, value=indexReadCateg)
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')

			indexReadCateg += 1
			
		self.readCateg.set(1)



		


class PossibleParamsAbyss(PossibleParamsParent):
	def __init__(self):
		

		tags = ["a", "b", "c", "d", "e", "E", "j", "l", "m", "n", "p", "q", "s", "S", "t"]

		#("param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7"]
		self.paramDesc = {}

		# FIXED PARAMETERS


		# OPTIONAL PARAMETERS
		self.paramDesc["a"] = ("maximum number of branches of a bubble [2]", 2, True)
		self.paramDesc["b"] = ("maximum length of a bubble (bp) [""] \n abyss-pe has two bubble popping stages. The default limits are 3*k bp", 2, True)
		self.paramDesc["c"] = ("minimum mean k-mer coverage of a unitig [sqrt(median)]", 2, True)
		self.paramDesc["d"] = ("allowable error of a distance estimate (bp) [6]", 2, True)
		self.paramDesc["e"] = ("minimum erosion k-mer coverage [round(sqrt(median))]", 2, True)
		self.paramDesc["E"] = ("minimum erosion k-mer coverage per strand [1 if sqrt(median) > 2 else 0]", 2, True)
		self.paramDesc["j"] = ("number of threads [2]", 2, True)
		self.paramDesc["l"] = ("minimum alignment length of a read (bp) [40]", 2, True)
		self.paramDesc["m"] = ("minimum overlap of two unitigs (bp) [30]", 2, True)
		self.paramDesc["n"] = ("minimum number of pairs required for building contigs [10]", 2, True)
		self.paramDesc["p"] = ("minimum sequence identity of a bubble [0.9]", 5, True)
		self.paramDesc["q"] = ("minimum base quality when trimming [3] \n Trim bases from the ends of reads whose quality is less q.", 2, True)
		self.paramDesc["s"] = ("minimum unitig size required for building contigs (bp) [1000] \n The seed length should be at least twice the  value  of  k. If  more  sequence  is \n assembled than the expected genome size, try increasing s.", 2, True)
		self.paramDesc["S"] = ("minimum contig size required for building scaffolds (bp) [1000-10000]", 2, True)
		self.paramDesc["t"] = ("maximum length of blunt contigs to trim [k]", 2, True)

		super().__init__(tags)
