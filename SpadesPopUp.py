from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *


class SpadesPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)

		#Frame: self.readProperties ----------------------------------------------------------

		indexReadCateg = 0        #index of read cateogry frame
		
		ttk.Label(self.readProperties, text= "Please choose the read category of the next input file:", style="HP.TLabel").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='w')
		indexReadCateg += 3

		# READ CATEGORY LIST
		#("read categ name", "terminalTag", isReadTypeNeeded, isLibraryNumberNeeded)
		self.readCategList = [("single-end", "--s", False, True),
							  ("paired-end", "--pe", True, True),
							  ("mate-pair", "--mp", True, True),
							  ("high-quality mate-pair", "--hqmp", True, True),
							  ("Lucigen NxMat", "--nxmate", True, True),
							  ('Sanger', "--sanger", False, False),
							  ('PacBio',  "--pacbio", False, False),
							  ('Nanopore', "--nanopore", False, False),
							  ('TSLR-contigs', "--tslr", False, False),
							  ('trusted contigs', "--trusted-contigs", False, False),
							  ('untrusted contigs', "--untrusted-contigs", False, False)]

		self.readCateg = StringVar()   #variable for radioButtons with read categories
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for rc in self.readCategList:
			# value of the radioButton is its terminalTag
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rc[0], variable=self.readCateg, value=rc[1])
			rb.grid(row=int(indexReadCateg / 3), column=(indexReadCateg % 3), sticky='w')

			#should the "read type" and "library number" group be enabled for this read category?
			#isReadTypeNeeded, isLibraryNumberNeeded
			if rc[2] and rc[3]:
				rb.configure(command=lambda: self.disableEnable(True, True))
			elif rc[2] and not(rc[3]):
				rb.configure(command=lambda: self.disableEnable(True, False))
			elif not(rc[2]) and rc[3]:
				rb.configure(command=lambda: self.disableEnable(False, True))
			elif not(rc[2]) and not(rc[3]):
				rb.configure(command=lambda: self.disableEnable(False, False))
			else:
				messagebox.showwarning("Error", "Unexpected error with isReadTypeNeeded and isLibraryNumberNeeded")
			indexReadCateg += 1
			
		self.readCateg.set("--pe")

		indexReadCateg += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='we')
		indexReadCateg +=3

		ttk.Label(self.readProperties, text="Please choose the type of reads in the next input file:", style="HP.TLabel").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='w')
		indexReadCateg += 3
		
		#READ TYPE LIST
		#("read type name", "terminalTag)
		self.readTypeList = [('forward reads', "-1"),
							 ('reverse reads', "-2"),
							 ('interlaced reads', "-12"),
							 ('merged reads', "-m"),
							 ('unpaired reads', "-s"),
							 ("forward-reverse orientation", "-fr"),
							 ("reverse-forward orientation", "-rf"),
							 ("forward-forward orientation", "-ff")]
		
		self.readTypeVar = StringVar()

		self.readTypeRadioButtons = []
		
		for rt in self.readTypeList:
			# value of the radioButton is its terminalTag
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rt[0], variable=self.readTypeVar, value=rt[1])
			rb.grid(row=int(indexReadCateg / 3), column=(indexReadCateg % 3), sticky='w')
			self.readTypeRadioButtons.append(rb)
			indexReadCateg += 1

		self.readTypeVar.set("-1")
		self.isEnabledReadType = True


		indexReadCateg += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='we')
		indexReadCateg += 3

		ttk.Label(self.readProperties, text="Please choose the library number of the next input file:", style="HP.TLabel").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='w')
		indexReadCateg += 3

		#LIBRARY NUMBER
		self.libraryNumberChoices = [('1', '-1'),
									 ('2', '-2'),
									 ('3', '-3'),
									 ('4', '-4'),
									 ('5', '-5'),
									 ('6', '-6')]

		self.libraryNumberVar = StringVar()

		self.libraryNumRadioButtons = []
		
		for lnc in self.libraryNumberChoices:
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=lnc[0], variable=self.libraryNumberVar, value=lnc[1])
			rb.grid(row=int(indexReadCateg / 3), column=(indexReadCateg % 3), sticky='w')
			self.libraryNumRadioButtons.append(rb)
			indexReadCateg += 1

		self.libraryNumberVar.set('-1')
		self.isEnabledLibraryNumber = True
		
		
	# Helping functions -------------------------------------------------

	def disableEnable(self, isEnabledReadType, isEnabledLibraryNumber):
		self.isEnabledReadType = isEnabledReadType
		self.isEnabledLibraryNumber = isEnabledLibraryNumber

		if(isEnabledReadType):
			stateText = NORMAL
		else:
			stateText = DISABLED

		for rtrb in self.readTypeRadioButtons:
			rtrb.configure(state = stateText)

		if(isEnabledLibraryNumber):
			stateText = NORMAL
		else:
			stateText = DISABLED
			
		for lnrb in self.libraryNumRadioButtons:
			lnrb.configure(state = stateText)

		
	def getFileType(self): #type of input file
		tmpFileType = self.readCateg.get()
		if self.isEnabledReadType:
			tmpFileType += self.readTypeVar.get()
		if self.isEnabledLibraryNumber:
			tmpFileType += self.libraryNumberVar.get()
		return tmpFileType
	

	def whereProgram(self):
		currentDir = str(sys.path[0]).split('/')
		goBack = len(currentDir) - 3 + 1    
		return goBack * "../" + "programs/spades/bin/spades.py"

	def runParameterBlocks(self):
		params = [self.whereProgram()]

		for fileName, fileType in self.inputType.items():
			params.append(fileType)
			params.append(self.cwdParam(fileName))

		
		for tag in self.parameterLabels.keys():
			# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
			tmpType = self.possibleParameters.paramDesc[tag][1]
			tmpValue = self.parameterValues[tag].get()
			#if paramater is a flag and checkbutton is checked
			if tmpType == 1 and tmpValue == "1":
				params.apped(tag)
			#if int, intlist, float, options or text
			elif tmpType == 2 or tmpType == 3 or tmpType == 5 or tmpType == 6 or tmpType == 7:
				params.append(tag)
				params.append(tmpValue)
			#if file or directory
			elif tmpType == 4 or tmpType == 8:
				params.append(tag)
				params.append(self.cwdParam(tmpValue)) #### CHECK THIS
				
		params.append("-o")
		params.append(".")
		
		return [params]
				
	def cwdParam(self, dic):
		currentDir = str(sys.path[0]).split('/')
		currentDir.append('spades')
		destenDir = str(dic).split('/')
		n = min(len(currentDir), len(destenDir))
		i = 0
		while i<n and currentDir[i] == destenDir[i] :
			i+=1
		return '../'*(len(currentDir)-i) + "/".join(destenDir[i:])
			

		
		
		
