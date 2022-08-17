#!/bin/env python3
from etroc_i2c import ETROC_I2C
import binaryFunctions as bf
import os
import ROOT
from array import array
import optparse
import time

def getPhaseSettings():
    #Gets phase settings; each bit is 100ps
    return list(p for p in range(0x00,0xFA,10))
    #return [0x00, 0x3F, 0x7F, 0xBF]

def getAllQinj():
    #Gets all possible Qinj values
    allQinj = {}
    b = 0b111
    for idx, a in enumerate(range(0b0, 0b11111 + 0b1)):
        c = bf.add_binary(a, b, 3)
        allQinj[c] = dict(binary=bf.get_binary_string(c), reg1=c, fC=idx)
    return allQinj

def getPixNum(n):
    #Figure out pixel number
    nEventsPerPixel = 256
    nEventsPerPacket = 4096

    pixNum = 999
    if n == 1:
        pixNum = 100
    elif n == nEventsPerPacket+2:
        pixNum = 101
    elif n<1 or  nEventsPerPacket+2<n:
        pixNum = 99
    else:
        pixNum = int((n-2) / nEventsPerPixel)

    pMap = [15, 11, 7, 3, 14, 10, 6, 2, 13, 9, 5, 1, 12, 8, 4, 0]
    pixNum = pMap[pixNum] if pixNum < 20 else pixNum
    return pixNum

