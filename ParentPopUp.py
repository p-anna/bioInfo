#import ParamParent as pp
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import subprocess
from tkinter import messagebox
import re


class ParentPopUp:
	def __init__(self, master, name):

		self.master = master                  # Root of this page
		rowcount = 0                          # row index for grid of main frame

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

        
		self.addicionalParamsLabel = {}
		self.addicionalParamsEntry = {}
        
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
		if not(filename in self.inputFiles) and str(filename) != "()":
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

	def showAddicionalParams(self):
		print("Show addicional params function running")
    
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


	def addParameter(self, oznaka, tip, opcije):
		# using: self.paramFrame & self.paramFrameRowcount
		if(tip == 1): #parameter is a flag
			
