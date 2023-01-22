"""generate Network Devices (Switch/Router) facts from its configuration outputs.
"""

# ------------------------------------------------------------------------------
# BELOW ARE FUNCTION IMPORTED AND PUBLISHED OUT FOR TESTING ONLY.
# ADD A FUNCTION HERE TO TEST IT EXCLUSIVELY FROM OUTSIDE EXECUTION
# EXAMPLE:
# ------------------------------------------------------------------------------
# from .cisco_parser import absolute_command
# from .cisco import get_cdp_neighbour
# from .juniper import get_lldp_neighbour
# ------------------------------------------------------------------------------

from .generators.merger import device
from .generators.merger import DeviceDB
from .rearrange import rearrange_tables

from .clean import CleanFacts



__all__ = [ 
	'device', 'DeviceDB',
	'CleanFacts',
	'rearrange_tables',
	]

__ver__ = "0.0.7"