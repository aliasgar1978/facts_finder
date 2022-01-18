"""juniper system config parser from show config command """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.juniper._cmd_parse_running import Running
from facts_finder.common import blank_line

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------


class RunningSystem(Running):

	def __init__(self, cmd_op):
		super().__init__(cmd_op)
		self.system_dict = OrderedDict()

	def system_read(self, func):
		op_dict = OrderedDict()
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			spl = l.strip().split()

			func(op_dict, l, spl)
		return op_dict


	def system_hostname(self):
		func = self.get_hostname
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_hostname(op_dict, l, spl):
		hostname = ""
		if l.startswith("set system host-name"): hostname = spl[-1]
		if hostname and not op_dict.get('hostname'):
			op_dict['hostname'] = hostname
		return op_dict


	def system_nameservers(self):
		func = self.get_nameservers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_nameservers(op_dict, l, spl):
		dns = ""
		if l.startswith("set system name-server"): dns = spl[-1]
		if dns and not op_dict.get('name_servers'):
			op_dict['name_servers'] = set()
		if dns: op_dict['name_servers'].add(dns)
		return op_dict


	def system_mgmt_ip(self):
		func = self.get_mgmt_ip
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_mgmt_ip(op_dict, l, spl):
		ip = ""
		if l.startswith("set system ") and spl[-2] == "source-address": ip = spl[-1]
		if ip and not op_dict.get('management_ip'):
			op_dict['management_ip'] = ip
		return op_dict


	def system_gtac_servers(self):
		func = self.get_gtac_servers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_gtac_servers(op_dict, l, spl):
		ip = ""
		if l.startswith("set system tacplus-server") : ip = spl[3]
		if ip and not op_dict.get('tacacs_servers'):
			op_dict['tacacs_servers'] = set()
		if ip: op_dict['tacacs_servers'].add(ip)
		return op_dict


	def system_syslog_servers(self):
		func = self.get_syslog_servers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_syslog_servers(op_dict, l, spl):
		ip = ""
		if l.startswith("set system syslog host") : ip = spl[4]
		if ip and not op_dict.get('syslog_servers'):
			op_dict['syslog_servers'] = set()
		if ip: op_dict['syslog_servers'].add(ip)
		return op_dict


	def system_ntp_servers(self):
		func = self.get_ntp_servers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_ntp_servers(op_dict, l, spl):
		ip = ""
		if l.startswith("set system ntp server") : ip = spl[4]
		if ip and not op_dict.get('ntp_servers'):
			op_dict['ntp_servers'] = set()
		if ip: op_dict['ntp_servers'].add(ip)
		return op_dict


	def system_banner(self):
		func = self.get_banner
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_banner(op_dict, l, spl):
		banner = ""
		if l.startswith("set system login announcement"): banner = " ".join(spl[4:])
		if banner and not op_dict.get('banner'):
			op_dict['banner'] = banner
		return op_dict


	# # Add more interface related methods as needed.


# ------------------------------------------------------------------------------


def get_running_system(cmd_op, *args):
	""" define set of methods executions. to get system parameters.
	"""
	R  = RunningSystem(cmd_op)
	R.system_hostname()
	R.system_nameservers()
	R.system_mgmt_ip()
	R.system_gtac_servers()
	R.system_syslog_servers()
	R.system_ntp_servers()
	R.system_banner()

	# # update more interface related methods as needed.

	return R.system_dict



# ------------------------------------------------------------------------------

