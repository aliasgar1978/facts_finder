facts_finder User documentation!
============================================

What is facts_finder ?
-----------------------------------------

facts_finder is an open-source package, used to get the device facts out of its configuration
and a few other show commands. It extracts informations and keep those in a user friendly summarized manner in Excel file.


Who can use ?
-----------------------------------------

Networking geeks can use it to gather the informations out of networking devices.


Where can be used ?
-----------------------------------------

It can be used on Cisco, Juniper Networking Switches, Routers.


Why to use ?
-----------------------------------------

It can gather the informations quickly and create excel summary sheets effortless

How can I use ?
-----------------------------------------

Stay Tuned!


High-level Overview 
----------------------------

	#. Import necessary package, modules
	#. Define your input files ( i.e. captures )
	#. Generate and evaluate database from device
	#. Write database to Excel

Detailed How To
--------------------

	#. Import necessary package, modules

		.. code::

			from facts_finder import DeviceDB
			from facts_finder import device
			from facts_finder import write_to_xl


	#. Define your input files ( i.e. captures )

		.. code::

			file = "file_with_output_captured.log"		# provide capture file 

		.. attention::
			
			* It is advisable to capture command output using **capture_it** package. So manual editing can be avoided.
			* Otherwise modify output as mentioned in information below, such that facts_finder can read it.
			* All commands output should be stored in a single file. 


	#. Generate and evaluate database from device

		.. code:: python

			_model = device(file)		# select the model based on input file
			device_database = DeviceDB()	# create a new device database object
			df_dict = device_database.evaluate(_model)	# evaluate object by providing necessary model, and return dictionary

		see also:
			* `device() <https://facts-finder.readthedocs.io/en/latest/docs/t_doc/__merger.html#facts_finder.merger.device>`_
			* `DeviceDB() <https://facts-finder.readthedocs.io/en/latest/docs/t_doc/__merger.html#facts_finder.merger.DeviceDB>`_

	#. Write database to Excel

		.. code:: python
			
			write_to_xl("output_file.xlsx", df_dict, index=True, overwrite=True)	# write output to Excel

		Parameters:
			* **df_dict:** [mandatory] dictionary extracted after evaluation, to write to excel.
			* **index:** [optional] will not keep index columns
			* **overwrite:** [optional] will overwrite the excel file if it does exist. otherwise create a copy.

		see also:
		`write_to_xl() <https://facts-finder.readthedocs.io/en/latest/docs/t_doc/__database.html#facts_finder.database.write_to_xl>`_



.. important::
	
	Below are the commands requires to be captured from device for **Cisco** Devices.

	* show lldp neighbors
	* show cdp neighbors
	* show interfaces status
	* show interfaces description
	* show mac address-table
	* show ip arp
	* show running-config
	* show version

	command output format should be as follows
		
		* ! ==========================================
		* ! output for command: show runn
		* ! ==========================================
		* <<output of command>> ...

	* No hostname-prompt requires to be mentioned in command line.

.. important::

	Below are the commands requires to be captured from device for **Juniper** Devices.

	* show lldp neighbors
	* show configuration
	* show version
	* show interfaces descriptions
	* show chassis hardware
	* show arp

	command output format should be as follows

		# ===================================================	
		# output for command: show configuration | no-more
		# ===================================================			
		<<output of command>> ...


	* No hostname-prompt requires to be mentioned in command line.


.. admonition:: Notice

	Make a note that output differs between version to version on devices, and thus it is obvious that parsing may not work every where, as expected incase if format differs from expectation. 

	Make sure to cross-check the generated facts before using it.