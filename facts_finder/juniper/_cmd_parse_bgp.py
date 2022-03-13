"""Juniper BGP level running-config for bgp section output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC, addressing, IPv4, IPv6

from facts_finder.juniper._cmd_parse_running import Running
from facts_finder.common import blank_line

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

def get_neighbor_or_nbrgrp(spl):
	if spl[0] == "group":
		nbr = spl[1]
	elif spl[0] == "neighbor":
		nbr = spl[1]
	else:
		nbr = None
	return nbr	


class BGP(Running):
	"""object for native BGP running config parser
	"""

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""
		super().__init__(cmd_op)
		# self.bgp_dict = OrderedDict()
		self.op_dict = {}
		self.afl = {}

	def bgp_read(self, func):
		"""directive function to get the various bgp native level output

		Args:
			func (method): method to be executed on bgp native config line

		Returns:
			dict: parsed output dictionary
		"""    		
		toggle, af = False, False
		op_dict = OrderedDict()
		prev_vrf = None
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.find("protocols bgp ") == -1:
				continue
			bgp_spl = l.strip().split(" protocols bgp ")
			spl = bgp_spl[-1].split()
			bgpinstspl = bgp_spl[0].split()
			if bgp_spl[0] == 'set':
				vrf = 'Mgmt-vrf'
			elif bgpinstspl[1] == "routing-instances":
				vrf = bgpinstspl[-1]
			else:
				continue
			if not self.afl.get(vrf): 
				op_dict = OrderedDict()
				self.afl[vrf] = op_dict

			nbr = get_neighbor_or_nbrgrp(spl)
			if not nbr: continue
			if not op_dict.get(nbr): 
				op_dict[nbr] = {}
			try:
				nbr_add = addressing(nbr)
				if isinstance( nbr_add, (IPv4, IPv6)):
					op_dict[nbr]["nbr_type"] = 'neighbor'
				else:
					op_dict[nbr]["nbr_type"] = 'group'
			except: 
				op_dict[nbr]["nbr_type"] = 'group'
				pass			
			nbr_dict = op_dict[nbr]
			func(nbr_dict, l, spl)

		update_dict = merge_vrftype_name_inkey(self.afl)
		self.op_dict.update(update_dict)
		return op_dict

	def bgp_nbr_attributes(self):
		"""update the bgp neighbor attribute details
		"""    		
		func = self.get_nbr_attributes
		merge_dict(self.op_dict, self.bgp_read(func))

	@staticmethod
	def get_nbr_attributes(op_dict, line, spl):
		"""parser function to update bgp neighbor attribute details

		Args:
			port_dict (dict): dictionary with a bgp neighbour info
			l (str): line to parse

		Returns:
			None: None
		""" 
		if "peer-as" in spl: op_dict['remote-as'] = spl[spl.index("peer-as")+1]
		if "local-as" in spl: op_dict['local-as'] = spl[spl.index("local-as")+1]
		if spl[2] == "description": op_dict['description'] = " ".join(spl[3:])
		if spl[2] == "authentication-key": op_dict['password'] = " ".join(spl[3:])
		if "multihop" in spl: op_dict['ebgp-multihop'] = spl[-1]
		if "local-address" in spl: op_dict['update-source'] = spl[-1]
		if op_dict["nbr_type"] == 'group' and spl[2] == 'neighbor': 
			if not op_dict.get('group_members'): op_dict['group_members'] = []
			op_dict['group_members'].append(spl[3])
			if not op_dict.get('member_description'): op_dict['member_description'] = []
			try:
				op_dict['member_description'].append(" ".join(spl[5:]))
			except: pass
 
		## add more as necessary ##
		return op_dict



def merge_vrftype_name_inkey(d):
	"""update vrf and vrf_type in dictionary

	Args:
		d (dict): dictionary with neighbours attributes

	Returns:
		dict: updated dict
	"""    	
	update_dict = {}
	for vrf, vrfattrs in d.items():
		for nbr, vrfattr in vrfattrs.items():
			update_dict[nbr] = vrfattr
			update_dict[nbr]['vrf'] = vrf
			# af = vrftype_spl[-3]
			# update_dict[nbr]['address-family'] = af
	return update_dict


# ------------------------------------------------------------------------------


def get_bgp_running(cmd_op, *args, **kwargs):
	"""defines set of methods executions. to get various bgp native parameters.
	uses BGP in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = BGP(cmd_op)
	R.bgp_nbr_attributes()

	# from pprint import pprint
	# pprint(R.op_dict)

	return R.op_dict
