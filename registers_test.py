from etroc_i2c import ETROC_I2C

if __name__ == '__main__':
    # Want to write/read to/from the MUX: once that works we can use it to write/read RegA/B in ETROC
    # Need to set MUX address E0 to 08: This sets the multiplexer to use ch=03
    # Then we can try write/read to Reg A: set address 03 to FF for example

    i2c = ETROC_I2C(1)    
    i2c.setupETROC()
    REGA = i2c.r.ETROC_REGA_ADDRESS
    REGB = i2c.r.ETROC_REGB_ADDRESS

    print("-"*50)
    commands = [
        ('w', REGA, 0x00, 0xF8),
        ('w', REGA, 0x01, 0x37),
        ('w', REGA, 0x02, 0xFF),
        ('w', REGA, 0x03, 0xFF),
        ('r', REGA, 0x00),
        ('r', REGA, 0x01),
        ('r', REGA, 0x02),
        ('r', REGA, 0x03),
    ]
    #i2c.run(commands)

    print("-"*50)
    commands = [
        ('w', REGB, 0x00, 0x1C),
        ('w', REGB, 0x01, 0x01),
        ('w', REGB, 0x02, 0x00),
        ('w', REGB, 0x03, 0x09),
        ('r', REGB, 0x00),
        ('r', REGB, 0x01),
        ('r', REGB, 0x02),
        ('r', REGB, 0x03),
    ]
    #i2c.run(commands)
    i2c.write_default()
    #i2c.read_all_registers()
    #i2c.load_default_no_termination()
    #i2c.RBMUX_test()
    #i2c.set_counter_readout_1G28()
    #i2c.set_DAC_4bits_high()
    #i2c.set_TDC_readout_1G28()
    #i2c.set_random_data()
    #i2c.set_random_data_copy()
    i2c.set_random_data_copy2_working()