if __name__ == '__main__':
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option('--Qinj', dest='Qinj', type='int', default = 0xFF, help="Set Qinj register value")
    parser.add_option('--phase', dest='phase', type='int', default = 0x00, help="Set phase register value")
    parser.add_option('--outfile', dest='outfile', default = "data.root", help="Set output root file name")
    parser.add_option('--nEvents', dest='nEvents', type='int', default = 32000, help="Set number of events to take per setting")
    options, args = parser.parse_args()

    allQinj = getAllQinj()
    Qinj = options.Qinj
    QinjValue = allQinj[Qinj]['fC']
    fixedPhase = options.phase

    outfile = options.outfile
    nEvents = options.nEvents
    doPhaseScan = True
    print("Qinj value: {}".format(hex(Qinj)))
    print("Outfile name: {}".format(outfile))
    print("nEvents: {}".format(nEvents))

    #################################################
    # Create instance of ETROC I2C class to communicate with the ETROC via the CERN dongle
    #################################################
    i2c = ETROC_I2C(dongle=2, verbose=None)
    i2c.setupETROC()
    REGA = i2c.r.ETROC_REGA_ADDRESS
    REGB = i2c.r.ETROC_REGB_ADDRESS
    i2c.write_default()

    #################################################
    # Loop over all thresholds and collect data
    #################################################
    allPhase = getPhaseSettings()
    dataTuple = []
    for idPhase, phase in enumerate(allPhase):
        if not doPhaseScan and idPhase !=0: break
        #if phase != 0x64: continue
        #if phase != 150: continue
        if phase != 0: continue 

        for idx, _  in enumerate(bf.getAllThresholdsType0(None, None)):
            if idx < 200 or idx > 800: continue
            #if idx < 100 or idx > 800: continue
            #if idx != 500: continue

            #--------------------------------------------------
            # Define thresholds for all pixels
            #--------------------------------------------------
            for i, p in bf.pixels.items():
                p.setActiveThresholds(idx)
                bf.regThresholdAddresses[p.reg1AddressTh] = bf.update_binary_num(bf.regThresholdAddresses[p.reg1AddressTh], p.thresholdReg1, p.getAllThresholds[0]["mask1"])
                bf.regThresholdAddresses[p.reg2AddressTh] = bf.update_binary_num(bf.regThresholdAddresses[p.reg2AddressTh], p.thresholdReg2, p.getAllThresholds[0]["mask2"])

            #--------------------------------------------------
            # Define the i2c commands for this setting and run them
            #--------------------------------------------------
            commands=[
                ('w', i2c.r.ETROC_REGB_ADDRESS, 0x00, 0x1C ), # default (1C)
                ('w', i2c.r.ETROC_REGB_ADDRESS, 0x06, 0x40 ), # disable (40)/enable (41) scrambling
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, Qinj ), # default (37), Q injected amplitude
                ('w', i2c.r.ETROC_REGB_ADDRESS, 0x04, phase), # default (00), Phase setting
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x04, 0x00 ), # default 0x11, Set Discriminator out
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x05, 0xFF ), # default (01), Set Q injected pixel
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x06, 0xFF ), # default (00), Set Q injected pixel
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x07, 0x40 ), # default (01), Set SRO or DMRO mode
            ]

            for regAddress, threshold in bf.regThresholdAddresses.items():
                commands.append(('w', i2c.r.ETROC_REGA_ADDRESS, regAddress, threshold))

            i2c.run(commands)            
            print("Setting thresholds to {}, Setting phase to {} {}".format(idx, hex(phase), phase))
            
            #--------------------------------------------------
            # Take data for this ETROC setting
            #--------------------------------------------------
            nRead = 10
            for rIndex in range(nRead):
                #os.system('./run_read_buffer.sh 10000 constant True')
                #os.system('./run_read_buffer.sh {} tdc True'.format(nEvents))
                os.system('./run_ETROC_readout_2links.sh')
                #with open('/home/daq/Alexey_ETL/SCA_work_scripts/outETROC/Chris_CCLink1_RxRAM_conv.txt') as f:
                with open('/home/daq/Alexey_ETL/SCA_work_scripts/outETROC/Chris_CCLink1_DBGRAM_conv.txt') as f:
                    lines = f.read().splitlines()
            
                    nHits = 0
                    for l in lines:
                        l = l.split()[1][:-1]
                        try:
                            word = int(l, 16)
                        except:
                            pass
                            print("This word failed:", l)
                        nHits += word % 2
            
                    dataTuple.append((idx, lines, nHits, phase, QinjValue))
                    print("Finished reading data")

    
    #################################################
    # Save recored data to nTuples
    #################################################
    root_file = ROOT.TFile(outfile, "RECREATE")
    tree = ROOT.TTree("tree","tree")
    thresholdDAC_ = array('I',[0])
    nHits_ = array('I',[0])
    wordNum_ = array('I',[0])
    eventNum_ = array('I',[0])
    word_ = array('I',[0])
    HEAD_ = array('I',[0])
    TOT_ = array('I',[0])
    TOA_ = array('I',[0])
    CAL_ = array('I',[0])
    hitFlag_ = array('I',[0])
    phaseDAC_ = array('I',[0])
    pixNum_ = array('I',[0])
    QinjValue_ = array('I',[0])
    tree.Branch('thresholdDAC', thresholdDAC_, 'thresholdDAC/I')
    tree.Branch('nHits', nHits_, 'nHits/I')
    tree.Branch('wordNum', wordNum_, 'wordNum/I')
    tree.Branch('eventNum', eventNum_, 'eventNum/I')
    tree.Branch('word', word_, 'word/I')
    tree.Branch('HEAD', HEAD_, 'HEAD/I')
    tree.Branch('TOT', TOT_, 'TOT/I')
    tree.Branch('TOA', TOA_, 'TOA/I')
    tree.Branch('CAL', CAL_, 'CAL/I')
    tree.Branch('hitFlag', hitFlag_, 'hitFlag/I')
    tree.Branch('phaseDAC', phaseDAC_, 'phaseDAC/I')
    tree.Branch('pixNum', pixNum_, 'pixNum/I')
    tree.Branch('QinjValue', QinjValue_, 'QinjValue/I')
    
    for thresholdDAC, lines, nHits, phase, QinjValue in dataTuple:
        thresholdDAC_[0] = thresholdDAC
        nHits_[0] = nHits
        phaseDAC_[0] = phase
        QinjValue_[0] = QinjValue
        
        eventNum = 0
        eventTracker = 9999
        for ll in lines:
            try:
                n = int(ll.split()[0][:-1])
                if eventTracker > n: eventNum += 1
                eventTracker = n

                l = ll.split()[1][:-1]
                word = format(int(l,16), "#034b")
                pixNum = getPixNum(n)
                wordNum_[0] = n
                eventNum_[0] = eventNum
                word_[0] = int(l,16)
                HEAD_[0] = int(word[2:4],2)
                TOT_[0] = int(word[4:13],2)
                TOA_[0] = int(word[13:23],2)
                CAL_[0] = int(word[23:33],2)
                hitFlag_[0] = int(word[33],2)
                pixNum_[0] = pixNum
                tree.Fill()
                #print("This word passed:", l, word, thresholdDAC, len(l), len(str(word)))
                #print("This word passed:", word)
            except:
                pass
                print("This word failed:", l, word, thresholdDAC, len(l), len(str(word)))

    
    tree.Write()
    root_file.Close()