class PossibleParamsSpades(PossibleParamsParent):
	def __init__(self):
		tags = ["-k", "--sc", "--meta", "--rna", "--plasmid", "--iontorrent", "--only-assembler", "--careful", "--continue", "--disable-gzip-outpu", "--disable-rr", "--dataset", "--threads", "--memory", "--tmp-dir", "--cov-cutoff", "--phred-offset"]

		#("param description", type, isOptionalParam, [options])
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
		self.paramDesc = {}

		# FIXED PARAMETERS
		self.paramDesc["-k"] = ("K-mer length", 3, False)
		
		# OPTIONAL PARAMETERS
		#Basic options:
		self.paramDesc["--sc"] = ("this flag is required for MDA (single-cell) data", 1, True)
		self.paramDesc["--meta"] = ("this flag is required for metagenomic sample data", 1, True)
		self.paramDesc["--rna"] = ("this flag is required for RNA-Seq data", 1, True)
		self.paramDesc["--plasmid"] = ("runs plasmidSPAdes pipeline for plasmid detection", 1, True)
		self.paramDesc["--iontorrent"] = ("this flag is required for IonTorrent data", 1, True)

		#Pipeline options:
		self.paramDesc["--only-assembler"] = ("runs only assembling (without read error correction)", 1, True)
		self.paramDesc["--careful"] = ("tries to reduce number of mismatches and short indels", 1, True)
		self.paramDesc["--continue"] = ("continue run from the last available check-point", 1, True)
		self.paramDesc["--disable-gzip-outpu"] = ("forces error correction not to compress the corrected reads", 1, True)
		self.paramDesc["--disable-rr"] = ("disables repeat resolution stage of assembling", 1, True)

		#Advanced options:
		self.paramDesc["--dataset"] = ("file with dataset description in YAML format", 4, True)
		self.paramDesc["--threads"] = ("number of threads [default: 16]", 2, True)
		self.paramDesc["--memory"] = ("RAM limit for SPAdes in Gb (terminates if exceeded) [default: 250]", 2, True)
		self.paramDesc["--tmp-dir"] = ("directory for temporary files [default: <output_dir>/tmp", 8, True)
		self.paramDesc["--cov-cutoff"] = ("coverage cutoff value (a positive float number, or 'auto', or 'off') [default: 'off']", 7, True)
		self.paramDesc["--phred-offset"] = ("PHRED quality offset in the input reads (33 or 64) [default: auto-detect]", 6, True, ["33", "64"])

		super().__init__(tags)

		
