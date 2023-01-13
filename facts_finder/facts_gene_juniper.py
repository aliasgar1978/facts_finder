from pprint import pprint

from facts_finder.gene import KeyExchanger
from facts_finder.gene import VarInterfaceJuniper
from facts_finder.gene import TableInterfaceJuniper
from facts_finder import DeviceFactsFg
from capture_it.database import write_to_xl, append_to_xl

from facts_finder.common import get_op
from nettoolkit import JSet
from facts_finder.common import verifid_output
import os

# ================================================================================================

def evaluate_juniper(
	capture_log_file,
	capture_file,
	column_mapper_file=None,
	):

	# ================================================================================================
	# var
	# ================================================================================================

	juniper_cmd_lst = {'show interfaces | no-more': {'admin_state': 'link_status',
												'description': 'description',
												'destination': '//subnet',
												'hardware_type': 'GRE',
												'interface': 'interface',
												'link_status': 'protocol_status',
												'local': '//subnet1',
												'mtu': ''},
					'show lacp interfaces | no-more': {'aggregated_interface': 'interface',
													'member_interface': '//po_to_interface',
													'mux_state': '',
													'receive_state': '',
													'transmit_state': ''},
					'show lldp neighbors | no-more': {'chassis_id': '',
												'local_interface': 'interface',
												'parent_interface': '',
												'port_info': 'nbr_interface',
												'system_name': '//nbr_hostname'},
					'show version | no-more': {'appid_services': '',
											'base_os_boot': '',
											'base_os_software_suite': '',
											'border_gateway_function_package': '',
											'crypto_software_suite': '',
											'hostname': 'hostname',
											'idp_services': '',
											'junos_version': 'ios_version',
											'kernel_software_suite': '',
											'lab_package': '',
											'model': 'hardware',
											'online_documentation': '',
											'other_device_properties': '',
											'other_properties_versions': '',
											'packet_forwarding_engine_support_m_t_ex_common': '',
											'packet_forwarding_engine_support_mx_common': '',
											'platform_software_suite': '',
											'py_base_i386': '',
											'qfabric_system_id': '',
											'routing_software_suite': '',
											'runtime_software_suite': '',
											'serial_number': 'serial',
											'services_aacl_container_package': '',
											'services_application_level_gateways': '',
											'services_captive_portal_content_delivery_package': '',
											'services_crypto': '',
											'services_http_content_management_package': '',
											'services_ipsec': '',
											'services_jflow_container_package': '',
											'services_ll_pdf_container_package': '',
											'services_mobile_subscriber_service_package': '',
											'services_mobilenext_software_package': '',
											'services_nat': '',
											'services_ptsp_container_package': '',
											'services_rpm': '',
											'services_ssl': '',
											'services_stateful_firewall': '',
											'voice_services_container_package': ''}}

	output_file = f'{capture_file}-facts_Gene.xlsx'		## Output Excel Facts Captured File

	## 1. --- Cleanup old
	try: os.remove(output_file)	# remove old file if any
	except: pass

	if column_mapper_file is not None:
		KEC_VAR = KeyExchanger(column_mapper_file, juniper_cmd_lst)
		juniper_cmd_lst = KEC_VAR.cisco_cmd_lst

	## 2. ---  `var` Tab 
	CIV = VarInterfaceJuniper(capture_file)
	CIV.execute(juniper_cmd_lst)
	append_to_xl(output_file, CIV.var)

	## 3. ---  `table` Tab 

	CID = TableInterfaceJuniper(capture_file)
	CID.execute(juniper_cmd_lst)
	append_to_xl(output_file, CID.pdf)

	# ## 5. --- `facts-gene` updates generated output excel; per required column names; based Excel column Mappers.
	DFF = DeviceFactsFg(capture_log_file, output_file)
	DFF.execute_juniper()

	print(f'Check output in -> {output_file}')

	return {'var': CIV, 'output': output_file}


# # ================================================================================================


