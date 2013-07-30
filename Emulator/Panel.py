#Boa:FramePanel:XBeePanel

import wx #visual python libs (need wxpython module)
import serial, serial.tools.list_ports #serial port python libs (need pyserial module)
import os, sys
import time, datetime
import string
import random
from socket import *
import threading
from binascii import hexlify, unhexlify
from crypto.cipher.aes  import AES
from crypto.cipher.base import padWithPadLen

path_to_file = os.path.dirname(os.path.abspath(__file__))+os.sep+'data'+os.sep

class CharValidator(wx.PyValidator):
    ''' Validates data as it is entered into the text controls. '''

    #----------------------------------------------------------------------
    def __init__(self, flag):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    #----------------------------------------------------------------------
    def Clone(self):
        '''Required Validator method'''
        return CharValidator(self.flag)

    #----------------------------------------------------------------------
    def Validate(self, win):
        return True

    #----------------------------------------------------------------------
    def TransferToWindow(self):
        return True

    #----------------------------------------------------------------------
    def TransferFromWindow(self):
        return True

    #----------------------------------------------------------------------
    def OnChar(self, event):
        keycode = int(event.GetKeyCode())
        if keycode in [8,13,127,314,316]:
            pass
        elif keycode < 256:
            key = chr(keycode)
            if self.flag == 'INT' and key not in string.digits:
                return
            elif self.flag == 'FLOAT' and key not in string.digits+'.':
                return
            elif self.flag == 'HEX' and key not in string.hexdigits:
                return 
            elif self.flag == 'ADDRESS' and key not in string.digits+'.:':
                return
            
        event.Skip()

