#Boa:Frame:Emulator

import wx  #visual python libs (need wxpython module)
import serial #serial port python libs (need pyserial module)
import os, sys
import time
import string
import random
import threading
from binascii import hexlify, unhexlify

from Panel import XBeePanel, CharValidator, path_to_file

def create(parent):
    return Emulator(parent)

class Emulator(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wx.NewId(), name='', parent=prnt,  
              size=wx.Size(340, 397),#(340,430),
              style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN,
              title='Medical Data Emulator'
        )
        
        self.menu_bar=self.Menu()
        self.SetMenuBar(self.menu_bar)
        
        self.panel = wx.Panel(id=wx.NewId(), name='panel', parent=self)
        
        self.notebook_ctrl = wx.Notebook(self.panel, wx.NewId(), pos=wx.Point(0, 0), size=wx.Size(350,400), name="notebook")
        self.notebook_ctrl.SetBackgroundColour((240,240,240,255))
        
        sensor1 = XBeePanel(self.notebook_ctrl)
        sensor1.debug=self.debug
        sensor2 = XBeePanel(self.notebook_ctrl)
        sensor2.debug=self.debug
        sensor3 = XBeePanel(self.notebook_ctrl)
        sensor3.debug=self.debug
        sensor4 = XBeePanel(self.notebook_ctrl)
        sensor4.debug=self.debug
        sensor5 = XBeePanel(self.notebook_ctrl)
        sensor5.debug=self.debug
        sensor6 = XBeePanel(self.notebook_ctrl)
        sensor6.debug=self.debug
        
        self.notebook_ctrl.AddPage(sensor1, "Sensor 1", True)
        self.notebook_ctrl.AddPage(sensor2, "Sensor 2", False)
        self.notebook_ctrl.AddPage(sensor3, "Sensor 3", False)
        self.notebook_ctrl.AddPage(sensor4, "Sensor 4", False)
        self.notebook_ctrl.AddPage(sensor5, "Sensor 5", False)
        self.notebook_ctrl.AddPage(sensor6, "Sensor 6", False)
        
        status_bar=self.CreateStatusBar()
        
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    def __init__(self, parent):
        self.debug=0
        try: 
            if sys.argv[1]=='debug': self.debug=1
        except: pass
            
        self._init_ctrls(parent)
        
    def Menu(self):
        '''Menubar creation and submenus appending'''
        menu_bar=wx.MenuBar()
        
        S1_AT=wx.Menu()
        S1_Spec=wx.Menu()
        S1_NetSec_Address=wx.Menu()
        S1_NetSec_Id=wx.Menu()
        S1_NetSec_Sec=wx.Menu()
        S1_NetSec=wx.Menu()
        S1_RFInt=wx.Menu()
        S1_Sleep=wx.Menu()
        S1_Diag=wx.Menu()
        S1_Serial=wx.Menu()
        
        S1_Spec.Append(1,"WR","Write")
        S1_Spec.Append(2,"RE","Restore Defaults")
        S1_Spec.Append(3,"FR","Software Reset")
        
        S1_NetSec_Address.Append(4,"CH","Operating Channel")
        S1_NetSec_Address.Append(5,"ID","PAN ID")
        S1_NetSec_Address.Append(6,"MY","16-bit Network Address")
        S1_NetSec_Address.Append(7,"SH","Serial Number High")
        S1_NetSec_Address.Append(8,"SL","Serial Number Low")
        S1_NetSec_Address.Append(9,"RR","XBee Retries")
        S1_NetSec_Address.Append(10,"RN","Random Delay Slots")
        S1_NetSec_Address.Append(11,"MM","MAC Mode")
        
        S1_NetSec_Id.Append(12,"NI","Node Identifier")
        S1_NetSec_Id.Append(13,"ND","Node Discover")
        S1_NetSec_Id.Append(14,"NT","Node Discover Time")
        S1_NetSec_Id.Append(15,"NO","Node Discover Options")
        S1_NetSec_Id.Append(16,"DN","Destination Node")
        S1_NetSec_Id.Append(17,"AI","Association Indication")
        
        S1_NetSec_Sec.Append(18,"EE","AES Encryption Enable")
        S1_NetSec_Sec.Append(19,"KY","AES Encryption Key")
        
        S1_NetSec.AppendMenu(-1,"Addressing",S1_NetSec_Address)
        S1_NetSec.AppendMenu(-1,"Identification",S1_NetSec_Id)
        S1_NetSec.AppendMenu(-1,"Security",S1_NetSec_Sec)
        
        S1_RFInt.Append(20,"PL","Power Level")
        S1_RFInt.Append(21,"CA","CCA Threshold")
        
        S1_Sleep.Append(22,"SM","Sleep Mode")
        S1_Sleep.Append(23,"SO","Sleep Options")
        S1_Sleep.Append(24,"ST","Time Before Sleep")
        S1_Sleep.Append(25,"SP","Cyclic Sleep Period")
        S1_Sleep.Append(26,"DP","Disassociated Cyclic Sleep Period")
        
        S1_Diag.Append(27,"VR","Firmware Version")
        S1_Diag.Append(28,"VL","Firmware Version - Verbose")
        S1_Diag.Append(29,"HV","Hardware Version")
        S1_Diag.Append(30,"DB","Received Signal Strength")
        S1_Diag.Append(31,"EC","CCA Failure")
        S1_Diag.Append(32,"EA","ACK Failure")
        S1_Diag.Append(33,"ED","Energy Scan")
        
        S1_Serial.Append(62,"BD","Interface Data Rate")
        S1_Serial.Append(63,"NB","Parity")
        
        S1_AT.AppendMenu(-1,"Special", S1_Spec)
        S1_AT.AppendMenu(-1,"Networking and Security", S1_NetSec)
        S1_AT.AppendMenu(-1,"RF Interfacing", S1_RFInt)
        S1_AT.AppendMenu(-1,"Sleep (Low Power)", S1_Sleep)
        S1_AT.AppendMenu(-1,"Diagnostics", S1_Diag)
        S1_AT.AppendMenu(-1,"Serial Interfacing", S1_Serial)
        
        S2_AT=wx.Menu()
        S2_Spec=wx.Menu()
        S2_NetSec_Address=wx.Menu()
        S2_NetSec_Id=wx.Menu()
        S2_NetSec_Sec=wx.Menu()
        S2_NetSec=wx.Menu()
        S2_RFInt=wx.Menu()
        S2_Sleep=wx.Menu()
        S2_Diag=wx.Menu()
        S2_Serial=wx.Menu()
        
        S2_Spec.Append(34,"WR","Write")
        S2_Spec.Append(35,"WB","Write Binding Table")
        S2_Spec.Append(36,"RE","Restore Defaults")
        S2_Spec.Append(37,"FR","Software Reset")
        S2_Spec.Append(38,"NR","Network Reset")
        
        S2_NetSec_Address.Append(39,"CH","Operating Channel")
        S2_NetSec_Address.Append(40,"ID","PAN ID")
        S2_NetSec_Address.Append(41,"MY","16-bit Network Address")
        S2_NetSec_Address.Append(42,"MP","16-bit Parent Network Address")
        S2_NetSec_Address.Append(43,"SH","Serial Number High")
        S2_NetSec_Address.Append(44,"SL","Serial Number Low")
        
        S2_NetSec_Id.Append(45,"NI","Node Identifier")
        S2_NetSec_Id.Append(46,"ND","Node Discover")
        S2_NetSec_Id.Append(47,"NT","Node Discover Time")
        S2_NetSec_Id.Append(48,"DN","Destination Node")
        S2_NetSec_Id.Append(49,"JN","Join Notification")
        S2_NetSec_Id.Append(50,"BH","Broadcast Hops")
        S2_NetSec_Id.Append(51,"AI","Association Indication")
        
        S2_NetSec_Sec.Append(52,"EE","AES Encryption Enable")
        S2_NetSec_Sec.Append(53,"KY","AES Encryption Key")
        
        S2_NetSec.AppendMenu(-1,"Addressing",S2_NetSec_Address)
        S2_NetSec.AppendMenu(-1,"Identification",S2_NetSec_Id)
        S2_NetSec.AppendMenu(-1,"Security",S2_NetSec_Sec)
        
        S2_RFInt.Append(54,"PL","Power Level")
        S2_RFInt.Append(55,"PM","Power Mode")
        
        S2_Sleep.Append(56,"SM","Sleep Mode")
        S2_Sleep.Append(57,"SN","Number of Sleep Periods")
        S2_Sleep.Append(58,"ST","Time Before Sleep")
        S2_Sleep.Append(59,"SP","Sleep Period")
        
        S2_Diag.Append(60,"VR","Firmware Version")
        S2_Diag.Append(61,"HV","Hardware Version")
        
        S2_Serial.Append(62,"BD","Interface Data Rate")
        S2_Serial.Append(63,"NB","Parity")
        
        S2_AT.AppendMenu(-1,"Special", S2_Spec)
        S2_AT.AppendMenu(-1,"Networking and Security", S2_NetSec)
        S2_AT.AppendMenu(-1,"RF Interfacing", S2_RFInt)
        S2_AT.AppendMenu(-1,"Sleep (Low Power)", S2_Sleep)
        S2_AT.AppendMenu(-1,"Diagnostics", S2_Diag)
        S2_AT.AppendMenu(-1,"Serial Interfacing", S2_Serial)
        
        Data_Import=wx.Menu()
        Data_Import.Append(90,"ECG","Import ECG File")
        Data_Import.Append(91,"HR","Import HR File")
        Data_Import.Append(92,"SpO2","Import SpO2 File")
        Data_Import.Append(93,"BP","Import BP File")
        Data_Import.Append(94,"RR","Import RR File")
        Data_Import.Append(95,"BG","Import BG File")
        Data_Import.Append(96,"BT","Import BT File")
        
        menu_bar.Append(S1_AT,"S1 AT Commands")
        menu_bar.Append(S2_AT,"S2 AT Commands")
        menu_bar.Append(Data_Import,"Import Data")
        
        
        self.Bind(wx.EVT_MENU, self.OnClickMenu)
        
        self.comm_dict={
            #Series 1 AT Command Info
            1:'Name and Description:\n'+"Write. Write parameter values to non-volatile memory so that parameter modifications\npersist through subsequent power-up or reset.\nNote: Once WR is issued, no additional characters should be sent to the module until\nafter the response OK is received."+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            2:'Name and Description:\n'+"Restore Defaults. Restore module parameters to factory defaults."+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            3:'Name and Description:\n'+"Software Reset. Responds immediately with an OK then performs a hard reset\n~100ms later."+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            
            4:'Name and Description:\n'+"Channel. Set/Read the channel number used for transmitting and receiving data\nbetween RF modules (uses 802.15.4 protocol channel numbers)."+'\nParameter Range:\n'+'0x0B - 0x1A (XBee)'+'\nDefault:\n'+'0x0C (12d)',
            5:'Name and Description:\n'+"PAN ID. Set/Read the PAN (Personal Area Network) ID.\nUse 0xFFFF to broadcast messages to all PANs."+'\nParameter Range:\n'+'0 - 0xFFFF'+'\nDefault:\n'+'0x3332 (13106d)',
            6:'Name and Description:\n'+"16-bit Network Address. Set/Read the RF module 16-bit source address. Set MY =\n0xFFFF to disable reception of packets with 16-bit addresses. 64-bit source address\n(serial number) and broadcast address (0x000000000000FFFF) is always enabled."+'\nParameter Range:\n'+'0 - 0xFFFF'+'\nDefault:\n'+'0',
            7:'Name and Description:\n'+"Serial Number High. Read high 32 bits of the RF module's unique IEEE 64-bit\naddress. 64-bit source address is always enabled."+'\nParameter Range:\n'+'0 - 0xFFFFFFFF [read-only]'+'\nDefault:\n'+'Factory-set',
            8:'Name and Description:\n'+"Serial Number Low. Read low 32 bits of the RF module's unique IEEE 64-bit address.\n64-bit source address is always enabled."+'\nParameter Range:\n'+'0 - 0xFFFFFFFF [read-only]'+'\nDefault:\n'+'Factory-set',
            9:'Name and Description:\n'+"XBee Retries. Set/Read the maximum number of retries the module will execute in\naddition to the 3 retries provided by the 802.15.4 MAC. For each XBee retry, the\n802.15.4 MAC can execute up to 3 retries."+'\nParameter Range:\n'+'0 - 6'+'\nDefault:\n'+'0',
            10:'Name and Description:\n'+"Random Delay Slots. Set/Read the minimum value of the back-off exponent in the\nCSMA-CA algorithm that is used for collision avoidance. If RN = 0, collision avoidance\nis disabled during the first iteration of the algorithm (802.15.4 - macMinBE)."+'\nParameter Range:\n'+'0 - 3 [exponent]'+'\nDefault:\n'+'0',
            11:'Name and Description:\n'+"MAC Mode. MAC Mode. Set/Read MAC Mode value. MAC Mode enables/disables the\nuse of a Digi header in the 802.15.4 RF packet. When Modes 0 or 3 are enabled\n(MM=0,3), duplicate packet detection is enabled as well as certain AT commands.\nPlease see the detailed MM description on page 47 for additional information."+'\nParameter Range:\n'+'0 - 3:  0 = Digi Mode, 1 = 802.15.4 (no ACKs),\n 2 = 802.15.4 (with ACKs), 3 = Digi Mode (no ACKs)'+'\nDefault:\n'+'0',
            
            12:'Name and Description:\n'+"Node Identifier. Stores a string identifier. The register only accepts printable ASCII\ndata. A string can not start with a space. Carriage return ends command. Command will\nautomatically end when maximum bytes for the string have been entered. This string is\nreturned as part of the ND (Node Discover) command. This identifier is also used with\nthe DN (Destination Node) command."+'\nParameter Range:\n'+'20-character ASCII string'+'\nDefault:\n'+'- -',
            13:'Name and Description:\n'+"Node Discover. Discovers and reports all RF modules found. The following information\nis reported for each module discovered (the example cites use of Transparent operation\n(AT command format) - refer to the long ND command description regarding differences\nbetween Transparent and API operation).\nMY<CR>\nSH<CR>\nSL<CR>\nDB<CR>\nNI<CR><CR>\nThe amount of time the module allows for responses is determined by the NT\nparameter. In Transparent operation, command completion is designated by a <CR>\n(carriage return). ND also accepts a Node Identifier as a parameter. In this case, only a\nmodule matching the supplied identifier will respond. If ND self-response is enabled\n(NO=1) the module initiating the node discover will also output a response for itself."+'\nParameter Range:\n'+'optional 20-character NI value'+'\nDefault:\n'+'- -',
            14:'Name and Description:\n'+"Node Discover Time. Set/Read the amount of time a node will wait for responses from\nother nodes when using the ND (Node Discover) command."+'\nParameter Range:\n'+'0x01 - 0xFC [x 100 ms]'+'\nDefault:\n'+'0x19',
            15:'Name and Description:\n'+"Node Discover Options. Enables node discover self-response on the module."+'\nParameter Range:\n'+'0-1'+'\nDefault:\n'+'0',
            16:'Name and Description:\n'+"Destination Node. Resolves an NI (Node Identifier) string to a physical address. The\nfollowing events occur upon successful command execution:\n1. DL and DH are set to the address of the module with the matching Node Identifier.\n2. OK is returned.\n3. RF module automatically exits AT Command Mode\nIf there is no response from a module within 200 msec or a parameter is not specified\n(left blank), the command is terminated and an ERROR message is returned."+'\nParameter Range:\n'+'20-character ASCII string'+'\nDefault:\n'+'- -',
            17:'Name and Description:\n'+"Association Indication. Read errors with the last association request:\n0x00 - Successful Completion - Coordinator successfully started or End Device\nassociation complete\n0x01 - Active Scan Timeout\n0x02 - Active Scan found no PANs\n0x03 - Active Scan found PAN, but the CoordinatorAllowAssociation bit is not set\n0x04 - Active Scan found PAN, but Coordinator and End Device are not\nconfigured to support beacons\n0x05 - Active Scan found PAN, but the Coordinator ID parameter does not match\nthe ID parameter of the End Device\n0x06 - Active Scan found PAN, but the Coordinator CH parameter does not match the\nCH parameter of the End Device\n0x07 - Energy Scan Timeout\n0x08 - Coordinator start request failed\n0x09 - Coordinator could not start due to invalid parameter\n0x0A - Coordinator Realignment is in progress\n0x0B - Association Request not sent\n0x0C - Association Request timed out - no reply was received\n0x0D - Association Request had an Invalid Parameter\n0x0E - Association Request Channel Access Failure. Request was not transmitted -\nCCA failure\n0x0F - Remote Coordinator did not send an ACK after Association Request was sent\n0x10 - Remote Coordinator did not reply to the Association Request, but an ACK was\nreceived after sending the request\n0x11 - [reserved]\n0x12 - Sync-Loss - Lost synchronization with a Beaconing Coordinator\n0x13 - Disassociated - No longer associated to Coordinator\n0xFF - RF Module is attempting to associate"+'\nParameter Range:\n'+'0 - 0x13 [read-only]'+'\nDefault:\n'+'- -',
            
            18:'Name and Description:\n'+"AES Encryption Enable. Disable/Enable 128-bit AES encryption support. Use in\nconjunction with the KY command."+'\nParameter Range:\n'+'0 - 1'+'\nDefault:\n'+'0 (disabled)',
            19:'Name and Description:\n'+"AES Encryption Key. Set the 128-bit AES (Advanced Encryption Standard) key for\nencrypting/decrypting data. The KY register cannot be read."+'\nParameter Range:\n'+'0 - (any 16-Byte value)'+'\nDefault:\n'+'- -',
            
            20:'Name and Description:\n'+"Power Level. Select/Read the power level at which the RF module transmits conducted\npower."+'\nParameter Range:\n'+'0 - 4 (XBee / XBee-PRO): \n0 = -10 / 10 dBm,  1 = -6 / 12 dBm,  2 = -4 / 14 dBm,\n3 = -2 / 16 dBm,  4 = 0 / 18 dBm'+'\nDefault:\n'+'4',
            21:'Name and Description:\n'+"CCA Threshold. Set/read the CCA (Clear Channel Assessment) threshold. Prior to\ntransmitting a packet, a CCA is performed to detect energy on the channel. If the\ndetected energy is above the CCA Threshold, the module will not transmit the packet."+'\nParameter Range:\n'+'0x24 - 0x50 [-dBm]'+'\nDefault:\n'+'0x2C (-44d dBm)',            
            
            22:'Name and Description:\n'+"Sleep Mode. Set/Read Sleep Mode configurations."+'\nParameter Range:\n'+'0 - 5: \n0 = No Sleep, 1 = Pin Hibernate, 2 = Pin Doze, 3 = Reserved,\n4 = Cyclic sleep remote, 5 = Cyclic sleep remote w/ pin wake-up,\n6 = [Sleep Coordinator] for backwards compatibility w/ v1.x6 only;\notherwise use CE command.'+'\nDefault:\n'+'0',
            23:'Name and Description:\n'+"Sleep Options Set/Read the sleep mode options.\nBit 0 - Poll wakeup disable\n0 - Normal operations. A module configured for cyclic sleep will poll for data on waking.\n1 - Disable wakeup poll. A module configured for cyclic sleep will not poll for data on\nwaking.\nBit 1 - ADC/DIO wakeup sampling disable.\n0 - Normal operations. A module configured in a sleep mode with ADC/DIO sampling\nenabled will automatically perform a sampling on wakeup.\n1 - Suppress sample on wakeup. A module configured in a sleep mode with ADC/DIO\nsampling enabled will not automatically sample on wakeup."+'\nParameter Range:\n'+'0-4'+'\nDefault:\n'+'0',
            24:'Name and Description:\n'+"Time before Sleep. <NonBeacon firmware> Set/Read time period of inactivity (no\nserial or RF data is sent or received) before activating Sleep Mode. ST parameter is\nonly valid with Cyclic Sleep settings (SM = 4 - 5).\nCoordinator and End Device ST values must be equal.\nAlso note, the GT parameter value must always be less than the ST value. (If GT > ST,\nthe configuration will render the module unable to enter into command mode.) If the ST\nparameter is modified, also modify the GT parameter accordingly."+'\nParameter Range:\n'+'1 - 0xFFFF [x 1 ms]'+'\nDefault:\n'+'0x1388 (5000d)',
            25:'Name and Description:\n'+"Cyclic Sleep Period. <NonBeacon firmware> Set/Read sleep period for cyclic sleeping\nremotes. Coordinator and End Device SP values should always be equal. To send\nDirect Messages, set SP = 0.\nEnd Device - SP determines the sleep period for cyclic sleeping remotes. Maximum\nsleep period is 268 seconds (0x68B0).\nCoordinator - If non-zero, SP determines the time to hold an indirect message before\ndiscarding it. A Coordinator will discard indirect messages after a period of (2.5 * SP)."+'\nParameter Range:\n'+'0 - 0x68B0 [x 10 ms]'+'\nDefault:\n'+'0',
            26:'Name and Description:\n'+"Disassociated Cyclic Sleep Period. <NonBeacon firmware>\nEnd Device - Set/Read time period of sleep for cyclic sleeping remotes that are\nconfigured for Association but are not associated to a Coordinator. (i.e. If a device is\nconfigured to associate, configured as a Cyclic Sleep remote, but does not find a\nCoordinator, it will sleep for DP time before reattempting association.) Maximum sleep\nperiod is 268 seconds (0x68B0). DP should be > 0 for NonBeacon systems."+'\nParameter Range:\n'+'1 - 0x68B0 [x 10 ms]'+'\nDefault:\n'+'0x3E8 (1000d)',
            
            27:'Name and Description:\n'+"Firmware Version. Read firmware version of the RF module."+'\nParameter Range:\n'+'0 - 0xFFFF [read-only]'+'\nDefault:\n'+'Factory-set',
            28:'Name and Description:\n'+"Firmware Version - Verbose. Read detailed version information (including application\nbuild date, MAC, PHY and bootloader versions). The VL command has been\ndeprecated in version 10C9. It is not supported in firmware versions after 10C8"+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            29:'Name and Description:\n'+"Hardware Version. Read hardware version of the RF module."+'\nParameter Range:\n'+'0 - 0xFFFF [read-only]'+'\nDefault:\n'+'Factory-set',
            30:'Name and Description:\n'+"Received Signal Strength. Read signal level [in dB] of last good packet received\n(RSSI). Absolute value is reported. (For example: 0x58 = -88 dBm) Reported value is\naccurate between -40 dBm and RX sensitivity."+'\nParameter Range:\n'+'0x17-0x5C (XBee) [read-only]'+'\nDefault:\n'+'- -',
            31:'Name and Description:\n'+"CCA Failures. Reset/Read count of CCA (Clear Channel Assessment) failures. This\nparameter value increments when the module does not transmit a packet because it\ndetected energy above the CCA threshold level set with CA command. This count\nsaturates at its maximum value. Set count to 0 to reset count."+'\nParameter Range:\n'+'0 - 0xFFFF'+'\nDefault:\n'+'- -',
            32:'Name and Description:\n'+"ACK Failures. Reset/Read count of acknowledgment failures. This parameter value\nincrements when the module expires its transmission retries without receiving an ACK\non a packet transmission. This count saturates at its maximum value. Set the parameter\nto 0 to reset count."+'\nParameter Range:\n'+'0 - 0xFFFF'+'\nDefault:\n'+'- -',
            33:'Name and Description:\n'+"Energy Scan. Send Energy Detect Scan. ED parameter determines the length of scan\non each channel. The maximal energy on each channel is returned and each value is\nfollowed by a carriage return. Values returned represent detected energy levels in units\nof -dBm. Actual scan time on each channel is measured as Time = [(2 ^ SD) * 15.36]\nms. Total scan time is this time multiplied by the number of channels to be scanned."+'\nParameter Range:\n'+'0-6'+'\nDefault:\n'+'- -',
            
            #Series 2 AT Command Info
            34:'Name and Description:\n'+"Write. Write parameter values to non-volatile memory so that parameter modifications\npersist through subsequent resets.\nNote: Once WR is issued, no additional characters should be sent to the module until\nafter the OK response is received."+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            35:'Name and Description:\n'+"Write Binding Table: Writes the current binding table to non-volative memory."+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            36:'Name and Description:\n'+"Restore Defaults. Restore module parameters to factory defaults. RE command does\nnot reset the ID parameter."+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            37:'Name and Description:\n'+"Software Reset. Reset module. Responds immediately with an OK then performs a\nreset ~2 seconds later. Use of the FR command will cause a network layer restart on the\nnode if SC or ID were modified since the last reset."+'\nParameter Range:\n'+'- -'+'\nDefault:\n'+'- -',
            38:'Name and Description:\n'+"Network Reset. Reset network layer parameters on one or more modules within a PAN.\nResponds immediately with an OK then causes a network restart. All network\nconfiguration and routing information is consequently lost.\nIf NR = 0: Resets network layer parameters on the node issuing the command.\nIf NR = 1: Sends broadcast transmission to reset network layer parameters on all\nnodes in the PAN."+'\nParameter Range:\n'+'0-1'+'\nDefault:\n'+'- -',
            
            39:'Name and Description:\n'+"Operating Channel. Read the channel number used for transmitting and receiving\nbetween RF modules. Uses 802.15.4 channel numbers."+'\nParameter Range:\n'+'0, 0x0B-0x1A (XBee)'+'\nDefault:\n'+'0',
            40:'Name and Description:\n'+"PAN ID. Set/Get the PAN (Personal Area Network) ID.\nCoordinator - Set the preferred Pan ID. Set (ID = 0xFFFF) to auto-select.\nRouter / End Device - Set the desired Pan ID. When the device searches for a\nCoordinator, it attempts to only join to a parent that has a matching Pan ID. Set (ID =\n0xFFFF) to join a parent operating on any Pan ID.\nChanges to ID should be written to non-volatile memory using the WR command. ID\nchanges are not used until the module is reset (FR, NR or power-up)."+'\nParameter Range:\n'+'0 - 0x3FFF, 0xFFFF'+'\nDefault:\n'+'0x0234 (291d)',
            41:'Name and Description:\n'+"16-bit Network Address. Get the 16-bit Network Address of the module."+'\nParameter Range:\n'+'0 - 0xFFFE [read-only]'+'\nDefault:\n'+'0xFFFE',
            42:'Name and Description:\n'+"16-bit Parent Network Address. Get the 16-bit parent Network Address of the module."+'\nParameter Range:\n'+'0 - 0xFFFE [read-only]'+'\nDefault:\n'+'0xFFFE',
            43:'Name and Description:\n'+"Serial Number High. Read high 32 bits of the RF module's unique IEEE 64-bit\naddress. 64-bit source address is always enabled."+'\nParameter Range:\n'+'0 - 0xFFFFFFFF [read-only]'+'\nDefault:\n'+'factory-set',
            44:'Name and Description:\n'+"Serial Number Low. Read low 32 bits of the RF module's unique IEEE 64-bit address.\n64-bit source address is always enabled."+'\nParameter Range:\n'+'0 - 0xFFFFFFFF [read-only]'+'\nDefault:\n'+'factory-set',
            
            45:'Name and Description:\n'+"Node Identifier. Stores a string identifier. The register only accepts printable ASCII\ndata. In AT Command Mode, a string can not start with a space. A carriage return ends\nthe command. Command will automatically end when maximum bytes for the string\nhave been entered. This string is returned as part of the ND (Node Discover) command.\nThis identifier is also used with the DN (Destination Node) command."+'\nParameter Range:\n'+'20-Byte printable ASCII string'+'\nDefault:\n'+'- -',
            46:'Name and Description:\n'+"Node Discover. Discovers and reports all RF modules found. The following information\nis reported for each module discovered.\nMY<CR>\nSH<CR>\nSL<CR>\nNI<CR> (Variable length)\nPARENT_NETWORK ADDRESS (2 Bytes)<CR>\nDEVICE_TYPE<CR> (1 Byte: 0=Coord, 1=Router, 2=End Device)\nSTATUS<CR> (1 Byte: Reserved)\nPROFILE_ID<CR> (2 Bytes)\nMANUFACTURER_ID<CR> (2 Bytes)\n<CR>\nAfter (NT * 100) milliseconds, the command ends by returning a <CR>. ND also accepts\na Node Identifier (NI) as a parameter (optional). In this case, only a module that\nmatches the supplied identifier will respond.\nIf ND is sent through the API, each response is returned as a separate\nAT_CMD_Response packet. The data consists of the above listed bytes without the\ncarriage return delimiters. The NI string will end in a 0x00 null character."+'\nParameter Range:\n'+'optional 20-Byte NI or MY value'+'\nDefault:\n'+'- -',
            47:'Name and Description:\n'+"Node Discover Timeout. Set/Read the amount of time a node will spend discovering\nother nodes when ND or DN is issued."+'\nParameter Range:\n'+'0 - 0xFC [x 100 msec]'+'\nDefault:\n'+'0x3C (60d)',
            48:'Name and Description:\n'+"Destination Node. Resolves an NI (Node Identifier) string to a physical address\n(casesensitive). The following events occur after the destination node is discovered:\n<AT Firmware>\n1. DL & DH are set to the extended (64-bit) address of the module with the matching\nNI (Node Identifier) string.\n2. OK (or ERROR)\r is returned.\n3. Command Mode is exited to allow immediate communication\n<API Firmware>\n1. The 16-bit network and 64-bit extended addresses are returned in an API\nCommand Response frame.\nIf there is no response from a module within (NT * 100) milliseconds or a parameter is\nnot specified (left blank), the command is terminated and an ERROR message is\nreturned. In the case of an ERROR, Command Mode is not exited."+'\nParameter Range:\n'+'up to 20-Byte printable ASCII string'+'\nDefault:\n'+'- -\n',
            49:'Name and Description:\n'+"Join Notification. Set/read the join notification value. If enabled, the device will send a\ntransmission after joining a PAN identifying itself to other devices in the PAN."+'\nParameter Range:\n'+'0 - Join notification disabled, 1 - Send notification only to coordinator after joining PAN,\n2 - Send notification as broadcast transmission after joining PAN'+'\nDefault:\n'+'0',
            50:'Name and Description:\n'+"Broadcast Hops. Set/Read the maximum number of hops for each broadcast data\ntransmission. Setting this to 0 will use the maximum number of hops."+'\nParameter Range:\n'+'0 - 0x0F'+'\nDefault:\n'+'0',
            51:'Name and Description:\n'+"Association Indication. Read information regarding last node join request:\n0x00 - Successful completion - Coordinator started or Router/End Device found and\njoined with a parent.\n0x21 - Scan found no PANs\n0x22 - Scan found no valid PANs based on current SC and ID settings\n0x23 - Valid Coordinator or Routers found, but they are not allowing joining (NJ expired)\n0x27 - Node Joining attempt failed\n0x2A - Coordinator Start attempt failed\n0xFF - Scanning for a Parent"+'\nParameter Range:\n'+'0 - 0xFF [read-only]'+'\nDefault:\n'+'- -',
            
            52:'Name and Description:\n'+"AES Encryption Enable. Disable/Enable 128-bit AES encryption support. Use in\nconjunction with the KY command."+'\nParameter Range:\n'+'0 - 1'+'\nDefault:\n'+'0 (disabled)',
            53:'Name and Description:\n'+"AES Encryption Key. Set the 128-bit AES (Advanced Encryption Standard) key for\nencrypting/decrypting data. The KY register cannot be read."+'\nParameter Range:\n'+'0 - (any 16-Byte value)'+'\nDefault:\n'+'- -',
            
            54:'Name and Description:\n'+"Power Level. Select/Read the power level at which the RF module transmits conducted\npower."+'\nParameter Range:\n'+'0 - 4 (XBee):\n0 = -10 / 10 dBm, 1 = -6 / 12 dBm, 2 = -4 / 14 dBm,\n3 = -2 / 16 dBm, 4 = 0 / 18 dBm'+'\nDefault:\n'+'4',
            55:'Name and Description:\n'+"Power Mode. Set/read the power mode of the device. Enabling boost mode will improve\nthe receive sensitivity by 1dB and increase the transmit power by 2dB"+'\nParameter Range:\n'+'0-1: 0= -Boost mode disabled, 1= Boost mode enabled.'+'\nDefault:\n'+'1',
            
            56:'Name and Description:\n'+"Sleep Mode Sets the sleep mode on the RF module"+'\nParameter Range:\n'+'0-Sleep disabled\n1-Pin sleep enabled\n4-Cyclic sleep enabled.\nNote: When SM=0, the device operates as a router. When SM changes to a non-zero\nvalue, the router leaves the network and rejoins as an end device.\nOnly end devices can sleep.'+'\nDefault:\n'+'0',
            57:'Name and Description:\n'+"Number of Sleep Periods. Sets the number of sleep periods to not assert the On/Sleep\npin on wakeup if no RF data is waiting for the end device. This command allows a host\napplication to sleep for an extended time if no RF data is present"+'\nParameter Range:\n'+'1-0xFF'+'\nDefault:\n'+'1',
            58:'Name and Description:\n'+"Time Before Sleep Sets the time before sleep timer on an end device.The timer is reset\neach time serial or RF data is received. Once the timer expires, an end device may enter\nlow power operation. Applicable for cyclic sleep end devices only."+'\nParameter Range:\n'+'1 - 0xFFFE (x 1ms)'+'\nDefault:\n'+'0x1388 (5 seconds)',
            59:'Name and Description:\n'+"Sleep Period. This value determines how long the end device will sleep at a time, up to\n28 seconds. (The sleep time can effectively be extended past 28 seconds using the SN\ncommand.) On the parent, this value determines how long the parent will buffer a\nmessage for the sleeping end device. It should be set at least equal to the longest SP\ntime of any child end device."+'\nParameter Range:\n'+'0x20 - 0xAF0 x 10ms (Quarter second resolution)'+'\nDefault:\n'+'0x7D0 (20 seconds)',
            
            60:'Name and Description:\n'+"Firmware Version. Read firmware version of the module."+'\nParameter Range:\n'+'0 - 0xFFFF [read-only]'+'\nDefault:\n'+'Factory-set',
            61:'Name and Description:\n'+"Hardware Version. Read hardware version of the module."+'\nParameter Range:\n'+'0 - 0xFFFF [read-only]'+'\nDefault:\n'+'Factory-set',
            
            62:'Name and Description:\n'+"Interface Data Rate. Set/Reed the serial interface data rate for communications\nbetween the RF module serial port and host."+'\nParameter Range:\n'+'0-7 (standard baud rates):\n0=1200, 1=2400, 2=4800, 3=9600,\n4=19200, 5=38400, 6=57600, 7=115200'+'\nDefault:\n'+'3',
            63:'Name and Description:\n'+"Parity. Set/Reed parity settings."+'\nParameter Range:\n'+'0-4:\n 0=NONE, 1=EVEN, 2=ODD,\n 3=MARK, 4=SPACE. '+'\nDefault:\n'+'0'
            }
        
        return menu_bar
    #----------------------------------------------------------------------
    #Event related functions:
    #----------------------------------------------------------------------
    def OnClickMenu(self, event):
        id = event.GetId()
        if(id<90):
            self.OnClickATMenu(event)
        else:
            self.OnClickDataImportMenu(event)
    
    def OnClickATMenu(self, event):
        id = event.GetId()
        menu=self.menu_bar
        AT_cmd = menu.GetLabel(id)
        flag=0
        if AT_cmd in ('NI','ND','DN'):
            flag=1 #AT_par will be string, else it will be HEX
        string=self.comm_dict.get(id)
        x=450
        y=(string.count('\n')+1)*14+100
        dlg = wx.Dialog(self, -1, title='AT Command '+AT_cmd, size=(x,y))
        wx.StaticText(dlg, -1, AT_cmd+" Parameters:", pos=(10,10))
        if(flag==1):
            text_box=wx.TextCtrl(dlg, -1, pos=(12,35),size=(300,-1))
        else:
            text_box=wx.TextCtrl(dlg, -1, pos=(12,35),size=(300,-1), validator=CharValidator('HEX'))
        btn = wx.Button(dlg, id=wx.ID_OK, label="Execute Command", pos=(312,34), size=(x-327,-1))
        wx.StaticText(dlg, -1, string, pos=(10,65),size=(x-20,-1), style=wx.TE_MULTILINE)
        
        if (dlg.ShowModal()==wx.ID_OK):
            AT_par=text_box.GetValue()
            if (flag==1):
                AT_par=hexlify(AT_par) #parameters are an ASCII string and we convert them to HEX
            else:
                if((len(AT_par)%2)!=0):
                    AT_par='0'+AT_par #parameters are a HEX string and if they are not even we add zero infront
            AT_cmd=hexlify(AT_cmd)
            
            page_obj=self.notebook_ctrl.GetPage(self.notebook_ctrl.GetSelection())
            
            if not page_obj.ser.isOpen():
                    if not page_obj.ser_open(): return
            
            frame_data="0801"+AT_cmd+AT_par #AT command send
            length = page_obj.length_calc(frame_data)
            check_sum = page_obj.check_sum_calc(frame_data)
            command="7E" + length + frame_data + check_sum
            if self.debug: 
                print 'command:'
                page_obj.print_com(command)
            page_obj.ser.write(unhexlify(command))
            response=(hexlify(page_obj.ser.readall()))
            if self.debug: 
                print 'response:'
                page_obj.print_com(response)
            
            if response[14:16]=='00' :
                if(flag==1):
                    cmd_response=unhexlify(response[16:-2])
                else:
                    cmd_response=response[16:-2]
                
                if ((AT_cmd != hexlify("WR")) and (len(AT_par)==0)):
                    msg=wx.MessageDialog(self, "OK\nvalue: "+cmd_response , caption="Response", style=wx.OK|wx.CENTRE)
                    if self.debug: print "Response: OK, Return value: "+ cmd_response
                else:
                    msg=wx.MessageDialog(self, "OK", caption="Response", style=wx.OK|wx.CENTRE)
                    if self.debug: print "Response: OK"
            else:
                msg=wx.MessageDialog(self, "ERROR", caption="Response", style=wx.OK|wx.CENTRE|wx.ICON_ERROR)
                if self.debug: print "Response: Error"
            msg.ShowModal()
    #----------------------------------------------------------------------
    def OnClickDataImportMenu(self, event):
        import shutil
        id = event.GetId()
        menu=self.menu_bar
        data_name = menu.GetLabel(id)
        fileopen = wx.FileDialog(self,"Import "+data_name+" File", defaultDir=os.getcwd(),
            wildcard="Binary Files (*.bin)|*.bin" ,style=wx.FD_OPEN)
        if (fileopen.ShowModal() == wx.ID_OK):
            file_source=fileopen.GetPath()
            file_destination=path_to_file+data_name.lower()+'.bin'
            shutil.copyfile(file_source, file_destination)
            if self.debug: print Success
    
    def OnClose(self, event):
        self.notebook_ctrl.GetPage(0).work_thr._Thread__stop()
        self.notebook_ctrl.GetPage(1).work_thr._Thread__stop()
        self.notebook_ctrl.GetPage(2).work_thr._Thread__stop()
        self.notebook_ctrl.GetPage(3).work_thr._Thread__stop()
        self.notebook_ctrl.GetPage(4).work_thr._Thread__stop()
        self.notebook_ctrl.GetPage(5).work_thr._Thread__stop()
        try: 
            wx.Window.Destroy(self)
        except: pass
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
