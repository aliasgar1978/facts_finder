
Samples
=======


A Sample Execution File with / without custom facts addition/modification 
--------------------------------------------------------------------------

.. note::

    This is a sample execution file, for facts-finder module usage, to generate clean file 
    along with custom module insertion
    Please modify the script as per your custom module name/definitions
    marked at MODIFY: markers
    Also refer to input sections to provide the inputs.


:download:`generate clean facts <files/fg_exec_with_custom.py>`. A sample execution file will look similar to this


To use it with custom facts
^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
While calling ``main`` function put **custom** switch to **True** in order to *keep custom processing*. 
custom imports are must in this case.


To use it without custom facts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While calling ``main`` function put **custom** switch to **False** in order to *skip custom processing*. 
And there is no need of custom imports as well in this case.



