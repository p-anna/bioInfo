from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent

class SpadesPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		
		super().__init__(master, name, possibleParamClassInit)	

class PossibleParamsSpades(PossibleParamsParent):
	def __init__(self):
		tags = ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7"]
					
		self.paramDesc = {}

		self.paramDesc["flag=1"] = ("", 1)		
		self.paramDesc["int=2"] = ("", 2)
		self.paramDesc["intlist=3"] = ("", 3)
		self.paramDesc["file=4"] = ("", 4)
		self.paramDesc["float=5"] = ("", 5)
		self.paramDesc["options=6"] = ("", 6, ["a", "b", "c"])
		self.paramDesc["text=7"] = ("", 7)

		super().__init__(tags)
