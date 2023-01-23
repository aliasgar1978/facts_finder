
Using facts-finder - CleanFacts - add custom config
==========================================================

	#. Generate clean config using CleanFacts
	#. Apply custom chages on database
	#. rearrange database columns of Excel



Detailed How To
--------------------

	Once CleanFacts are generated ( Point. 3 from previous page ), go ahead with below steps.

	#. Import necessary custom package, modules

		modify as per custom package/module name(s).

		*customer_x*: is custom package
		*package_class*: custom package class containing modifying methonds.

		.. code::

			from customer_x import CustomDeviceFacts


	#. Provide Input to Custom Class
	
		Provide the generated CleanFact instance object to custom package class. 
		
		Evaluate/Modify using custom method.  

		.. code::

			ADF = CustomDeviceFacts(			## provide input to custom class
				hostname=cf.hostname,
				dev_type=cf.dev_type,
				config=cf.config,
				facts_gene_file=cf.clean_file,
			)
			ADF()								## call to generate modified data.
			ADF.write()							## custom method to write out modified data.


	#. Rearrange columns in excel file in orders [optional step]

		Orders are defined as per `rearrange.py` module of the package.

		.. code:: python
			
			rearrange_tables(cf.clean_file)




.. admonition:: Notice

	Make a note that output differs between version to version on devices, and thus it is obvious that parsing may not work every where, as expected incase if format differs from expectation. 

	Make sure to cross-check the generated facts before using it.

