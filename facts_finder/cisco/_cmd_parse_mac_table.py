"""cisco mac address table command output parser """

# ------------------------------------------------------------------------------
from facts_finder.common import verifid_output
from facts_finder.common import blank_line
from facts_finder.common import standardize_mac
from facts_finder.common import mac_4digit_separated
from facts_finder.common import mac_2digit_separated

# ------------------------------------------------------------------------------

def get_mac_address_table(cmd_op, *args):
	"""parser - show mac address-table command output

	Parsed Fields:
		* port/interface
		* neighbor mac
		* neighbor mac2
		* neighbor mac4

	Args:
		cmd_op (list, str): command output in list/multiline string.

	Returns:
		dict: output dictionary with parsed fields
	"""	
	cmd_op = verifid_output(cmd_op)
	op_dict = {}
	start = False
	for l in cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		if l.startswith("Multicast"): break
		spl = l.strip().split()
		try:
			if spl[2].upper() != 'DYNAMIC': continue
		except: continue
		p = spl[-1]
		if not op_dict.get(p): op_dict[p] = {'neighbor': {}}
		nbr = op_dict[p]['neighbor']
		if not nbr.get("mac"): nbr["mac"] = set()
		if not nbr.get("mac2"): nbr["mac2"] = set()
		if not nbr.get("mac4"): nbr["mac4"] = set()
		nbr["mac"].add(standardize_mac(spl[1]))
		nbr['mac2'].add(mac_2digit_separated(spl[1]))
		nbr['mac4'].add(mac_4digit_separated(spl[1]))
	return op_dict
# ------------------------------------------------------------------------------
