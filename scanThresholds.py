from etroc_i2c import ETROC_I2C
import os


def add_binary(a, b, shift=8):
    return a<<shift | b

def get_binary_string(a, nBits=8):
    return "{0:{fill}{nBits}b}".format(a, nBits=nBits, fill='0')

def getAllQinj():
    #Gets all possible Qinj values
    allQinj = []
    b = 0b111
    for a in range(0b0, 0b11111 + 0b1):
        c = add_binary(a, b, 3)
        allQinj.append(dict(binary=get_binary_string(c), regA=c))
    return allQinj

def getAllThresholds():
    #Get all possible pixel 1 thresholds
    #000000XX XXXXXXXX
    allThresholds = []
    for regB in range(0b00, 0b111 + 0b1):
        for regA in range(0b00, 0b11111111 + 0b1):
            threshold = add_binary(regB, regA)
            allThresholds.append(dict(binary=get_binary_string(threshold, 16), regB=regB, regA=regA))
    return allThresholds

def getAllThresholdsPixel15():
    #Get all possible pixel 15 thresholds
    #XXXXXXXX XX100000
    constant = 0b100000
    allThresholds = []
    for b in range(0b00, 0b11111111 + 0b1):
        for a in range(0b00, 0b11 + 0b1):
            c = add_binary(a, constant, 6)
            threshold = add_binary(b, a)
            total = add_binary(b, c)
            allThresholds.append(dict(binary=get_binary_string(total, 16), regB=b, regA=c))
    return allThresholds

if __name__ == '__main__':
    # Create instance of ETROC I2C class to communicate with the ETROC via the CERN dongle
    i2c = ETROC_I2C(dongle=2, verbose=1)
    i2c.setupETROC()
    REGA = i2c.r.ETROC_REGA_ADDRESS
    REGB = i2c.r.ETROC_REGB_ADDRESS
    i2c.write_default()
    #i2c.read_all_registers()

    firstRead = []
    allThresholds = getAllThresholds()    
    #allThresholds = getAllThresholdsPixel15()
    for idx, threshold in enumerate(allThresholds):
        #if idx % 64 != 1: continue
        if idx < int(0x175) or idx>int(0x190): continue

        #Reading out Pixel 1
        commands=[
            ('w', i2c.r.ETROC_REGB_ADDRESS, 0x00, 0x1C), # default (1C)
            ('w', i2c.r.ETROC_REGB_ADDRESS, 0x06, 0x41), # disable (40)/enable (41) scrambling
            #('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0x37), # default (37), Q injected amplitude
            ('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0xFF), # default (37), Q injected amplitude
            ('w', i2c.r.ETROC_REGA_ADDRESS, 0x0A, threshold['regA']), # default (00), signal threshold pixel 1
            ('w', i2c.r.ETROC_REGA_ADDRESS, 0x0B, threshold['regB']), # default (02), signal threshold (only first two bits belong to pixel 1 the rest belong to pixel 2)
            ('w', i2c.r.ETROC_REGB_ADDRESS, 0x04, 0x00), # default (00), Phase setting
            ('w', i2c.r.ETROC_REGA_ADDRESS, 0x05, 0x01), ### 01 on, 00 off. disables Q INJ (I2C A REG 05)
            ('w', i2c.r.ETROC_REGA_ADDRESS, 0x06, 0x00),  ### 00 regardless. disables Q INJ (I2C A REG 06)
        ]

        ##Reading out Pixel 15
        #commands=[
        #    ('w', i2c.r.ETROC_REGB_ADDRESS, 0x00, 0x1C), # default (1C)
        #    ('w', i2c.r.ETROC_REGB_ADDRESS, 0x06, 0x40), # disable (40)/enable (41) scrambling
        #    #('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0x37), # default (37), Q injected amplitude
        #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0xFF), # default (37), Q injected amplitude
        #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x05, 0x00), # default (01)
        #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x06, 0x80), # default (00)
        #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x07, 0x38), # default (01)
        #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x1C, threshold['regA']), # default (20), signal threshold pixel 1
        #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x1D, threshold['regB']), # default (80), signal threshold (only first two bits belong to pixel 1 the rest belong to pixel 2)
        #    ('w', i2c.r.ETROC_REGB_ADDRESS, 0x04, 0x00), # default (00), Phase setting
        #]

        i2c.run(commands)
        break
        print("Setting threshold to {} {} {}".format(threshold['binary'], hex(threshold['regB']), hex(threshold['regA'])))
        print(commands)
        #i2c.read_all_registers()

        os.system('./run_read_DebugRAM_2links.sh')
        with open('etl-kcu105-ipbus/etroc_readout.dat') as f:
            lines = f.read().splitlines()
            firstRead.append((threshold['binary'], bin(int(lines[0], 16))))
            #for l in lines:
            #    print(len(lines), l, bin(int(l, 16)))
        #break
        #if idx is 5: break

    for l in firstRead:        
        print(l[0], l[1], int(l[1],2)-0b10000000000000000000000000000000)
