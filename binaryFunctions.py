
def add_binary(a, b, shift=8):
    return a<<shift | b

def get_binary_string(a, nBits=8):
    return "{0:{fill}{nBits}b}".format(a, nBits=nBits, fill='0')

def set_bit(num, idx, value):
    if value == 1:
        return num | (  1 << idx)
    else:
        return num & (~(1 << idx))

def get_bit(num, idx):
    return int(num & (1 << idx) != 0)

def update_binary_num(nMain, nChange, mask):
    sMain = get_binary_string(nMain)
    sMain = list(sMain)
    sChange = get_binary_string(nChange)

    for i in range(len(sMain)):
        if mask[i] == 'X':
            sMain[i] = sChange[i]
    sMain = ''.join(sMain)
    return int(sMain, 2)

def getAllThresholdsType0(reg1Address, reg2Address):
    #000000XX XXXXXXXX
    #00000010 00000000
    allThresholds = []
    for b in range(0b00, 0b11 + 0b1):
        for a in range(0b00, 0b11111111 + 0b1):
            threshold = add_binary(b, a)
            allThresholds.append(dict(binary=get_binary_string(threshold, 16), reg2=b, reg1=a, reg2Address=reg2Address, reg1Address=reg1Address, mask2='000000XX', mask1='XXXXXXXX'))
    return allThresholds

def getAllThresholdsType1(reg1Address, reg2Address):
    #0000XXXX XXXXXX10
    #00001000 00000010
    constant = 0b10
    allThresholds = []
    for b in range(0b00, 0b1111 + 0b1):
        for a in range(0b00, 0b111111 + 0b1):
            c = add_binary(a, constant, 2)
            threshold = add_binary(b, a)
            total = add_binary(b, c)
            allThresholds.append(dict(binary=get_binary_string(total, 16), reg2=b, reg1=c, reg2Address=reg2Address, reg1Address=reg1Address, mask2='0000XXXX', mask1='XXXXXX10'))
    return allThresholds

def getAllThresholdsType2(reg1Address, reg2Address):
    #00XXXXXX XXXX1000
    #00100000 00001000
    constant = 0b1000
    allThresholds = []
    for b in range(0b00, 0b111111 + 0b1):
        for a in range(0b00, 0b1111 + 0b1):
            c = add_binary(a, constant, 4)
            threshold = add_binary(b, a)
            total = add_binary(b, c)
            allThresholds.append(dict(binary=get_binary_string(total, 16), reg2=b, reg1=c, reg2Address=reg2Address, reg1Address=reg1Address, mask2='00XXXXXX', mask1='XXXX1000'))
    return allThresholds

def getAllThresholdsType3(reg1Address, reg2Address):
    #XXXXXXXX XX100000
    #10000000 00100000
    constant = 0b100000
    allThresholds = []
    for b in range(0b00, 0b11111111 + 0b1):
        for a in range(0b00, 0b11 + 0b1):
            c = add_binary(a, constant, 6)
            threshold = add_binary(b, a)
            total = add_binary(b, c)
            allThresholds.append(dict(binary=get_binary_string(total, 16), reg2=b, reg1=c, reg2Address=reg2Address, reg1Address=reg1Address, mask2='XXXXXXXX', mask1='XX100000'))
    return allThresholds

class pixelInfo:
    def __init__(self, pixelNum, reg1AddressTh, reg2AddressTh, getAllThresholds, grid07, q06, q05):
        self.pixelNum = pixelNum
        self.reg1AddressTh = reg1AddressTh
        self.reg2AddressTh = reg2AddressTh
        self.getAllThresholds = getAllThresholds(reg1AddressTh, reg2AddressTh)
        self.grid07 = grid07
        self.q06 = q06
        self.q05 = q05
        self.baseline = 0
        self.thresholdReg1 = None
        self.thresholdReg2 = None

    def setActiveThresholds(self, idx):
        self.thresholdReg1 = self.getAllThresholds[idx]["reg1"]
        self.thresholdReg2 = self.getAllThresholds[idx]["reg2"]

