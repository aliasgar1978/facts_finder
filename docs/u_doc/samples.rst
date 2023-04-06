
Samples
=======

.. note::

    This is a sample execution file, for facts-finder module usage, to generate clean file 
    along with custom module insertion
    Please modify the script as per your custom module name/definitions
    marked at MODIFY:, INPUT: markers
    Also refer to input sections to provide the inputs.

-----


A Sample Execution File using DeviceDB
--------------------------------------------------------------------------

:download:`sample execution file<files/exec-devicedb.py>`. A sample execution file will look similar to this


-----



A Sample Execution File to generate clean file
--------------------------------------------------------------------------

:download:`generate clean facts <files/fg_exec_with_custom.py>`. A sample execution file will look similar to this



without custom facts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * While calling ``main`` function put **custom** switch to **False** in order to *skip custom processing*.
  * And there is no need of custom imports in this case.





with custom facts
^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    * While calling ``main`` function put **custom** switch to **True** in order to *keep custom processing*.
    * custom imports are **must** in this case.



-----
