from etroc_i2c import ETROC_I2C

if __name__ == '__main__':
    # Create instance of ETROC I2C class to communicate with the ETROC via the CERN dongle
    i2c = ETROC_I2C(dongle=2, verbose=1)
    i2c.setupETROC()
    REGA = i2c.r.ETROC_REGA_ADDRESS
    REGB = i2c.r.ETROC_REGB_ADDRESS

    # --------------------------------------
    # Write defaults first then change to the mode you want to use
    # --------------------------------------
    i2c.write_default()
    #i2c.read_all_registers()
    #i2c.load_default_no_termination()

    # --------------------------------------
    # Set ETROC to counter readout mode with 4 bits high or 4 bits low
    # --------------------------------------
    #i2c.set_counter_readout_1G28(); i2c.set_DAC_4bits_high()
    #i2c.set_counter_readout_1G28(); i2c.set_DAC_4bits_low()

    # --------------------------------------
    # Set ETROC to TDC mode
    # --------------------------------------
    i2c.set_TDC_readout_1G28()

    # --------------------------------------
    # Extra settings
    # --------------------------------------
    #i2c.RBMUX_test()
    #i2c.set_random_data()
    #i2c.set_random_data_copy()
    #i2c.set_random_data_copy2_working()

    print("-"*50)
    i2c.read_all_registers()
