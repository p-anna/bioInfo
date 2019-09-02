from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent

class SpadesPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		
		super().__init__(master, name, possibleParamClassInit)	

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
