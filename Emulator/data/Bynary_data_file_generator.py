import random
from binascii import unhexlify, hexlify

def Create_file(file, sample_rate_unit, sample_rate_value, data_bytes):
    #try:
    fd=None
    buf=''
    #-------------------------------------#
    #Sample-Rate-unit-initialization:-----#
    #1-Byte-------------------------------#
    #buf+='00' # Sample Rate in Milisec
    #buf+='01' # Sample Rate in Sec
    #buf+='10' # Sample Rate in Hz
    if sample_rate_unit.lower()=='millisec': buf+='00'
    elif sample_rate_unit.lower()=='sec': buf+='01'
    elif sample_rate_unit.lower()=='hz': buf+='10'
    else: 
        raise Exception('Sample_rate_unit Error')
    #-------------------------------------#
    #Sample Rate value initialization:----#
    #2-Bytes-(up-to-65535)----------------#
    buf+='%04x' % int(sample_rate_value)
    #-------------------------------------#
    #Data-Bytes-of-one-Sample:------------#
    #2-Bytes-(up-to-65535)----------------#
    buf+='%04x' % int(data_bytes)

    #for i in range (0,65535):
    #    rand='%04x' % random.randint(0,65535)
    #    buf+=rand
    #
    
    for i in range (0,2000):
        rand='%020x' % random.randint(3,12)
        #rand2='%010x' % random.randint(50,80)
        buf+=rand
    
    buf=unhexlify(buf)
    fd=open(file, 'wb+')
    fd.write(buf)
    fd.close()
    return True
    #except Exception, e:
    #    if fd!=None: fd.close()
    #    print 44, e
    #    return False

def Update_file(file, sample_rate_unit, sample_rate_value, data_bytes):
    try:
        fd=None
        buf=''
        #-------------------------------------#
        #Sample-Rate-unit-initialization:-----#
        #1-Byte-------------------------------#
        #buf+='00' # Sample Rate in Milisec
        #buf+='01' # Sample Rate in Sec
        #buf+='10' # Sample Rate in Hz
        if sample_rate_unit.lower()=='millisec': buf+='00'
        elif sample_rate_unit.lower()=='sec': buf+='01'
        elif sample_rate_unit.lower()=='hz': buf+='10'
        else: 
            raise Exception('Sample_rate_unit Error')
        #-------------------------------------#
        #Sample Rate value initialization:----#
        #2-Bytes-(up-to-65535)----------------#
        buf+='%04x' % int(sample_rate_value)
        #-------------------------------------#
        #Data-Bytes-of-one-Sample:------------#
        #2-Bytes-(up-to-65535)----------------#
        buf+='%04x' % int(data_bytes)
        
        fd=open(file, 'rb+')
        fd.read(5)
        
        buf+=hexlify(fd.read())
        fd.close()
        
        buf=unhexlify(buf)
        fd=open(file, 'wb+')
        fd.write(buf)
        fd.close()
        return True
    except Exception, e:
        if fd!=None: fd.close()
        print 84, e
        return False

def Update_ECG_file(file, sample_rate_unit, sample_rate_value, data_bytes):
    try:
        fd=None
        buf=''
        #-------------------------------------#
        #Sample-Rate-unit-initialization:-----#
        #1-Byte-------------------------------#
        #buf+='00' # Sample Rate in Milisec
        #buf+='01' # Sample Rate in Sec
        #buf+='10' # Sample Rate in Hz
        if sample_rate_unit.lower()=='millisec': buf+='00'
        elif sample_rate_unit.lower()=='sec': buf+='01'
        elif sample_rate_unit.lower()=='hz': buf+='10'
        else: 
            raise Exception('Sample_rate_unit Error')
        #-------------------------------------#
        #Sample Rate value initialization:----#
        #2-Bytes-(up-to-65535)----------------#
        buf+='%04x' % int(sample_rate_value)
        #-------------------------------------#
        #Data-Bytes-of-one-Sample:------------#
        #2-Bytes-(up-to-65535)----------------#
        buf+='%04x' % int(data_bytes)
        
        fd=open(file, 'rb+')
        fd.read(16)
        
        buf+=hexlify(fd.read())
        fd.close()
        
        buf=unhexlify(buf)
        fd=open(file, 'wb+')
        fd.write(buf)
        fd.close()
        return True
    except Exception, e:
        if fd!=None: fd.close()
        print 124, e
        return False

def main():
    #if Update_ECG_file('ecg.bin', 'millisec', 200, 16): print 'Success'
    
    #if Update_file('hr.bin', 'sec', 10, 4): print 'Success'
    
    #if Create_file('hr.bin', 'sec', 10, 4): print 'Success'   #!!
    #if Create_file('spo2.bin', 'sec', 10, 4): print 'Success' #!!
    #if Create_file('rr.bin', 'sec', 10, 10): print 'Success'  #!!
    #if Create_file('bp.bin', 'sec', 10, 20): print 'Success'  #!!
    #if Create_file('bg.bin', 'sec', 10, 20): print 'Success'  #!!
    #if Create_file('bt.bin', 'sec', 10, 20): print 'Success'  #!!
    
if __name__ == "__main__":
    main()