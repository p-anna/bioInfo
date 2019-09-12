from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *
import subprocess

class AbyssPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)

		#Frame: self.readProperties ----------------------------------------------------------

		indexReadCateg = 0        #index of frame

		ttk.Label(self.readProperties, text= "Please choose the read category of the next input file:", style="HP.TLabel").grid(row=int(indexReadCateg / 2), columnspan=2, sticky='w')
		indexReadCateg += 2
		
		# READ CATEGORY LIST
		#("read categ name", "terminalTag")
		self.readCategList = [('single-end reads', "se="),
							  ('paired-end reads', "in=")]

		self.readCateg = StringVar()   #variable for radioButtons with read categories
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for rc in self.readCategList:
			# value of the radioButton is the index in self.readCategList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rc[0], variable=self.readCateg, value=rc[1])
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')

			indexReadCateg += 1
			
		self.readCateg.set("se=")

	def getFileType(self): #type of input file
		return (self.readCateg.get())

	def whereProgram(self):
		return "abyss-pe"
	

	def runParameterBlocks(self):
		params = [self.whereProgram(), "name=abyss"]
		tmpIN = ""
		tmpSE = ""
		
		for fileName in sorted(self.inputFiles.keys()):
			tmpType = self.inputType[fileName]
			if tmpType == "in=":
				tmpIN += self.cwdParam(fileName) + " "
			elif tmpType == "se=":
				tmpSE += self.cwdParam(fileName) + " "
			else:
				messagebox.showwarning("Error", "Unexpected error in runParameterBlocks function!")
		if tmpIN != "":
			params.append("in=" + tmpIN)
		if tmpSE != "":
			params.append("se=" + tmpSE)

		
		for tag in self.parameterLabels.keys():
			# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
			tmpType = self.getTypeParam(tag)
			tmpValue = self.parameterValues[tag].get()
			#if paramater is a flag and checkbutton is checked
			if tmpType == 1 and tmpValue == 1:
				params.append(tag)
			#if int, intlist, float, options or text
			elif tmpType == 2 or tmpType == 3 or tmpType == 5 or tmpType == 6 or tmpType == 7:
				params.append(tag + "=" + tmpValue)
			#if file or directory
			elif tmpType == 4 or tmpType == 8:
				params.append(tag + "=" +self.cwdParam(tmpValue))

		subprocess.run(params, cwd = self.name)



class PossibleParamsAbyss(PossibleParamsParent):
	def __init__(self):
		

		tags = ["k", "a", "b", "c", "d", "e", "E", "j", "l", "m", "n", "p", "q", "s", "S", "t"]

		#("label text", "param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
		self.paramDesc = {}

		# FIXED PARAMETERS
		self.paramDesc["k"] = ("K-mer length", "K-mer length", 2, False)

		# OPTIONAL PARAMETERS
		self.paramDesc["a"] = ("Max number of branches of a bubble", "Maximum number of branches of a bubble [2]", 2, True)
		self.paramDesc["b"] = ("Max length of a bubble", "Maximum length of a bubble (bp) [""] \n abyss-pe has two bubble popping stages. The default limits are 3*k bp", 2, True)
		self.paramDesc["c"] = ("Min mean k-mer coverage", "Minimum mean k-mer coverage of a unitig [sqrt(median)]", 2, True)
		self.paramDesc["d"] = ("Max error of a distance estimate", "Allowable error of a distance estimate (bp) [6]", 2, True)
		self.paramDesc["e"] = ("Min erosion k-mer coverage", "Minimum erosion k-mer coverage [round(sqrt(median))]", 2, True)
		self.paramDesc["E"] = ("Min erosion k-mer coverage / strand", "Minimum erosion k-mer coverage per strand [1 if sqrt(median) > 2 else 0]", 2, True)
		self.paramDesc["j"] = ("Number of threads", "Number of threads [2]", 2, True)
		self.paramDesc["l"] = ("Min alignment length of a read", "Minimum alignment length of a read (bp) [40]", 2, True)
		self.paramDesc["m"] = ("Min overlap of two unitigs", "Minimum overlap of two unitigs (bp) [30]", 2, True)
		self.paramDesc["n"] = ("Min number of pairs for building contigs", "Minimum number of pairs required for building contigs [10]", 2, True)
		self.paramDesc["p"] = ("Min sequence identity of a bubble", "Minimum sequence identity of a bubble [0.9]", 5, True)
		self.paramDesc["q"] = ("Min base quality when trimming", "Minimum base quality when trimming [3] \n Trim bases from the ends of reads whose quality is less q.", 2, True)
		self.paramDesc["s"] = ("Min unitig size for building contigs", "Minimum unitig size required for building contigs (bp) [1000] \n The seed length should be at least twice the  value  of  k. If  more  sequence  is \n assembled than the expected genome size, try increasing s.", 2, True)
		self.paramDesc["S"] = ("Min contig size for building scaffolds", "Minimum contig size required for building scaffolds (bp) [1000-10000]", 2, True)
		self.paramDesc["t"] = ("Max length of blunt contigs to trim", "Maximum length of blunt contigs to trim [k]", 2, True)

		super().__init__(tags)
