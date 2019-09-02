from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *

class SpadesPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)

		#Frame: self.readProperties ----------------------------------------------------------

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

		indexReadCateg = 0        #index of read cateogry frame
		self.readCateg = StringVar()   #variable for radioButtons with read categories
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for rc in self.readCategList:
			# value of the radioButton is the index in self.readCategList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rc[0], variable=self.readCateg, value=indexReadCateg)
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')

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
			
		self.readCateg.set(1)

		indexReadCateg += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexReadCateg / 2), columnspan=2, sticky='we')
		indexReadCateg +=2
		
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

		indexReadType = 0 #index of read type
		self.readTypeRadioButtons = []
		
		for rt in self.readTypeList:
			# value of the radioButton is the index in self.readTypeList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rt[0], variable=self.readTypeVar, value=indexReadType)
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')
			self.readTypeRadioButtons.append(rb)
			indexReadCateg += 1
			indexReadType += 1

		self.readTypeVar.set(0)

		indexReadCateg += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexReadCateg / 2), columnspan=2, sticky='we')
		indexReadCateg += 1

		#LIBRARY NUMBER
		self.libraryNumberChoices = ['1', '2', '3', '4', '5', '6', '7', '8']

		self.libraryNumberVar = StringVar()

		indexLibraryNum = 1 #index of library number
		self.libraryNumRadioButtons = []
		
		for lnc in self.libraryNumberChoices:
			# value of the radioButton is the index in self.libraryNumberChoices
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=lnc[0], variable=self.libraryNumberVar, value=indexLibraryNum)
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')
			self.libraryNumRadioButtons.append(rb)
			indexReadCateg += 1
			indexLibraryNum += 1

		self.libraryNumberVar.set(1)

		
	# Helping functions -------------------------------------------------

	# num == 1 -> group of "read type" RadioButtons
	# num == 2 -> group of "library number" RadioButtons
	
	def disableEnable(self, isEnabledReadType, isEnabledLibraryNumber):
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
		






		

		
class PossibleParamsSpades(PossibleParamsParent):
	def __init__(self):
		tags = ["sc", "meta", "rna", "plasmid", "iontorrent", "only-assembler", "careful", "continue", "disable-gzip-outpu", "disable-rr", "dataset", "threads", "memory", "tmp-dir", "cov-cutoff", "phred-offset"]
					
		self.paramDesc = {}

		# ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7"]

		#Basic options:
		self.paramDesc["sc"] = ("this flag is required for MDA (single-cell) data", 1)
		self.paramDesc["meta"] = ("this flag is required for metagenomic sample data", 1)
		self.paramDesc["rna"] = ("this flag is required for RNA-Seq data", 1)
		self.paramDesc["plasmid"] = ("runs plasmidSPAdes pipeline for plasmid detection", 1)
		self.paramDesc["iontorrent"] = ("this flag is required for IonTorrent data", 1)

		#Pipeline options:
		self.paramDesc["only-assembler"] = ("runs only assembling (without read error correction)", 1)
		self.paramDesc["careful"] = ("tries to reduce number of mismatches and short indels", 1)
		self.paramDesc["continue"] = ("continue run from the last available check-point", 1)
		self.paramDesc["disable-gzip-outpu"] = ("forces error correction not to compress the corrected reads", 1)
		self.paramDesc["disable-rr"] = ("disables repeat resolution stage of assembling", 1)

		#Advanced options:
		self.paramDesc["dataset"] = ("file with dataset description in YAML format", 4)
		self.paramDesc["threads"] = ("number of threads [default: 16]", 2)
		self.paramDesc["memory"] = ("RAM limit for SPAdes in Gb (terminates if exceeded) [default: 250]", 2)
		self.paramDesc["tmp-dir"] = ("directory for temporary files [default: <output_dir>/tmp", 4)
		self.paramDesc["cov-cutoff"] = ("coverage cutoff value (a positive float number, or 'auto', or 'off') [default: 'off']", 7)
		self.paramDesc["phred-offset"] = ("PHRED quality offset in the input reads (33 or 64) [default: auto-detect]", 2)

		super().__init__(tags)
