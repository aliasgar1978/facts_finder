

from nettoolkit import JSet
from facts_finder.common import verifid_output


class Running():

	def __init__(self, cmd_op):
		self.cmd_op = cmd_op
		JS = JSet(input_list=cmd_op)
		JS.to_set
		self.set_cmd_op = verifid_output(JS.output)
