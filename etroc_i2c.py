from usb_dongle import USB_dongle
from etroc_registers import ETROC_Regs
import time

class ETROC_I2C:
    def __init__(self, dongle=1, verbose=None):
        self.my_interface=USB_dongle(dongle)
        self.my_interface.i2c_connect(1)
        self.r = ETROC_Regs()        
        self.verbose = verbose
        self.delay = 0.01

    def mux_write_register(self, register, value):
        """write a value to a register"""
        reg_add=register >> 1
        payload=[value]
        if self.verbose is 1:
            print("sending: {} to register: {}".format(hex(value), hex(register)))
        time.sleep(self.delay)
        self.my_interface.i2c_write(reg_add,payload)
            
    def mux_read_register(self,register):
        """read a value from a register - return register byte value"""
        reg_add=register >> 1
        payload=[reg_add]
        time.sleep(self.delay)
        answer= self.my_interface.i2c_read(reg_add,1)
        if self.verbose is 1:
            print("read register: {} output: {}".format(hex(register),hex(answer[1])))    
        return answer[1]
            
    def etroc_write_register(self,etroc_address,register,value):
        """write a value to a register"""
        etroc_add=etroc_address >> 1
        reg_add=register
        payload=[reg_add]+[value]
        if self.verbose is 1:
            REG = "A" if hex(etroc_address)==hex(self.r.ETROC_REGA_ADDRESS) else "B"
            print("sending: {} to register: {}-{}".format(hex(value), REG, hex(register)))
        time.sleep(self.delay)
        self.my_interface.i2c_write(etroc_add,payload)
    
    def etroc_read_register(self,etroc_address,register):
        """read a value from a register - return register byte value"""
        etroc_add=etroc_address >> 1
        reg_add=register
        payload=[reg_add]
        time.sleep(self.delay)
        answer= self.my_interface.i2c_writeread(etroc_add,1,payload)
        if self.verbose is 1:
            REG = "A" if hex(etroc_address)==hex(self.r.ETROC_REGA_ADDRESS) else "B"
            print("read register:{}-{} output: {}".format(REG, hex(register), hex(answer[1])))
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
        for key in self.r.ETROC_REGA_ADDRESS_DICT:
            self.etroc_write_register(self.r.ETROC_REGA_ADDRESS, key, self.r.ETROC_REGA_ADDRESS_DICT[key]) 
        for key in self.r.ETROC_REGB_ADDRESS_DICT:
            self.etroc_write_register(self.r.ETROC_REGB_ADDRESS, key, self.r.ETROC_REGB_ADDRESS_DICT[key])

    def read_all_registers(self):
        for key in self.r.ETROC_REGA_ADDRESS_DICT:
            self.etroc_read_register(self.r.ETROC_REGA_ADDRESS, key) 
        for key in self.r.ETROC_REGB_ADDRESS_DICT:
            self.etroc_read_register(self.r.ETROC_REGB_ADDRESS, key)

    def disable_scrambling(self):
        self.run('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0x40)

    def load_default(self):
        self.setupETROC()
        self.write_default()
        self.read_all_registers()

    def load_default_no_termination(self):
        self.setupETROC()
        for key in self.r.ETROC_REGA_ADDRESS_DICT:
            self.etroc_write_register(self.r.ETROC_REGA_ADDRESS, key, self.r.ETROC_REGA_ADDRESS_DICT[key]) 
        commands = [
            ('w', self.r.ETROC_REGB_ADDRESS, 0x00, 0x1C),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x01, 0x01),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x02, 0x00),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x03, 0x09),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x04, 0x00),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x05, 0x03),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0x41),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x07, 0x30),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x08, 0x18),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x09, 0x18),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x0A, 0x30),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x0B, 0x77),
        ]
        self.run(commands)   
        self.read_all_registers() 
   
    def RBMUX_test(self):
        self.setupETROC()
        commands= [
            ('w', self.r.ETROC_REGA_ADDRESS, 0x01, 0xA0),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x01),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x01),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x01, 0x05),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x01),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x01),
        ]
        self.run(commands)   


    def set_counter_readout_1G28(self):
        self.setupETROC()
        commands= [
            ('w', self.r.ETROC_REGB_ADDRESS, 0x00, 0x1E),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0x40),
            ('w', self.r.ETROC_REGA_ADDRESS, 0x0A, 0x0F),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x00),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x06),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x0A),
        ]
        self.run(commands)

    def set_DAC_4bits_high(self):
        commands= [
            ('w', self.r.ETROC_REGA_ADDRESS, 0x0A, 0x0F),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x0A),
        ]
        self.run(commands)

    def set_DAC_4bits_low(self):
        commands= [
            ('w', self.r.ETROC_REGA_ADDRESS, 0x0A, 0x00),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x0A),
        ]
        self.run(commands)

    def set_TDC_readout_1G28(self):
        self.setupETROC() 
        commands=[
            ('w', self.r.ETROC_REGB_ADDRESS, 0x00, 0x1C), # default (1C)
            ('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0x40), # disable (40)/enable (41) scrambling
            ('w', self.r.ETROC_REGA_ADDRESS, 0x01, 0x37), # default (37), Q injected amplitude
            ('w', self.r.ETROC_REGA_ADDRESS, 0x0A, 0x00), # default (00), signal threshold pixel 1
            ('w', self.r.ETROC_REGA_ADDRESS, 0x0B, 0x02), # default (02), signal threshold (only first two bits belong to pixel 1 the rest belong to pixel 2)
        ]
        self.run(commands)

    def enable_scrambling(self):
        commands= [
            ('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0x41), # disable (40)/enable (41) scrambling
        ]
        self.run(commands)

    def set_random_data(self):
        self.setupETROC()
        commands=[
            ('r', self.r.ETROC_REGB_ADDRESS, 0x06),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0x49),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x06),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x07),
        ]
        self.run(commands)
   
    def set_random_data_copy(self):
        self.setupETROC()
        commands=[
            ('r', self.r.ETROC_REGB_ADDRESS, 0x00),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0xFA),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x06),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x07),
        ]
        self.run(commands)

    def set_random_data_copy2(self):
        self.setupETROC()
        commands=[
            ('r', self.r.ETROC_REGB_ADDRESS, 0x00),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x00, 0xFA),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x00),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x07),
        ]
        self.run(commands) 

    def set_random_data_copy2_working(self):
        self.setupETROC()
        commands=[
            ('r', self.r.ETROC_REGB_ADDRESS, 0x00),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x00, 0xFA),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x00),
            ('r', self.r.ETROC_REGB_ADDRESS, 0x06),
            ('w', self.r.ETROC_REGB_ADDRESS, 0x06, 0x40), 
            ('r', self.r.ETROC_REGB_ADDRESS, 0x06),
            ('r', self.r.ETROC_REGA_ADDRESS, 0x07),
        ]
        self.run(commands)  
