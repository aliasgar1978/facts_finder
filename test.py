

from facts_finder import DeviceDB
from facts_finder import device
from facts_finder import write_to_xl
from pprint import pprint

datapath = "c:/Users/ALI/Desktop/Data/"
capture_file = datapath + "d4t-vid-1a.log"
# capture_file = datapath + "d4t-vod-d4a.log"
capture_file = datapath + "d4t-vsc-a.log"
output = capture_file + ".xlsx" 

_model = device(capture_file)					# select the model based on input file

# print(_model)
device_database = DeviceDB()					# create a new device database object

## optional input for extra columns 
# device_database.add_extra_v4_ips(_model, n={'1':'both', '2':False, '3':True})		# pass n as dictionray
device_database.add_extra_v4_ips(_model, n=range(1, 6), mask='both')				# pass n as list of ip's

df_dict = device_database.evaluate(_model)		# evaluate object by providing necessary model, and return dictionary

write_to_xl(output, df_dict, index=True, overwrite=True)	# write output to Excel
