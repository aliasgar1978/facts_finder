
from nettoolkit import *

# ================================================================================================
# common functions
# ================================================================================================

def get_appeneded_value(dic, key, value):
	"""appends the value to an existing value found in dictionary with provided key if exist other wise returns same value

	Args:
		dic (dict): dictionary
		key (str): dictionary key
		value (str): arbitrary value to be appended to existing key if exist

	returns:
		str: appened string
	"""
	if not dic.get(key):
		return value
	else:
		return dic[key] + '\n'+ value


# ================================================================================================


def get_subnet(address):
	"""derive subnet number for provided ipv4 address

	Args:
		address (str): ipv4 address in string format a.b.c.d/mm

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv4(address).subnet_zero()

def get_v6_subnet(address):
	"""derive subnet number for provided ipv6 address

	Args:
		address (str): ipv6 address in string with mask

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv6(address).subnet_zero()


def get_int_ip(ip): 
	"""get ip address from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: ip address
	"""	
	return ip.split("/")[0]

def get_int_mask(ip): 
	"""get mask from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: mask
	"""	
	return ip.split("/")[-1]




# ================================================================================================
# register all declared functions here
# ================================================================================================

__all__ = [
	'get_appeneded_value', 
	'get_subnet', 'get_v6_subnet',
	'get_int_ip', 	'get_int_mask',


]