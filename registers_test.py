from etroc_i2c import ETROC_I2C

if __name__ == '__main__':
    # Create instance of ETROC I2C class to communicate with the ETROC via the CERN dongle
    i2c = ETROC_I2C(dongle=1, verbose=1)
    i2c.setupETROC()
    REGA = i2c.r.ETROC_REGA_ADDRESS
    REGB = i2c.r.ETROC_REGB_ADDRESS

    i2c.write_default()
    i2c.read_all_registers()
    #i2c.load_default_no_termination()
    #i2c.RBMUX_test()
    #i2c.set_counter_readout_1G28()
    #i2c.set_DAC_4bits_high()
    #i2c.set_TDC_readout_1G28()
    #i2c.set_random_data()
    #i2c.set_random_data_copy()
    #i2c.set_random_data_copy2_working()
