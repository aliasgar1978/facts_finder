
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.common import get_device_manufacturar
from facts_finder.common import dataframe_generate
from facts_finder.cisco_parser import Cisco
from facts_finder.cisco_parser import cisco_cmds_list
from facts_finder.cisco_parser import cisco_cmds_op_hierachy_level
from facts_finder.juniper_parser import Juniper
from facts_finder.juniper_parser import juniper_cmds_list
from facts_finder.juniper_parser import juniper_cmds_op_hierachy_level

merge_dict = DIC.merge_dict

class DeviceDB():

	def __init__(self):
		self.config = OrderedDict()

	def __getitem__(self, k): return self.config[k]
	def __setitem__(self, k, v): self.config[k] = v
	def __iter__(self):
		for k, v in self.config.items(): yield k,v
	def keys(self): return self.config.keys()

	def evaluate(self, device):
		cl_hl = get_cmd_hierachylevels(device)
		cmds_list = cl_hl['cmds_list']
		hierachy_levels = cl_hl['hierachy_levels']
		for cmd, kwargs in cmds_list.items():
			parsed_op = device.parse(cmd, self, **kwargs)
			if isinstance(hierachy_levels[cmd], str):
				self.update_hierarcy(hierachy_levels[cmd], parsed_op)
			elif isinstance(hierachy_levels[cmd], tuple):
				for i, hierachy_level in enumerate(hierachy_levels[cmd]):
					self.update_hierarcy(hierachy_level, parsed_op[i])
		# pprint(self.config)
		return self.convert_dict_to_df()

	def update_hierarcy(self, hierarchy, content=None):
		if not content: return None
		if not self.config.get(hierarchy):
			self[hierarchy] = OrderedDict()
		merge_dict(self.config[hierarchy], content)

	def convert_dict_to_df(self):
		df_dict = {}
		for k, v in self:
			df = dataframe_generate(v)
			df.index.name = k
			df_dict[k] = df
		return df_dict


def device(file):
	dev_manu = get_device_manufacturar(file)
	if dev_manu == "Cisco":  return Cisco(file)
	if dev_manu == "Juniper": return Juniper(file)
	raise TypeError("Device configuration Unidentified, please re-check")

def get_cmd_hierachylevels(device):
	if isinstance(device, Cisco):
		cmds_list = cisco_cmds_list
		hierachy_levels = cisco_cmds_op_hierachy_level
	elif isinstance(device, Juniper):
		cmds_list = juniper_cmds_list
		hierachy_levels = juniper_cmds_op_hierachy_level
	else:
		raise TypeError("Device configuration Unidentified, please re-check")
	return {'cmds_list': cmds_list, 'hierachy_levels': hierachy_levels}

