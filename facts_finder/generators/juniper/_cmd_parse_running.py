"""juniper set config initiator - parent """

from facts_finder.generators.commons import *
from .common import *


class Running():
	"""parent object for config parser

	Args:
		cmd_op (list, str): config output, either list of multiline string
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output
		"""    		    		
		self.cmd_op = cmd_op
		JS = JSet(input_list=cmd_op)
		JS.to_set
		self.set_cmd_op = verifid_output(JS.output)
