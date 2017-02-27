import sys
import urllib
import json
from optparse import OptionParser

import hashlib 
import zlib
import struct 
import urllib
import json
from optparse import OptionParser
import binascii
from binascii import unhexlify
from binascii import hexlify
from bitarray import bitarray

print ''
print ''
print '__EMBB Pacakger__v3.0         '

inputfile = ''
outputfile = ''
ppap =''
help_string = 'embb_packeger.py -d  <deviceId>  -f <filterId> -c <compression 0/1> -t <type mbb / cc1> -i <inputfile>  -o <outputfile>'
device_id = ''
filter_id = '0'
input_file = ''
embb_file  = ''
payload_type = ''
compression_flag = ''

parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-d", "--deviceid", dest="device_id")
parser.add_option("-f", "--filterId", dest="filter_id")
parser.add_option("-c", "--compression", dest="compression_flag")
parser.add_option("-t", "--type", dest="payload_type")
parser.add_option("-i", "--inputfile", dest="input_file")
parser.add_option("-o", "--outputfile", dest="outputfile")
(options, args) = parser.parse_args()

if not options.device_id or not options.filter_id or not options.compression_flag or not options.payload_type or not options.input_file or not options.outputfile:
    print 'ERROR: invalid or missing command line options'
    #parser.print_help()
    print help_string 
    sys.exit(1)


device_id = options.device_id

if int(options.filter_id) >=256:
    print 'Filter ID must be between 0 and 255'
    sys.exit(1)
filter_id = options.filter_id

compression_flag=options.compression_flag

if options.payload_type == 'mbb': 
    payload_type = '1000000'
elif options.payload_type == 'cc1':
    payload_type = '0100000'
else:
    payload_type = '0000000'
    
input_file = options.input_file
output_file = options.outputfile


#building embb container 
temp = hashlib.sha1()
temp.update(device_id)
embb_deviceId = temp.hexdigest()
embb_filterId = struct.pack(">H",int(filter_id))
embb_payloadType = bitarray(compression_flag+payload_type)

in_file = open(input_file, "rb")  
dataFromFile = in_file.read()  
in_file.close()
    
embb_payload = dataFromFile        
if compression_flag == '1':
    embb_payload = zlib.compress(dataFromFile)

embb_payloadSize = struct.pack('>H', len(embb_payload))
   
print 'Embb Devcie ID    ', embb_deviceId
print 'Filter  ID        ', embb_filterId
print 'Embb Payload Type ', embb_payloadType
print 'Embb Payload Size ', len(embb_payload)    
   
out_file = open(output_file, "wb")
out_file.write(binascii.unhexlify(embb_deviceId))
out_file.write(embb_filterId)
embb_payloadType.tofile(out_file)
out_file.write(embb_payloadSize)

#out_file.write(binascii.unhexlify(embb_payloadSize)

out_file.write(embb_payload)
out_file.close()
