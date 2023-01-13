from pprint import pprint

from facts_finder.gene import KeyExchanger
from facts_finder.gene import VarInterfaceCisco
from facts_finder.gene import TableInterfaceCisco, TableVrfsCisco
from facts_finder import DeviceFactsFg
from capture_it.database import write_to_xl, append_to_xl
from facts_finder.cisco_parser import get_op_cisco
import os

# ================================================================================================

def evaluate_cisco(
	capture_log_file,
	capture_file,
	var_column_mapper_file=None,
	int_column_mapper_file=None,
	):


	# ================================================================================================
	# var
	# ================================================================================================
	cmd_lst_var = {'show ipv6 interface brief': {'admin': '',
											'intf': '',
											'ipaddr': '//h2b-h3b',
											'protocol': ''},
											'show route-map': {'action': '',
											'match_clauses': '',
											'name': '',
											'seq': '',
											'set_clauses': '//reso'},
											'show version': {'config_register': '',
											'hardware': 'hardware',
											'hostname': 'hostname',
											'mac': 'mac',
											'reload_reason': '',
											'restarted': '',
											'rommon': '',
											'running_image': 'bootvar',
											'serial': 'serial',
											'uptime': '',
											'uptime_days': '',
											'uptime_hours': '',
											'uptime_minutes': '',
											'uptime_weeks': '',
											'uptime_years': '',
											'version': 'ios_version'}}
	cmd_lst_int = {'show cdp neighbors detail': {'capabilities': '',
											'destination_host': '//nbr_hostname',
											'local_port': 'interface',
											'management_ip': 'nbr_ip',
											'platform': 'nbr_platform',
											'remote_port': 'nbr_interface',
											'software_version': ''},
											'show etherchannel summary': {'group': 'int_number',
											'interfaces': '//po_to_interface',
											'interfaces_status': '',
											'po_name': 'interface',
											'po_status': '',
											'protocol': ''},
											'show interfaces': {'abort': '',
											'address': '',
											'bandwidth': '',
											'bia': '',
											'crc': '',
											'delay': '',
											'description': 'description',
											'duplex': 'duplex',
											'encapsulation': '',
											'hardware_type': '//filter',
											'input_errors': '',
											'input_packets': '',
											'input_rate': '',
											'interface': 'interface',
											'ip_address': '//subnet',
											'last_input': '',
											'last_output': '',
											'last_output_hang': '',
											'link_status': 'link_status',
											'media_type': 'media_type',
											'mtu': '',
											'output_errors': '',
											'output_packets': '',
											'output_rate': '',
											'protocol_status': 'protocol_status',
											'queue_strategy': '',
											'speed': 'speed'},
											'show interfaces switchport': {'access_vlan': 'access_vlan',
											'admin_mode': 'admin_mode',
											'interface': 'interface',
											'mode': '//interface_mode',
											'native_vlan': 'native_vlan',
											'switchport': 'switchport',
											'switchport_monitor': '',
											'switchport_negotiation': 'switchport_negotiation',
											'trunking_vlans': '//vlan_members',
											'voice_vlan': 'voice_vlan'},
											'show ip bgp all summary': {'addr_family': 'bgp_vrf',
											'bgp_neigh': 'bgp_peer_ip',
											'local_as': '',
											'neigh_as': '',
											'router_id': '',
											'state_pfxrcd': '',
											'up_down': ''},
											'show ip bgp vpnv4 all neighbors': {'bgp_state': '',
											'inbound_routemap': '',
											'local_as': '',
											'localhost_ip': '',
											'localhost_port': '',
											'neighbor': '',
											'outbound_routemap': '',
											'peer_group': 'bgp_peergrp',
											'remote_as': '',
											'remote_ip': 'bgp_peer_ip',
											'remote_port': '',
											'remote_router_id': '',
											'vrf': ''},
											'show ip vrf interfaces': {'interface': 'interface',
											'ipaddress': '',
											'proto_state': '',
											'vrf': 'intvrf'},
											'show ipv6 interface brief': {'admin': '',
											'intf': 'interface',
											'ipaddr': '//h4block',
											'protocol': ''},
											'show lldp neighbors detail': {'capabilities': '',
											'chassis_id': '',
											'local_interface': 'interface',
											'management_ip': 'nbr_ip',
											'neighbor': '//nbr_hostname',
											'neighbor_interface': '',
											'neighbor_port_id': 'nbr_interface',
											'serial': 'nbr_serial',
											'system_description': '',
											'vlan': 'nbr_vlan'},
											'show vrf': {'default_rd': '',
											'interfaces': '',
											'name': 'vrf',
											'protocols': ''}}
	cmd_lst_vrf = {'show vrf': {'default_rd': '',
							'interfaces': '',
							'name': 'vrf',
							'protocols': ''}}

	output_file = f'{capture_file}-facts_Gene.xlsx'		## Output Excel Facts Captured File

	## 1. --- Cleanup old
	try: os.remove(output_file)	# remove old file if any
	except: pass

	## 2. ---  `var` Tab 
	if var_column_mapper_file is not None:
		KEC_VAR = KeyExchanger(var_column_mapper_file, cmd_lst_var)
		cmd_lst_var = KEC_VAR.cisco_cmd_lst
	CIV = VarInterfaceCisco(capture_file)
	CIV.execute(cmd_lst_var)
	append_to_xl(output_file, CIV.var)

	## 3. ---  `table` Tab 
	if int_column_mapper_file is not None:
		KEC_INT = KeyExchanger(int_column_mapper_file, cmd_lst_int)
		cmd_lst_int = KEC_INT.cisco_cmd_lst
	CID = TableInterfaceCisco(capture_file)
	CID.execute(cmd_lst_int)
	append_to_xl(output_file, CID.pdf)

	## 4. ---  `vrf` Tab 
	if int_column_mapper_file is not None:
		KEC_VRF = KeyExchanger(int_column_mapper_file, cmd_lst_vrf)
		cmd_lst_vrf = KEC_VRF.cisco_cmd_lst
	TVC = TableVrfsCisco(capture_file)
	TVC.execute(cmd_lst_vrf)
	append_to_xl(output_file, TVC.pdf)

	# ## 5. --- `facts-gene` updates generated output excel; per required column names; based Excel column Mappers.
	DFF = DeviceFactsFg(capture_log_file, output_file)
	DFF.execute()

	print(f'Check output in -> {output_file}')

	return {'var': CIV, 'output': output_file}