class XBeePanel(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wx.NewId(), name='', parent=prnt,
              pos=wx.Point(592, 208), size=wx.Size(345, 343),
              style=wx.TAB_TRAVERSAL)
        self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        
        self.pan_id_text = wx.StaticText(id=wx.NewId(), label=u'PAN ID',
              name='pan_id_text', parent=self, pos=wx.Point(15, 15),
              size=wx.Size(35, 13), style=0)
        
        self.pan_id_textctrl = wx.TextCtrl(id=wx.NewId(),
              name='pan_id_textctrl', parent=self, pos=wx.Point(64, 13),
              size=wx.Size(128, 21), style=0, value=u'1234',
              validator=CharValidator('HEX'))
        
        self.short_text = wx.StaticText(id=wx.NewId(), label=u'SHORT',
              name='short_text', parent=self, pos=wx.Point(15, 39),
              size=wx.Size(35, 13), style=0)
        
        self.short_textctrl = wx.TextCtrl(id=wx.NewId(), name='short_textctrl',
              parent=self, pos=wx.Point(64, 37), size=wx.Size(128, 21), style=0,
              value=u'0000',
              validator=CharValidator('HEX'))
        
        self.long_text = wx.StaticText(id=wx.NewId(), label=u'LONG',
              name='long_text', parent=self, pos=wx.Point(15, 63),
              size=wx.Size(35, 13), style=0)
        
        self.long_textctrl = wx.TextCtrl(id=wx.NewId(), name='long_textctrl',
              parent=self, pos=wx.Point(64, 61), size=wx.Size(128, 21), style=0,
              value=u'0013A20040305AC7',
              validator=CharValidator('HEX'))
        
        self.udp_port_text = wx.StaticText(id=wx.NewId(), label=u'UDP port',
              name='udp_port_text', parent=self, pos=wx.Point(15, 87),
              size=wx.Size(44, 13), style=0)
        
        self.udp_port_textctrl = wx.TextCtrl(id=wx.NewId(),
              name='udp_port_textctrl', parent=self, pos=wx.Point(64, 85),
              size=wx.Size(128, 21), style=0, value=u'192.168.33.106:12345',
              validator=CharValidator('ADDRESS'))
        
        self.data_bytes_text = wx.StaticText(id=wx.NewId(),
              label=u'Data [bytes]', name='data_bytes_text', parent=self,
              pos=wx.Point(15, 127), size=wx.Size(62, 13), style=0)
        
        self.data_bytes_textctrl = wx.TextCtrl(id=wx.NewId(),
              name='data_bytes_textctrl', parent=self, pos=wx.Point(123, 125),
              size=wx.Size(69, 21), style=0, value=u'16',
              validator=CharValidator('INT'))
        
        self.sample_rate_rb = wx.RadioBox(choices=['[Sec]', '[Hz]'],
              id=wx.NewId(), label=u'Sample Rate', majorDimension=2,
              name='sample_rate_rb', parent=self, pos=wx.Point(8, 151),
              size=wx.Size(112, 43), style=wx.RA_SPECIFY_COLS)
        
        self.sample_rate_textctrl = wx.TextCtrl(id=wx.NewId(),
              name='sample_rate_textctrl', parent=self, pos=wx.Point(123, 149),
              size=wx.Size(69, 21), style=0, value=u'1',
              validator=CharValidator('FLOAT'))
        
        self.encryption_check = wx.CheckBox(id=wx.NewId(), label=u'Encryption',
              name='encryption_check', parent=self, pos=wx.Point(125, 178),
              size=wx.Size(72, 13), style=0)
        self.encryption_check.Bind(wx.EVT_CHECKBOX, self.OnEncryption_check)
        
        self.samples_text = wx.StaticText(id=wx.NewId(), label=u'Samples',
              name='samples_text', parent=self, pos=wx.Point(139, 218),
              size=wx.Size(40, 13), style=0)
        
        self.samples_textctrl = wx.TextCtrl(id=wx.NewId(),
              name='samples_textctrl', parent=self, pos=wx.Point(137, 236),
              size=wx.Size(55, 21), style=0, value=u'100',
              validator=CharValidator('INT'))

        self.addressing_type_rb = wx.RadioBox(choices=['XBee S2', 'XBee short',
              'XBee long', 'UDP'], id=wx.NewId(), label=u'Addressing Type',
              majorDimension=1, name='addressing_type_rb', parent=self,
              pos=wx.Point(208, 6), size=wx.Size(112, 99),
              style=wx.RA_SPECIFY_COLS)
        self.addressing_type_rb.Bind(wx.EVT_RADIOBOX, self.OnAddressing_type_rb)
        
        self.data_type_rb = wx.RadioBox(choices=['Rand', 'ECG', 'HR', 'SpO2',
              'BP', 'RR', 'BG', 'BT'], id=wx.NewId(), label=u'Data Type',
              majorDimension=2, name='data_type_rb', parent=self,
              pos=wx.Point(208, 109), size=wx.Size(112, 99),
              style=wx.RA_SPECIFY_COLS)
        self.data_type_rb.Bind(wx.EVT_RADIOBOX, self.OnData_type_rb)
        
        self.progress_bar = wx.Gauge(id=wx.NewId(), name='progress_bar',
              parent=self, pos=wx.Point(8, 265), range=100, 
              size=wx.Size(312, 32), style=wx.GA_HORIZONTAL)
        
        self.start_btn = wx.Button(id=wx.NewId(), label=u'Start Transmission',
              name=u'start_btn', parent=self, pos=wx.Point(8, 215),
              size=wx.Size(112, 43), style=0)
        self.start_btn.Bind(wx.EVT_BUTTON, self.OnClickStart_btn)
        
        self.serial_btn = wx.Button(id=wx.NewId(), label=u'Serial Port Config',
              name=u'serial_btn', parent=self, pos=wx.Point(208, 215),
              size=wx.Size(112, 43), style=0)
        self.serial_btn.Bind(wx.EVT_BUTTON, self.OnClickSerial_btn)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.debug=1
        self.BROADCASTMODE=0
        self.run=0
        self.rand=1
        self.data_file=None
        self.encryption_enabled=0
        self.encryption_key=''
        self.ser=serial.Serial()
        self.udp=None
        self.work_thr=threading.Thread()
        
        self.control_pool=[
            self.pan_id_textctrl,
            self.short_textctrl,
            self.long_textctrl,
            self.udp_port_textctrl,
            self.data_bytes_textctrl,
            self.sample_rate_textctrl,
            self.sample_rate_rb,
            self.encryption_check,
            self.samples_textctrl,
            self.addressing_type_rb,
            self.serial_btn,
            self.data_type_rb
        ]
        self.enabled_controls={
            self.pan_id_textctrl:True,
            self.short_textctrl:True,
            self.long_textctrl:True,
            self.udp_port_textctrl:False,
            self.data_bytes_textctrl:True,
            self.sample_rate_textctrl:True,
            self.sample_rate_rb:True,
            self.encryption_check:True,
            self.samples_textctrl:True,
            self.addressing_type_rb:True,
            self.serial_btn:True,
            self.data_type_rb:True
        }
        self.Control_Updater()    
    #----------------------------------------------------------------------
    #Event Functions:
    #----------------------------------------------------------------------
    def OnClickStart_btn(self, event=''):
        if self.run==0:
            choice=self.addressing_type_rb.GetStringSelection()
            if choice.startswith('XBee'):
                if not self.ser.isOpen():
                    if not self.ser_open(): return
            else:
                pass
                #if not self.udp_open(): return open udp socket and use it. When done close it!!!
            self.run=1
            self.start_btn.SetLabel('Stop Transmission')
            
            self.Control_Temporal_Disabler()
            self.work_thr=threading.Thread(target=self.TX, name="worker thread")
            self.work_thr.start()
        else:
            self.run=0
            self.start_btn.SetLabel('Start Transmission')
            
            self.Control_Updater()
            self.progress_bar.SetValue(0)
    #----------------------------------------------------------------------
    def OnClickSerial_btn(self, event):
        self.ser_open()
    #----------------------------------------------------------------------
    def OnAddressing_type_rb(self, event):
        choice=self.addressing_type_rb.GetStringSelection()
        if choice=='XBee S2':
            self.enabled_controls[self.pan_id_textctrl]=True
            self.enabled_controls[self.short_textctrl]=True
            self.enabled_controls[self.long_textctrl]=True
            self.enabled_controls[self.udp_port_textctrl]=False
            self.enabled_controls[self.serial_btn]=True
        elif choice=='XBee short':
            self.enabled_controls[self.pan_id_textctrl]=True
            self.enabled_controls[self.short_textctrl]=True
            self.enabled_controls[self.long_textctrl]=False
            self.enabled_controls[self.udp_port_textctrl]=False
            self.enabled_controls[self.serial_btn]=True
        elif choice=='XBee long':
            self.enabled_controls[self.pan_id_textctrl]=True
            self.enabled_controls[self.short_textctrl]=False
            self.enabled_controls[self.long_textctrl]=True
            self.enabled_controls[self.udp_port_textctrl]=False
            self.enabled_controls[self.serial_btn]=True
        elif choice=='UDP':
            self.enabled_controls[self.pan_id_textctrl]=False
            self.enabled_controls[self.short_textctrl]=False
            self.enabled_controls[self.long_textctrl]=False
            self.enabled_controls[self.udp_port_textctrl]=True
            self.enabled_controls[self.serial_btn]=False
        self.Control_Updater()
    #----------------------------------------------------------------------    
    def OnData_type_rb(self, event):
        choice=self.data_type_rb.GetStringSelection()
        if choice=='Rand':
            self.rand=1
            self.enabled_controls[self.data_bytes_textctrl]=True
            self.enabled_controls[self.sample_rate_textctrl]=True
            self.enabled_controls[self.sample_rate_rb]=True
        else:
            self.rand=0
            self.enabled_controls[self.data_bytes_textctrl]=False
            self.enabled_controls[self.sample_rate_textctrl]=False
            self.enabled_controls[self.sample_rate_rb]=False
            if choice=='ECG':
                self.data_file=path_to_file+'ecg.bin'
                
            elif choice=='HR':
                self.data_file=path_to_file+'hr.bin'
                
            elif choice=='SpO2':
                self.data_file=path_to_file+'spo2.bin'
                
            elif choice=='BP':
                self.data_file=path_to_file+'bp.bin'
                
            elif choice=='RR':
                self.data_file=path_to_file+'rr.bin'
                
            elif choice=='BG':
                self.data_file=path_to_file+'bg.bin'
                
            elif choice=='BT':
                self.data_file=path_to_file+'bt.bin'
                
            SR_unit, SR_value, Data_Size = self.bin_file_header_reader()
            if SR_unit=='00': 
                self.sample_rate_rb.SetStringSelection('[Sec]')
                self.sample_rate_textctrl.SetValue(str(SR_value/1000.0))
            elif SR_unit=='01':
                self.sample_rate_rb.SetStringSelection('[Sec]')
                self.sample_rate_textctrl.SetValue(str(SR_value))
            elif SR_unit=='10':
                self.sample_rate_rb.SetStringSelection('[Hz]')
                self.sample_rate_textctrl.SetValue(str(1.0/SR_value))
            else:
                self.sample_rate_rb.SetStringSelection('[Sec]')
                self.sample_rate_textctrl.SetValue(str(1.0))
            self.data_bytes_textctrl.SetValue(str(Data_Size))
        self.Control_Updater()
    #----------------------------------------------------------------------
    def OnEncryption_check(self, event):
        if self.encryption_check.IsChecked()==1:
            dlg = wx.Dialog(self, -1, title='Encryption', size=(336, 137), style=wx.DEFAULT_DIALOG_STYLE|wx.CENTER)
            
            wx.StaticText(dlg, -1, "Encryption Key", pos=wx.Point(10, 14))
            
            encryption_key_textctrl=wx.TextCtrl(dlg, -1, value = self.encryption_key, pos=wx.Point(8, 32), size=wx.Size(312, 21), validator=CharValidator('HEX'))
            
            ok_button=wx.Button(dlg, -1 , 'OK', pos=wx.Point(246, 76), style=wx.OK)
            ok_button.Bind(wx.EVT_BUTTON, lambda event: dlg.EndModal(wx.ID_OK))
            
            while True:
                if (dlg.ShowModal()==wx.ID_OK):
                    if encryption_key_textctrl.GetValue()=='':
                        continue
                    self.encryption_key=encryption_key_textctrl.GetValue()
                    self.encryption_enabled=1
                    break
                else: 
                    self.encryption_check.SetValue(False)
                    break
        else:
            self.encryption_enabled=0
    #----------------------------------------------------------------------
    #GUI functions:
    #----------------------------------------------------------------------
    def Control_Updater(self):
        for obj in self.control_pool:
            if not self.enabled_controls[obj] and obj.IsEnabled(): 
                obj.Disable()
        for obj in self.control_pool:
            if self.enabled_controls[obj]and not obj.IsEnabled():
                obj.Enable()
    #----------------------------------------------------------------------
    def Control_Temporal_Disabler(self):
        for obj in self.control_pool:
            if obj.IsEnabled():
                obj.Disable()
    #----------------------------------------------------------------------
    #Internal Functions:
    #----------------------------------------------------------------------
    def ser_open(self):
        '''take RS232 port information'''
        if self.ser.isOpen():
            self.ser.close()
        ports=[]
        for port, desc, hwid in serial.tools.list_ports.comports():
            ports.append(port)
        if ports==[]:
            ports=['No Serial Ports detected']
        #'''
        dlg = wx.Dialog(self, -1, title='Port Open', size=(336, 137), style=wx.DEFAULT_DIALOG_STYLE|wx.CENTER)
        
        wx.StaticText(dlg, -1, "PORT", pos=wx.Point(10, 14))
        SerialPort_cbox=wx.ComboBox(dlg, -1, value = ports[0], pos=wx.Point(8, 32), size=wx.Size(312, 21), choices=ports, style=wx.CB_DROPDOWN)
        
        wx.StaticText(dlg, -1, "Baud Rate", pos=(10,59))
        Baud_cbox=wx.ComboBox(dlg, -1, value = "9600", pos=(8,77), size=(65,-1), choices= ['1200','2400','4800','9600','19200','38400','57600','115200','230400'], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        
        wx.StaticText(dlg, -1, "Data Bits", pos=(80,59))
        DataBits_cbox=wx.ComboBox(dlg, -1, value = "8", pos=(78,77), size=(47,-1), choices= ['4','5','6','7','8'], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        
        wx.StaticText(dlg, -1, "Parity", pos=(132,59))
        Parity_cbox=wx.ComboBox(dlg, -1, value = "NONE", pos=(130,77), size=(55,-1), choices= ['NONE','ODD','EVEN','MARK','SPACE'], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        
        wx.StaticText(dlg, -1, "Stop Bits", pos=(192,59))
        StopBits_cbox=wx.ComboBox(dlg, -1, value = "1", pos=(190,77), size=(52,-1), choices= ['1','2'], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        
        ok_button=wx.Button(dlg, -1 , 'OK', pos=wx.Point(246, 76), style=wx.OK)
        ok_button.Bind(wx.EVT_BUTTON, lambda event: dlg.EndModal(wx.ID_OK))
        
        while True:
            if (dlg.ShowModal()==wx.ID_OK):
                self.ser=self.serport(SerialPort_cbox.GetValue(), int(Baud_cbox.GetValue()),  int(DataBits_cbox.GetValue()), Parity_cbox.GetValue()[0], int(StopBits_cbox.GetValue())) #if Serial port is properly open, then flag =0 after this and we get out of White cycle
                if self.ser.isOpen()== True:
                    break
            else: return False
        if self.debug: print "Port "+SerialPort_cbox.GetValue()+" is open, Baud Rate={0}, Data Bits={1}, Parity={2}, Stop Bits={3}".format(Baud_cbox.GetValue(),DataBits_cbox.GetValue(),Parity_cbox.GetValue(),StopBits_cbox.GetValue())
        
        return True
    #----------------------------------------------------------------------
    def serport(self, port, Baud, DataBits, Parity, StopBits):
        MAXTRY=3
        i=MAXTRY
        while True:
            try:
                if i==0:
                    if self.debug: print "Serial port "+port+" is busy or blocked!"
                    break
                ser=serial.Serial(port, baudrate=Baud, bytesize=DataBits, parity=Parity, stopbits=StopBits, timeout=0.1)
                if ser.port!=port:
                    ser.port=port
                    raise Exception
                break
            except:
                i-=1
                if self.debug: print "For some reason can't open Serial port "+port+". Trying again...("+str(MAXTRY-i)+")"
                ser=serial.Serial()
                ser.port=port
                ser.close()
                time.sleep(0.2)
        return ser  
    #----------------------------------------------------------------------
    def get_lan_ip(self):#currently not used!
        if os.name != "nt":
            import struct, fcntl
            
            def get_interface_ip(ifname):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])
        ip = socket.gethostbyname(socket.gethostname())
        
        if ip.startswith("127.") and os.name != "nt":
            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
            for ifname in interfaces:
                try:
                    ip = get_interface_ip(ifname)
                    break;
                except IOError:
                    pass
        return ip
    #----------------------------------------------------------------------
    def length_calc(self, frame_data):
        framelen=hex(len(frame_data)/2)[2:]
        lframelen=len(framelen)
        length=""
        if lframelen<=4:
            for i in range(4-lframelen):
                length=length+"0"
            length=length+framelen
        elif lframelen<=6:
            for i in range(6-lframelen):
                length=length+"0"
            length=length+framelen
        elif lframelen>6:
            raise Exception
        return length
    #----------------------------------------------------------------------
    def check_sum_calc(self, frame_data):
        res=0
        x=0    
        for i in range(len(frame_data)/2):
            res=res + int(frame_data[x:x+2],16)
            x=x+2
        res=res & 0xFF
        check_sum = '%02x'%(0xFF - res)
        return check_sum
    #----------------------------------------------------------------------
    def print_com(self, command):
        x=0
        com=""
        for i in range(len(command)/2):
            com=com+command[x:x+2]+' '
            x=x+2
        print com.upper()
    #----------------------------------------------------------------------
    def random_data_generator(self):
        self.data_arr=[]
        
        samples=self.samples_textctrl.GetValue()
        if samples=='' or samples=='0':
            self.samples_textctrl.SetValue('1')
            samples==1
        else:
            samples=int(samples)
        count=self.data_bytes_textctrl.GetValue()
        if count=='' or count=='0':
            self.data_bytes_textctrl.SetValue('1')
            count==1
        else:
            count=int(count)
        
        for i in range(0, samples):
            res=''
            for j in range(0, count):
                res=res+'%02X' % random.randint(0,255)
            self.data_arr.append(res)
        '''
        self.data_bytes_textctrl.SetValue('2')
        for i in range(0, samples):
            res='%04X' % i
            self.data_arr.append(res)
        '''
    #----------------------------------------------------------------------
    def bin_file_header_reader(self):
        filename=self.data_file
        fd=None
        try:
            fd=open(filename, "rb")
            
            SR_unit = hexlify(fd.read(1))
            SR_value = int(hexlify(fd.read(2)),16)
            Data_Size = int(hexlify(fd.read(2)),16)
            
            return SR_unit, SR_value, Data_Size
        except KeyboardInterrupt:
            if fd != None: fd.close()
        except Exception, e:
            if self.debug: print e
            if fd != None: fd.close()
    #----------------------------------------------------------------------
    def bin_file_data_extractor(self):
        filename=self.data_file
        self.data_arr=[]
        
        samples=self.samples_textctrl.GetValue()
        if samples=='' or samples=='0':
            self.samples_textctrl.SetValue('1')
            samples==1
        else:
            samples=int(samples)
        
        count=self.data_bytes_textctrl.GetValue()
        if count=='' or count=='0':
            self.data_bytes_textctrl.SetValue('1')
            count==1
        else:
            count=(int(count))/2
        
        fd=None
        try:
            while samples:
                fd=open(filename, "rb")
                fd.read(5)
                while samples:
                    data = fd.read(count)
                    if data and len(data)==count:
                        samples-=1
                        self.data_arr.append(hexlify(data))
                    else:
                        fd.close()
                        break
        except KeyboardInterrupt:
            if fd != None: fd.close()
        except Exception, e:
            if self.debug: print e
            if fd != None: fd.close()
    #----------------------------------------------------------------------
    def TX(self):
        try:
            if self.rand:
                self.random_data_generator()
            else:
                self.bin_file_data_extractor()
            
            SAMPLES=int(self.samples_textctrl.GetValue())
            self.progress_bar.SetRange(SAMPLES)
            
            #Check Sample Rate mode and calculate Sleep in seconds
            sample_rate=self.sample_rate_textctrl.GetValue()
            if sample_rate in ['0','']:
                sample_rate=1
                self.sample_rate_textctrl.SetValue('1')
            else:
                sample_rate=float(sample_rate)
            choice=self.sample_rate_rb.GetStringSelection()
            if choice=='[Hz]':
                SLEEP=1.0/float(sample_rate)
            else:
                SLEEP=float(sample_rate)
            
            choice=self.addressing_type_rb.GetStringSelection()
            if choice.startswith('XBee'):
                #PAN Change
                #self.ser.Open()
                PAN = self.pan_id_textctrl.GetValue()
                frame_data="0801"+hexlify("ID")+PAN
                length = self.length_calc(frame_data)
                check_sum = self.check_sum_calc(frame_data)
                command="7E" + length + frame_data + check_sum
                self.ser.write(unhexlify(command))
                #response=hexlify(self.ser.readall())
                
                #Encryption Disable (if not set)
                if self.encryption_enabled:
                    AT_cmd=hexlify('KY')
                    AT_par=self.encryption_key
                    if len(AT_par) % 2:
                        AT_par='0'+AT_par
                    frame_data="0801"+AT_cmd+AT_par #AT command send
                    length = self.length_calc(frame_data)   
                    check_sum = self.check_sum_calc(frame_data)
                    command="7E" + length + frame_data + check_sum
                    self.ser.write(unhexlify(command))
                    #response=(hexlify(self.ser.readall()))
                    
                    AT_cmd=hexlify('EE')
                    AT_par='01'
                    frame_data="0801"+AT_cmd+AT_par #AT command send
                    length = self.length_calc(frame_data)   
                    check_sum = self.check_sum_calc(frame_data)
                    command="7E" + length + frame_data + check_sum
                    self.ser.write(unhexlify(command))
                    #response=(hexlify(self.ser.readall()))
                else:
                    AT_cmd=hexlify('EE')
                    AT_par='00'
                    frame_data="0801"+AT_cmd+AT_par #AT command send
                    length = self.length_calc(frame_data)   
                    check_sum = self.check_sum_calc(frame_data)
                    command="7E" + length + frame_data + check_sum
                    self.ser.write(unhexlify(command))
                    #response=(hexlify(self.ser.readall()))
            else:
                if self.encryption_enabled: #UDP AES Encryption calrulation here!
                    key = '%016x' % int(self.encryption_key, 16)
                    kSize = len(key)
                    
                    alg = AES(key, keySize=kSize, padding=padWithPadLen())
                    
                    for i in range(0, SAMPLES):
                        self.data_arr[i]=alg.encrypt(self.data_arr[i])
                    
            '''
            XBee S2     - we will use Radios Series2 (ZigBee) Module with explicit addressing (64bit & 16bit) data Transmission
            XBee short  - we will use Radios Series1 (XBee) Module with short addressing (16bit) data Transmission
            XBee long   - we will use Radios Series1 (XBee) Module with long addressing (64bit) data Transmission
            UDP         - we will use standard UDP data Transmission (no Digi Modules involved here)
            '''
            if choice=="XBee S2":
                #self.ser.Open()
                self.S2_TX(SLEEP, SAMPLES)
                #self.ser.Close()
            elif choice=="XBee short":
                #self.ser.Open()
                self.S1_TX_short(SLEEP, SAMPLES)
                #self.ser.Close()
            elif choice=="XBee long":
                #self.ser.Open()
                self.S1_TX_long(SLEEP, SAMPLES)
                #self.ser.Close()
            elif choice=="UDP":
                #self.udp.Open()
                self.UDP_TX(SLEEP, SAMPLES)
                #self.udp.Close()
                
        except KeyboardInterrupt:
            return
    #----------------------------------------------------------------------
    def S2_TX(self, SLEEP, SAMPLES):
        '''S2 TX Request (short + long addressing) API ID= 0x10'''
        try:
            if self.BROADCASTMODE:
                LONG_ADDR,SHORT_ADDR="000000000000FFFF","FFFE" #broadcast
            else:
                LONG_ADDR=self.long_textctrl.GetValue()
                SHORT_ADDR=self.short_textctrl.GetValue()
            
            api_id="10"
            
            count=0
            frame_id=1
            while self.run:
                t1=datetime.datetime.now()
                
                DATA=self.data_arr[count]
                frame_id_str='%02x'% frame_id
                frame_data=api_id+frame_id_str+LONG_ADDR+SHORT_ADDR+"0000"+DATA
                length = self.length_calc(frame_data)   
                check_sum = self.check_sum_calc(frame_data)
                
                command="7E" + length + frame_data + check_sum
                
                self.ser.write(unhexlify(command))
                if self.debug:
                    print "Api command is:"
                    self.print_com(command)
                
                '''getting command response - it will slow down the process and it's turn off'''
                #response=hexlify(self.ser.readall())
                #if self.debug: 
                #   print "xbee response is"
                #   self.print_com(response)
                
                if count < SAMPLES-1:
                    count+=1
                    if frame_id==255:
                        frame_id=1
                    else:
                        frame_id+=1
                else:
                    time.sleep(1)
                    self.OnClickStart_btn()
                    break
                self.progress_bar.SetValue(count)
                
                t2=datetime.datetime.now()
                work_t= t2-t1
                T_sleep=SLEEP-work_t.total_seconds()
                if T_sleep<0: T_sleep=0
                time.sleep(T_sleep)
                
            self.progress_bar.SetValue(0)
            
        except KeyboardInterrupt:
                ser.readall()
                return
    #----------------------------------------------------------------------
    def S1_TX_short(self, SLEEP, SAMPLES):
        '''S1 TX Request (short addressing) API ID= 0x01'''
        try:
            if self.BROADCASTMODE:
                SHORT_ADDR="FFFF" #broadcast
            else:
                SHORT_ADDR=self.short_textctrl.GetValue()
            
            api_id="01"
            
            count=0
            frame_id=1
            while self.run:
                t1=datetime.datetime.now()
                
                DATA=self.data_arr[count]
                frame_id_str='%02x'% frame_id
                frame_data=api_id+frame_id_str+SHORT_ADDR+"00"+DATA
                length = self.length_calc(frame_data)   
                check_sum = self.check_sum_calc(frame_data)
                
                command="7E" + length + frame_data + check_sum
                
                self.ser.write(unhexlify(command))
                if self.debug:
                    print "Api command is:"
                    self.print_com(command)
                
                '''getting command response - it will slow down the process and it's turn off'''
                #response=hexlify(self.ser.readall())
                #if self.debug: 
                #   print "xbee response is"
                #   self.print_com(response)
                
                if count < SAMPLES-1:
                    count+=1
                    if frame_id==255:
                        frame_id=1
                    else:
                        frame_id+=1
                else:
                    time.sleep(1)
                    self.OnClickStart_btn()
                    break
                self.progress_bar.SetValue(count)
                
                t2=datetime.datetime.now()
                work_t= t2-t1
                T_sleep=SLEEP-work_t.total_seconds()
                if T_sleep<0: T_sleep=0
                time.sleep(T_sleep)
                
            self.progress_bar.SetValue(0)
            
        except KeyboardInterrupt:
            ser.readall()
            return
    #----------------------------------------------------------------------
    def S1_TX_long(self, SLEEP, SAMPLES):
        '''S1 TX Request (long addressing) API ID= 0x00'''
        try:
            if self.BROADCASTMODE:
                LONG_ADDR="000000000000FFFF" #broadcast
            else:
                LONG_ADDR=self.long_textctrl.GetValue()
            
            api_id="00"
            
            count=0
            frame_id=1
            while self.run:
                t1=datetime.datetime.now()
                
                DATA=self.data_arr[count]
                frame_id_str='%02x'% frame_id
                frame_data=api_id+frame_id_str+LONG_ADDR+"00"+DATA
                length = self.length_calc(frame_data)   
                check_sum = self.check_sum_calc(frame_data)
                
                command="7E" + length + frame_data + check_sum
                
                self.ser.write(unhexlify(command))
                if self.debug:
                    print "Api command is:"
                    self.print_com(command)
                
                '''getting command response - it will slow down the process and it's turn off'''
                #response=hexlify(self.ser.readall())
                #if self.debug: 
                #   print "xbee response is"
                #   self.print_com(response)
                
                if count < SAMPLES-1:
                    count+=1
                    if frame_id==255:
                        frame_id=1
                    else:
                        frame_id+=1
                else:
                    time.sleep(1)
                    self.OnClickStart_btn()
                    break
                self.progress_bar.SetValue(count)
                
                t2=datetime.datetime.now()
                work_t= t2-t1
                T_sleep=SLEEP-work_t.total_seconds()
                if T_sleep<0: T_sleep=0
                time.sleep(T_sleep)
                
            self.progress_bar.SetValue(0)
            
        except KeyboardInterrupt:
            self.ser.readall()
            return
    #----------------------------------------------------------------------
    def UDP_TX(self, SLEEP, SAMPLES):
        try:
            udp_sock = socket(AF_INET, SOCK_DGRAM)
            address, port = self.udp_port_textctrl.GetValue().split(':')
            port= int(port)
            
            count=0
            while self.run:
                t1=datetime.datetime.now()
                
                DATA=self.data_arr[count]
                
                udp_sock.sendto(DATA, (address, port))
                
                if count < SAMPLES-1:
                    count+=1
                else:
                    time.sleep(1)
                    self.OnClickStart_btn()
                    break
                self.progress_bar.SetValue(count)
                
                t2=datetime.datetime.now()
                work_t= t2-t1
                T_sleep=SLEEP-work_t.total_seconds()
                if T_sleep<0: T_sleep=0
                time.sleep(T_sleep)
                
            self.progress_bar.SetValue(0)
            
            udp_sock.close()
        except KeyboardInterrupt:
            udp_sock.close()