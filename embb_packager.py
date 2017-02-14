#!/usr/bin/python

import sys, getopt

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



def main(argv):
      
   inputfile = ''
   outputfile = ''
   ppap =''
   help_string = 'embb_packeger.py -d  <deviceId>  -f <filterId> -c <compression 0/1> -t <type mbb> -i <inputfile>  -o <outputfile>'
   device_id = ''
   filter_id = ''
   input_file = ''
   embb_file  = ''
   payload_type = ''
   compression_flag = ''
      
    
   try:
      opts, args = getopt.getopt(argv,"hd:f:c:t:m:i:o:",["deviceId=","filterId=","compression=","type=","ifile=","ofile="])
   except getopt.GetoptError:
      print help_string
      sys.exit(2)
   for opt, arg in opts:
        if opt == '-h':
            print help_string 
            sys.exit()
        elif opt in ("-d", "--deviceId"):
            # Devcie ID
            device_id = arg
        elif opt in ("-f", "--filterId"):
            # Filter ID
            if int(arg) >=256:
                print 'Filter ID must be between 0 and 255'
                sys.exit()
            filter_id = arg 
            
        elif opt in ("-t", "--type"):
            # Payload Type 
            payload_type = '000000'
            if arg == 'mbb': 
                payload_type = '100000'        
        elif opt in ("-c", "--compression"):
            # Compression Flag 
            compression_flag= arg
        elif opt in ("-i", "--ifile"):
            input_file = arg 
        elif opt in ("-o", "--ofile"):
            embb_file = arg 
    
   print '__EMBB Pacakger__v1.0         '
   print 'Params:        '

   print 'Device ID         ', device_id
   print 'Fileter ID        ', filter_id 
   print 'Payload type      ', payload_type
   print 'Compression flag  ', compression_flag
   print 'Input file        ', input_file
   print 'EMBB output file  ', embb_file
   print ''
   print 'Embb Output:'
    
   #building embb container 
   
   #deviceID  
   temp = hashlib.sha1()
   temp.update(device_id)
   embb_deviceId = temp.hexdigest()
    
   #Fileter ID 
   embb_filterId = struct.pack(">H",int(filter_id))
   
   #Set payload type 
   embb_payloadType = bitarray(compression_flag+payload_type)
   
   #Read mbb file 
   in_file = open(input_file, "rb")  
   dataFromFile = in_file.read()  
   in_file.close()
   
   #Generate Payload 
   embb_payload = dataFromFile        
   if compression_flag == '1':
        embb_payload = zlib.compress(dataFromFile)
   
   #Calculate payload size 
   embb_payloadSize = struct.pack('>H', len(embb_payload))
   
   #Output Summary  
 
   print 'Embb Devcie ID    ', embb_deviceId
   print 'Filter  ID        ', embb_filterId
   print 'Embb Payload Type ', embb_payloadType
   print 'Embb Payload Size ', len(embb_payload)    
   
   #write to file 
   out_file = open(embb_file, "wb")
   out_file.write(binascii.unhexlify(embb_deviceId))
   out_file.write(embb_filterId)
   embb_payloadType.tofile(out_file)
   out_file.write(embb_payloadSize)
   out_file.write(embb_payload)
   out_file.close()
       

if __name__ == "__main__":
   main(sys.argv[1:])
