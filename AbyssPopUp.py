from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent

class AbyssPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)		


class PossibleParamsAbyss(PossibleParamsParent):
	def __init__(self):
		

		tags = ["a", "b", "c", "d", "e", "E", "j", "l", "m", "n", "p", "q", "s", "S", "t"]
		
		self.paramDesc = {}

		#["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7"]
		
		self.paramDesc["a"] = ("maximum number of branches of a bubble [2]", 2)
		self.paramDesc["b"] = ("maximum length of a bubble (bp) [""] \n abyss-pe has two bubble popping stages. The default limits are 3*k bp", 2)
		self.paramDesc["c"] = ("minimum mean k-mer coverage of a unitig [sqrt(median)]", 2)
		self.paramDesc["d"] = ("allowable error of a distance estimate (bp) [6]", 2)
		self.paramDesc["e"] = ("minimum erosion k-mer coverage [round(sqrt(median))]", 2)
		self.paramDesc["E"] = ("minimum erosion k-mer coverage per strand [1 if sqrt(median) > 2 else 0]", 2)
		self.paramDesc["j"] = ("number of threads [2]", 2)
		self.paramDesc["l"] = ("minimum alignment length of a read (bp) [40]", 2)
		self.paramDesc["m"] = ("minimum overlap of two unitigs (bp) [30]", 2)
		self.paramDesc["n"] = ("minimum number of pairs required for building contigs [10]", 2)
		self.paramDesc["p"] = ("minimum sequence identity of a bubble [0.9]", 5)
		self.paramDesc["q"] = ("minimum base quality when trimming [3] \n Trim bases from the ends of reads whose quality is less q.", 2)
		self.paramDesc["s"] = ("minimum unitig size required for building contigs (bp) [1000] \n The seed length should be at least twice the  value  of  k. If  more  sequence  is \n assembled than the expected genome size, try increasing s.", 2)
		self.paramDesc["S"] = ("minimum contig size required for building scaffolds (bp) [1000-10000]", 2)
		self.paramDesc["t"] = ("maximum length of blunt contigs to trim [k]", 2)

		super().__init__(tags)
