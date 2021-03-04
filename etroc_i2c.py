from usb_dongle import USB_dongle
from etroc_registers import ETROC_Regs
import time

class ETROC_I2C:
    def __init__(self, dongle=1):
        self.my_interface=USB_dongle()
        self.my_interface.i2c_connect(dongle)
        self.r = ETROC_Regs()        

    def mux_write_register(self, register, value):
        """write a value to a register"""
        reg_add=register >> 1
        payload=[value]
        print("sending: {} to register: {}".format(hex(value), hex(register)))
        time.sleep(1)
        self.my_interface.i2c_write(reg_add,payload)
            
    def mux_read_register(self,register):
        """read a value from a register - return register byte value"""
        reg_add=register >> 1
        payload=[reg_add]
        time.sleep(1)
        answer= self.my_interface.i2c_read(reg_add,1)
        print("read register: {} output: {}".format(hex(register),hex(answer[1])))    
        return answer[1]
            
    def etroc_write_register(self,etroc_address,register,value):
        """write a value to a register"""
        etroc_add=etroc_address >> 1
        reg_add=register
        payload=[reg_add]+[value]
        print("sending: {} to register: {}".format(hex(value), hex(register)))
        time.sleep(1)
        self.my_interface.i2c_write(etroc_add,payload)
    
    def etroc_read_register(self,etroc_address,register):
        """read a value from a register - return register byte value"""
        etroc_add=etroc_address >> 1
        reg_add=register
        payload=[reg_add]
        time.sleep(1)
        answer= self.my_interface.i2c_writeread(etroc_add,1,payload)
        print("read register: {} output: {}".format(hex(register), hex(answer[1])))
        if(answer[0] != 0):
            raise Exception("Error with reading internal register {} from {}".format(hex(register), hex(etroc_address)))
        return answer[1]

    def setupETROC(self):
        self.mux_write_register( self.r.MUX_ADDRESS, self.r.MUX_DEFAULT_VALUE)
        #self.mux_read_register( self.r.MUX_ADDRESS)
        
    def run(self, commands):
        for command in commands:
            if command[0] == 'w':
                self.etroc_write_register(command[1], command[2], command[3])
            elif command[0] == 'r':
                output = self.etroc_read_register(command[1], command[2])
            else:
                raise ValueError("Error: {} command not recognized".format(command))

    def write_default(self):
        for key in self.r.ETROC_A_ADDRESS_DICT:
            self.etroc_write_register(self.r.ETROC_REGA_ADDRESS, key, self.r.ETROC_A_ADDRESS_DICT[key]) 
        for key in self.r.ETROC_B_ADDRESS_DICT:
            self.etroc_write_register(self.r.ETROC_REGB_ADDRESS, key, self.r.ETROC_B_ADDRESS_DICT[key])

    def read_all_registers(self):
        for key in self.r.ETROC_A_ADDRESS_DICT:
            self.etroc_read_register(self.r.ETROC_REGA_ADDRESS, key) 
        for key in self.r.ETROC_B_ADDRESS_DICT:
            self.etroc_read_register(self.r.ETROC_REGB_ADDRESS, key)

    def disable_scrambling(self):
        self.run('w', REGB, 0x06, 0x40)