pixels = {
    0  : pixelInfo( 0, 0x0A, 0x0B, getAllThresholdsType0, 0x01, 0x00, 0x01),
    1  : pixelInfo( 1, 0x0B, 0x0C, getAllThresholdsType1, 0x02, 0x00, 0x02),
    2  : pixelInfo( 2, 0x0C, 0x0D, getAllThresholdsType2, 0x04, 0x00, 0x04),
    3  : pixelInfo( 3, 0x0D, 0x0E, getAllThresholdsType3, 0x08, 0x00, 0x08),
    4  : pixelInfo( 4, 0x0F, 0x10, getAllThresholdsType0, 0x11, 0x00, 0x10),
    5  : pixelInfo( 5, 0x10, 0x11, getAllThresholdsType1, 0x12, 0x00, 0x20),
    6  : pixelInfo( 6, 0x11, 0x12, getAllThresholdsType2, 0x14, 0x00, 0x40),
    7  : pixelInfo( 7, 0x12, 0x13, getAllThresholdsType3, 0x18, 0x00, 0x80),
    8  : pixelInfo( 8, 0x14, 0x15, getAllThresholdsType0, 0x21, 0x01, 0x00),
    9  : pixelInfo( 9, 0x15, 0x16, getAllThresholdsType1, 0x22, 0x02, 0x00),
    10 : pixelInfo(10, 0x16, 0x17, getAllThresholdsType2, 0x24, 0x04, 0x00),
    11 : pixelInfo(11, 0x17, 0x18, getAllThresholdsType3, 0x28, 0x08, 0x00),
    12 : pixelInfo(12, 0x19, 0x1A, getAllThresholdsType0, 0x31, 0x10, 0x00),
    13 : pixelInfo(13, 0x1A, 0x1B, getAllThresholdsType1, 0x32, 0x20, 0x00),
    14 : pixelInfo(14, 0x1B, 0x1C, getAllThresholdsType2, 0x34, 0x40, 0x00),
    15 : pixelInfo(15, 0x1C, 0x1D, getAllThresholdsType3, 0x38, 0x80, 0x00),
}

regThresholdAddresses = {
    0x0A:0x00,
    0x0B:0x02,
    0x0C:0x08,
    0x0D:0x20,
    0x0E:0x80,
    0x0F:0x00,
    0x10:0x02, 
    0x11:0x08,
    0x12:0x20,
    0x13:0x80,
    0x14:0x00,
    0x15:0x02,
    0x16:0x08,
    0x17:0x20,
    0x18:0x80,
    0x19:0x00,
    0x1A:0x02,
    0x1B:0x08,
    0x1C:0x20,
    0x1D:0x80,
}


#for idx, _  in enumerate(getAllThresholdsType0(None, None)):
#    for i, p in pixels.items():
#        p.setActiveThresholds(idx)
#        print p.pixelNum, get_binary_string(p.thresholdReg2), get_binary_string(p.thresholdReg1), p.reg2AddressTh, p.reg1AddressTh, p.getAllThresholds[0]["mask2"], p.getAllThresholds[0]["mask1"]
#
#        regThresholdAddresses[p.reg1AddressTh] = update_binary_num(regThresholdAddresses[p.reg1AddressTh], p.thresholdReg1, p.getAllThresholds[0]["mask1"])
#        regThresholdAddresses[p.reg2AddressTh] = update_binary_num(regThresholdAddresses[p.reg2AddressTh], p.thresholdReg2, p.getAllThresholds[0]["mask2"])
#
#    for i, reg in regThresholdAddresses.items():
#        print i, get_binary_string(reg)

#t0 = getAllThresholdsType0(None, None)
#t1 = getAllThresholdsType1(None, None)
#t2 = getAllThresholdsType2(None, None)
#t3 = getAllThresholdsType3(None, None)
#
#for i, _  in enumerate(t0):
#    print t0[i]["binary"], t1[i]["binary"], t2[i]["binary"], t3[i]["binary"]
