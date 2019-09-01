#import ParamParent as pp
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import subprocess
from tkinter import messagebox
import re


class ParentPopUp:
	def __init__(self, master, name):


		self.kulcsok = ["-a", "-b", "-c", "-d", "-e"]
		self.letezoKulcsok = ["-b", "-e"]

		self.master = master                  # Root of this page
		rowcount = 0                          # row index for grid of main frame
		self.fixParamCount = 0                # number of required parameters

		frame = ttk.Frame(master, style="M.TFrame")
		frame.pack(fill='both', expand=True)

		ttk.Label(frame, text = name, style="N.TLabel").grid(row=rowcount, columnspan=2, sticky='w')
		rowcount += 1

		# read categories +  types +  library numbers in this next frame 
		self.readProperties = ttk.Frame(frame, style="P.TFrame", padding=(10, 10, 10, 10))
		self.readProperties.grid(row=rowcount, columnspan=2, pady=10)
		rowcount += 1

        #--------

		ttk.Label(frame, text="Files with the reads:", style="C.TLabel").grid(row=rowcount, column=0, sticky='w')
		self.buttonUlaz = ttk.Button(frame, text='Choose the input files', command=self.openFileName)
		self.buttonUlaz.grid(row=rowcount, column=1, sticky='w', padx=20)
		rowcount += 1
        
		self.inputFrame = ttk.Frame(frame, style="P.TFrame", padding=(10, 10, 10, 10))
		self.inputFrame.grid(row=rowcount, columnspan=2, pady=10)
		rowcount += 1
            
        #-------- inputFrame
		self.inputFiles = {} # ttk.Button(text=filename)
		self.inputType = {} # ("libraryNumber", "readCategIndex", "readTypeIndex")
		
        #--------

		ttk.Label(frame, text='Parameters:', style="C.TLabel").grid(row=rowcount, column=0, sticky='w')

		self.buttonParams = ttk.Button(frame, text='More parameters', command=self.chooseParams)
		self.buttonParams.grid(row=rowcount, column = 1, sticky='w', padx = 20, pady = 5)
		rowcount += 1

		self.paramFrame = ttk.Frame(frame, style="P.TFrame", padding=(10, 10, 10, 10))
		self.paramFrame.grid(row=rowcount, columnspan=2)
		rowcount += 1
        
        #--------- paramFrame
		self.paramFrameRowcount = 0
		
        
		self.parameterLabels = {}
		self.parameterValues = {}
		self.parameterContainers = {}
		#---------
        
		self.buttonStart = ttk.Button(frame, text='Run ' + name + '!', command=self.runScript)
		self.buttonStart.grid(row=rowcount, columnspan=2, sticky='s', pady=20)
		rowcount += 1

		self.statusLabel = ttk.Label(frame)
		self.statusLabel.grid(row=rowcount, columnspan=2, pady=10)
		rowcount += 1
        
    # ---- end of init ------------------------------------------------------------------- 
    
	# ---- Functionality  -----------------------------------------------------------------------

	def runScript(self):
		print('Validating the parameters...')
		if len(self.inputFiles)==0:
			messagebox.showwarning("Problem with the input files", "No input file is choosen")
		else:
			print('Running of the assembly...')
			self.statusLabel["text"] = "Wait..."
                
			tmpDic = self.determineCommonDict()
               
			parameters = [self.whereProgram()]
                
			self.statusLabel["text"] = "Finished!"
    
            
	def openFileName(self):
		filename = askopenfilename(filetypes =(("Fasta, fastq, sra, sam ..", ("*.fa", "*.fasta", "*.fq", "*.fastq", "*.sam", "*.bam")),("All Files","*.*")),
                                   title = "Choose a file.")
		if not(filename in self.inputFiles) and str(filename) != "()" and str(filename) != "":
			self.inputFiles[filename]=ttk.Button(self.inputFrame, text=self.buttonText(filename),
                                                 style="1I.TButton", command=lambda: self.deleteInputFile(filename))
			self.inputFiles[filename].pack(fill=BOTH, expand=1)
			self.inputType[filename] = (self.libraryNumber.get(), self.readCateg.get(), self.readTypeVar.get())
			#self.inputFileFormat[filename] = self.fileForm.get()
            

	def deleteInputFile(self, text):
		try:
			self.inputFiles[text].destroy()
			del self.inputFiles[text]
		except:
			messagebox.showwarning("Error", "Unexpected error deleteInputFile")

	#################################### implement in specific classes ##############
	def chooseParams(self):
		print("Choose parameters function running")
	##################################################################################
    
	def buttonText(self, filename):
		try:
			m = re.search('.*/(.*)', filename)
			return "x   " + m.group(1)
		except:
			messagebox.showwarning("Error", "Unexpected error buttonText")

	def determineCommonDict(self):
		lista = str(next(iter(self.inputFiles))).split('/')[:-1] #apsoluth path directories
		for key in self.inputFiles.keys(): #for every input file find the common parant dictionary
			tmp = str(key).split('/') 
			n = min(len(lista), len(tmp))
			i = 0
			while i<n and lista[i] == tmp[i] :
				i+=1
			lista = lista[:i]
		return "/".join(lista)              #make an apsoluth path from list of directories
            
	def cwdParam(self, dic):
		currentDir = str(sys.path[0]).split('/')
		currentDir.append('spades')
		destenDir = str(dic).split('/')
		n = min(len(currentDir), len(destenDir))
		i = 0
		while i<n and currentDir[i] == destenDir[i] :
			i+=1
		return '../'*(len(currentDir)-i) + "/".join(destenDir[i:])

	def whereProgram(self):
		return "Here is the program"
		         
	def outputDirectory(self):
		return "Output directory"

	def showAddicionalParams(self):
		print("Show addicional params function running")
		paramFrameRowcount = self.fixParamCount #Fix parameters k-mer length

		self.destroyPreviousParameters()
		
		for k in self.kulcsok:
			if True: #if checkbutton checked
				self.addParameter("-k", 2, [])

	def destroyPreviousParameters(self):
	# destroy labels containers and values for previous parameters
		for k in self.letezoKulcsok:
			try:
				self.parameterLabels[k].destroy()
				self.parameterValues[k].destroy()
				for pCont in self.parameterContainers[k]:
					pCont.destroy()
				del self.parameterLabels[k]
				del self.parameterValues[k]
				for pCont in self.parameterContainers[k]:	
					del pCont
			except:
				messagebox.showwarning("Error", "Unexpected error showAddicionalParams")


	def addParameter(self, tag, typeOfParam, options):
		# using: self.paramFrame & self.paramFrameRowcount
		self.parameterLabels[tag] = ttk.Label(self.paramFrame, text = tag, style="P.TLabel")
		self.parameterLabels[tag].grid(row=self.paramFrameRowcount, column=0, sticky='e')

		self.parameterContainers[tag][0] = ttk.Frame(self.paramFrame, style="P.TFrame")
		self.parameterContainers[tag][0].grid(row=self.paramFrameRowcount, column=1, sticky='e')

		#parameter is a flag
		if(typeOfParam == 1):
			self.parameterValues[tag] = IntVar()
			self.parameterContainers[tag][1] = ttk.Checkbutton(self.parameterContainers[tag][0], style="1.TRadiobutton", text="", variable = self.parameterValues[tag])
			self.parameterContainers[tag][1].grid(row=0, column=0)

		#int, int list, float, string
		elif(typeOfParam == 2 or typeOfParam == 3 or typeOfParam == 5 or typeOfParam == 7):
			self.parameterValues[tag] = StringVar()
			self.parameterContainers[tag][1] = ttk.Entry(self.parameterContainers[tag][0], textvariable = self.parameterValues[tag])
			self.parameterContainers[tag][1].grid(row=0, column=0)

		#file
		elif typeOfParam == 4:
			self.parameterValues[tag] = StringVar()

			self.parameterContainers[tag][2] = ttk.Entry(self.parameterContainers[tag][0], textvariable=self.parameterValues[tag], state="disabled")
			self.parameterContainers[tag][1] = ttk.Button(self.parameterContainers[tag][0], text='Choose the file', command = lambda : self.openFileParam(self.parameterValues[tag]))
			self.parameterContainers[tag][1].grid(row=0, column=0) #button for opening
			self.parameterContainers[tag][2].grid(row=0, column=1) #entry with name of file

		#
		elif typeOfParam == 6:
			self.parameterValues[tag] = StringVar()

			indexContainer = 1 #from 1, 0 is the frame
			for option in options:
				self.parameterContainers[tag][indexContainer] = ttk.Radiobutton(self.parameterContainers[tag][0], style="1.TRadiobutton", text=option, variable = self.parameterValues[tag])
				self.parameterContainers[tag][indexContainer].grid(row=0, column=indexContainer-1)
				indexContainer += 1
		else:
			messagebox.showwarning("Error", "Error with the type of option in function addParameter ")
				
		self.paramFrameRowCount += 1


	def openFileParam(self, buttonFileName):
		filename = askopenfilename(filetypes =(("All Files","*.*")),
                                   title = "Choose a file.")
		if str(filename) != "()" and str(filename) != "":
			buttonFileName.set(filename)
        
