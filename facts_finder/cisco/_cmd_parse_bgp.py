"""cisco BGP level running-config for bgp section output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.cpw_cracker import decrypt_type7
from facts_finder.common import verifid_output
from facts_finder.common import blank_line

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class BGP_Papa():
	"""parent object for BGP level running config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		    		
		self.cmd_op = verifid_output(cmd_op)
		self.op_dict = {}

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
		if spl[2] == "remote-as": op_dict['remote-as'] = spl[-1]
		if spl[2] == "update-source": op_dict['update-source'] = spl[-1]
		if spl[2] == "ebgp-multihop": op_dict['ebgp-multihop'] = spl[-1]
		if spl[2] == "unsuppress-map" : op_dict["unsuppress-map"] = spl[-1]
		if spl[-2] == "peer-group": op_dict["peer-group"] = spl[-1]

		if spl[2] == "password":
			op_dict["password"] = decrypt_type7(spl[-1]) if spl[3] == "7" else spl[-1]

		if spl[2] == "route-map" and spl[-1] == "in": op_dict["route-map in"] = spl[-2]
		if spl[2] == "route-map" and spl[-1] == "out": op_dict["route-map out"] = spl[-2]

		if spl[2] == "local-as": op_dict['local-as'] = spl[3]
		if spl[2] == "description": op_dict['description'] = " ".join(spl[3:])
		## add more as necessary ##
		return op_dict


class AddressFamily(BGP_Papa):
	"""object for address-family BGP running config parser
	"""

	def bgp_read(self, func):
		"""directive function to get the various bgp af level output

		Args:
			func (method): method to be executed on bgp af config line

		Returns:
			dict: parsed output dictionary
		"""    		
		toggle, af, update_dict = False, False, ""
		op_dict = OrderedDict()
		for l in self.cmd_op:
			spl = l.strip().split()
			if l.startswith(" address-family "):
				op_dict['type'] = spl[1]
				op_dict['vrf'] = spl[3]
				continue
			if spl[1] == "router-id ": 
				op_dict['router_id'] = spl[-1]
				continue
			if spl[0] != "neighbor" : continue			# continue except neighbour statements
			nbr = spl[1]
			if not op_dict.get(nbr):
				op_dict[nbr] = {}
				nbr_dict = op_dict[nbr]
			func(nbr_dict, l, spl)

		return op_dict


class BGP(BGP_Papa):
	"""object for native BGP running config parser
	"""

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		    		
		super().__init__(cmd_op)
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
		for l in self.cmd_op:
			if blank_line(l): continue
			spl = l.strip().split()
			if l.startswith("router bgp "):
				toggle = True
				continue
			if l.startswith("!"):
				toggle = False
				continue
			if spl[0][0].startswith("!"): continue
			# if spl[0] == "!": continue
			if l.startswith(" address-family ") and spl[-2] == "vrf": 
				toggle = False
				af = True
				af_name = l.split(" address-family ")[-1]
				afl = []
				continue
			if af and l.startswith(" exit-address-family"): 
				af = False
				self.afl[af_name] = get_bgp_af_running(afl)
				continue
			if af: afl.append(l)			
			if not toggle: continue
			if spl[0] == "exit-address-family": continue
			# 
			if spl[1] == "router-id ": 
				op_dict['router_id'] = spl[-1]
				continue
			if spl[0] != "neighbor" : continue			# continue except neighbour statements
			nbr = spl[1]
			if not op_dict.get(nbr):
				op_dict[nbr] = {}
				nbr_dict = op_dict[nbr]
			func(nbr_dict, l, spl)

		update_dict = merge_vrftype_name_inkey(self.afl)
		self.op_dict.update(update_dict)
		return op_dict


def merge_vrftype_name_inkey(d):
	"""update vrf and vrf_type in dictionary

	Args:
		d (dict): dictionary with neighbours attributes

	Returns:
		dict: updated dict
	"""    	
	update_dict = {}
	for vrftype, vrfattrs in d.items():
		for nbr, vrfattr in vrfattrs.items():
			vrftype_spl = vrftype.split()
			vrf = vrftype_spl[-1]
			af = vrftype_spl[-3]
			update_dict[nbr] = vrfattr
			update_dict[nbr]['vrf'] = vrf
			update_dict[nbr]['address-family'] = af
	return update_dict


# ------------------------------------------------------------------------------

def get_bgp_af_running(cmd_op, *args):
	"""defines set of methods executions. to get various bgp address-family parameters.
	uses AddressFamily in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	AF = AddressFamily(cmd_op)	
	AF.bgp_nbr_attributes()

	return AF.op_dict

def get_bgp_running(cmd_op, *args):
	"""defines set of methods executions. to get various bgp native parameters.
	uses BGP in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = BGP(cmd_op)
	R.bgp_nbr_attributes()

	return R.op_dict

