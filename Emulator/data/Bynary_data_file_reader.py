import time
from binascii import hexlify
import os, sys
path = os.path.dirname(os.path.abspath(__file__))+os.sep

def bin_file_data_reader(filename, chunk=None):
    filename=path+filename
    fd=None
    try:
        fd=open(filename, "rb")
        
        fd.read(3)
        if chunk==None:
            print 'here'
            chunk= int(hexlify(fd.read(2)),16)
            print chunk
        else: 
            fd.read(2)
        print chunk, type(chunk)
        while True:
            while True:
                data = fd.read(chunk)
                if data and len(data)==chunk:
                    yield data
                else:
                    fd.close()
                    break
            fd=open(filename, "rb")
            fd.read(5)
    except KeyboardInterrupt:
        if fd != None: fd.close()
    except Exception, e:
        print e
        if fd != None: fd.close()


def bin_file_header_reader(filename):
    filename=path+filename
    fd=None
    try:
        fd=open(filename, "rb")
        
        SR_unit = hexlify(fd.read(1))
        if SR_unit=='00': print 'SR_unit: Millisec'
        elif SR_unit=='01': print 'SR_unit: Sec'
        elif SR_unit=='10': print 'SR_unit: Hz'
        else: print 'SR_unit: error'
        SR_value = int(hexlify(fd.read(2)),16)
        print 'SR_value: ',SR_value
        Data_Size = int(hexlify(fd.read(2)),16)
        print 'Data_Size: ',Data_Size
        
        return SR_unit, SR_value, Data_Size
    except KeyboardInterrupt:
        if fd != None: fd.close()
    except Exception, e:
        print e
        if fd != None: fd.close()

def main():
    SR_unit, SR_value, Data_Size = bin_file_header_reader('rr.bin')
    
    if SR_unit=='00': SR_sec=SR_value/1000.0
    elif SR_unit=='01': SR_sec=SR_value
    elif SR_unit=='10': SR_sec=1.0/SR_value
    else: SR_sec=1
    for data in bin_file_data_reader('rr.bin'):
        print hexlify(data)
        time.sleep(SR_sec)
        
if __name__ == "__main__":
    main()