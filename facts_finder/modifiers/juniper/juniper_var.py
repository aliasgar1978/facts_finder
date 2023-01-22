
from nettoolkit import *
import pandas as pd

from facts_finder.modifiers.commons import *
from .commands.cmd_dict import *
# ================================================================================================
# Cisco  Var  DB
# ================================================================================================
class VarJuniper(DataFrameInit, Var):
	
	def __init__(self, capture, cmd_lst=None):
		self.var = {}
		self.cmd_lst=cmd_lst
		if not self.cmd_lst:
			self.cmd_lst = cmd_lst_var
		super().__init__(capture)

	def __call__(self):
		self.update_device('show version | no-more')
		self.convert_to_dataframe()

	## Calls




# ================================================================================================