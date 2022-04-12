"""cisco running-config system level command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.common import verifid_output

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningSystem():
	"""object for running config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		
		self.cmd_op = verifid_output(cmd_op)
		self.system_dict = {}


	def system_management_ip(self):
		"""get the device management ip address
		"""    		
		src_mgmt_vl, ifconf = '', False
		for l in self.cmd_op:
			if not src_mgmt_vl and l.find('source-interface')>0: 
				src_mgmt_vl=l.strip().split()[-1]
			if src_mgmt_vl:
				if not ifconf and l.startswith('interface ') and l.find(src_mgmt_vl) > 0:
					ifconf = True
				if ifconf:
					if l.startswith('ip address'):
						return(l.strip().split()[-2])

	def system_exec_banner(self):
		"""get the device exec banner
		"""
		banner, banner_start = "", False
		for l in self.cmd_op:
			if l.startswith("banner exec "):
				banner_start = True
				spl = l.strip().split()
				banner_starter = spl[2]
				l = " ".join(spl[3:])
			if banner_start: banner += l
			if banner_start and l.strip().endswith(banner_starter):
				break
		return banner

# ------------------------------------------------------------------------------


def get_system_running(cmd_op, *args, **kwargs):
	"""defines set of methods executions. to get various system parameters.
	uses RunningSystem in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningSystem(cmd_op)
	R.system_dict['management_ip'] = R.system_management_ip()
	R.system_dict['banner'] = R.system_exec_banner()
	# # update more interface related methods as needed.

	return R.system_dict
