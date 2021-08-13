#!/bin/env python

import random # For randint
import sys # For sys.argv and sys.exit
import uhal
import time
import optparse

from descrambler import descramble
from binaryFunctions import get_binary_string

def allignWord(binstring, wordsize, pattern, persist = 10, secPattern = None, offsetSecPattern = 0):
    for x in range(len(binstring)):
        alligned = True
        for index in range(persist):
            if(binstring[x+index*wordsize:x+index*wordsize+len(pattern)] != pattern):
                alligned = False
            elif(offsetSecPattern > 0 and  binstring[x+offsetSecPattern+index*wordsize:x+offsetSecPattern+index*wordsize+len(secPattern)] != secPattern   ): 
                alligned = False
        if(alligned):
            return x
    print("-"*50)
    print("Didn't find an offset for the \"{}\" pattern that persisted for \"{}\" words".format(pattern, persist))

def checkLockWrite(binstring, wordsize, pattern):
    lockLoss = False
    words = []
    lastGoodBitIdx = 0
    for x in range(0, len(binstring), wordsize):
        lastGoodBitIdx = x
        word = binstring[x:x+wordsize]
        words.append(hex(int(word, 2)))
        #print int(word, 2), hex(int(word, 2)), word

        if(binstring[x:x+len(pattern)] != pattern):
            #print "lock loss: ", x
            lockLoss = True
            break
    return lockLoss, words, lastGoodBitIdx

def readout(reset = 0, mode = 'tdc', scrambled = False): 
    uhal.disableLogging()
    connectionFilePath = "/home/daq/etltest_0721/etltests_0721/etl-kcu105-ipbus/Real_connections.xml"
    deviceId = "KCU105real"

    # PART 2: Creating the HwInterface
    connectionMgr = uhal.ConnectionManager("file://" + connectionFilePath);
    hw = connectionMgr.getDevice(deviceId);
    TOFHIR_status    = hw.getNode("LINK1_status")
    debug_RAM1 		 = hw.getNode("Tx1_debug_RAM")
    debug_RAM1_start = hw.getNode("Tx1_debug_RAM_start")
    debug_RAM0 		 = hw.getNode("Tx0_debug_RAM")
    debug_RAM0_start = hw.getNode("Tx0_debug_RAM_start")
    rst_Rx1_addr_cnt = hw.getNode("rst_Rx1_addr_cnt")
    rst_Rx0_addr_cnt = hw.getNode("rst_Rx0_addr_cnt")

    Nword = 8
    Value = []
    MEM0 = []
    MEM1 = []
    wait = 1
    TxValue = reset  
    Value = 1
    depth = 128*2
    Nword = depth*8

    debug_RAM1_start.write(int(Value)); 
    hw.dispatch();
    time.sleep(wait) # wait 1 sec

    #"----------- data in output lpGBT uplink for each e-port ------------"
    MEM0_decode = []
    MEM1_decode = []
    MEM0=debug_RAM0.readBlock(int(Nword));
    hw.dispatch();
    MEM1=debug_RAM1.readBlock(int(Nword));
    hw.dispatch();
    
    #"--------------------- link 0 -------------------------"
    FrameData = 0
    xx = 0
    yy = 0
    for x in range(7): 
       MEM0_decode.append( 0 )
       MEM1_decode.append( 0 )

    for x in range(int(Nword)): 
         if yy == 7:
            yy = 0
            xx = xx + 1
            FrameData = 0
         else : 
            FrameData = ((MEM0[x]&0xFFFFFFFF)<<xx*32)
            MEM0_decode[yy] = MEM0_decode[yy] + FrameData;
            yy = yy + 1 

    #"--------------------- link 1 -------------------------"
    FrameData = 0
    xx = 0
    yy = 0
    for x in range(int(Nword)-1, -1 , -1): 
        if yy == 7:
            yy = 0
            xx = xx + 1
            FrameData = 0
        else : 
            FrameData = ((MEM1[x]&0xFFFFFFFF)<<xx*32)
            MEM1_decode[yy] = MEM1_decode[yy] + FrameData;
            yy = yy + 1 

    #########################################
    # Determine header offset for the buffer
    #########################################
    frame = bin(MEM1_decode[6])

    offset = None
    if mode == 'counter':
        offset = allignWord(frame,32,"10", 16, "10101010", 2)
    elif mode == 'tdc':
        offset = allignWord(frame,32,"10", 16)
    elif mode == 'constant':
        offset = 28

    #print "offset for the allignment: ", offset
    lockedFrame = frame[offset:]
    #print lockedFrame

    #offset = allignWord(frame,32,"01", 16)    
    #print "offset for the false allignment: ", offset
    lockloss, words, lastGoodBitIdx = checkLockWrite(lockedFrame,32,"10")

    tryAgain = True
    if tryAgain and lockloss and lastGoodBitIdx > 32*10:
        lockloss, words, lastGoodBitIdx = checkLockWrite(lockedFrame[:lastGoodBitIdx],32,"10")

    if scrambled:
        words = descramble(words)

    return lockloss, words, offset

if __name__ == '__main__':
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option('--nEvents', dest='nEvents', type='int', default = 1000, help="Set number of events to save to tmp data file")
    parser.add_option('--mode', dest='mode', type='string', default = 'tdc', help="Set offset finder type")
    parser.add_option('--scrambled', dest='scrambled', default = True, help="Descramble the data or not")
    options, args = parser.parse_args()

    nEvents = options.nEvents
    mode = options.mode
    scrambled = options.scrambled

    data = []
    while( len(data) < nEvents):
        lockloss, words, offset = readout(1, mode, scrambled)

        if not lockloss:
            data += words[1:-1] #First and Last word is always half empty
        print("nEvents = {}, offset = {}".format(len(data), offset))

    data = data[:nEvents]
    fileData = open("etroc_readout.dat","w")
    for d in data:
        #print(get_binary_string(int(d,16),32))
        fileData.write("{}\n".format(d))
    fileData.close()
