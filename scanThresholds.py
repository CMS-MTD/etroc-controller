#!/bin/env python3
from etroc_i2c import ETROC_I2C
from binaryFunctions import add_binary, get_binary_string
import os
import ROOT
from array import array
import optparse
import time

def getPhaseSettings():
    #Gets phase settings; each bit is 100ps
    #return list(p for p in range(0x00,0xFA,10))
    return [0x00, 0x3F, 0x7F, 0xBF]

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
    for regB in range(0b00, 0b11 + 0b1):
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
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option('--Qinj', dest='Qinj', type='int', default = 0xFF, help="Set Qinj register value")
    parser.add_option('--outfile', dest='outfile', default = "data.root", help="Set output root file name")
    parser.add_option('--nEvents', dest='nEvents', type='int', default = 1000, help="Set number of events to take per setting")
    options, args = parser.parse_args()

    Qinj = options.Qinj
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
    allQinj = getAllQinj()
    allPhase = getPhaseSettings()

    dataTuple = []
    allThresholds = getAllThresholds()    
    #allThresholds = getAllThresholdsPixel15()
    for idPhase, phase in enumerate(allPhase):
        if not doPhaseScan and idPhase !=0: break
        if phase != 0x3F: continue

        for idx, threshold in reversed(list(enumerate(allThresholds))):
            #if idx < 360 or idx > 400: continue
            if idx < 605 or idx > 660: continue
            #if idx != 500: continue
        
            #Reading out Pixel 1
            commands=[
                ('w', i2c.r.ETROC_REGB_ADDRESS, 0x00, 0x1C), # default (1C)
                ('w', i2c.r.ETROC_REGB_ADDRESS, 0x06, 0x41), # disable (40)/enable (41) scrambling
                #('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0x37), # default (37), Q injected amplitude
                #('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0x87), # default (37), Q injected amplitude
                #('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0xCF), # default (37), Q injected amplitude
                #('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, 0xFF), # default (37), Q injected amplitude
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, Qinj), # default (37), Q injected amplitude
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x0A, threshold['regA']), # default (00), signal threshold pixel 1
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x0B, threshold['regB']), # default (02), signal threshold (only first two bits belong to pixel 1 the rest belong to pixel 2)
                ('w', i2c.r.ETROC_REGB_ADDRESS, 0x04, phase), # default (00), Phase setting
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x05, 0x01), ### 01 on, 00 off. disables Q INJ (I2C A REG 05)
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x06, 0x00),  ### 00 regardless. disables Q INJ (I2C A REG 06)
                ('w', i2c.r.ETROC_REGA_ADDRESS, 0x04, 0x00), # default 0x11 

                ('r', i2c.r.ETROC_REGB_ADDRESS, 0x06), # disable (40)/enable (41) scrambling
            ]

            ##Reading out Pixel 15
            #commands=[
            #    ('w', i2c.r.ETROC_REGB_ADDRESS, 0x00, 0x1C), # default (1C)
            #    ('w', i2c.r.ETROC_REGB_ADDRESS, 0x06, 0x41), # disable (40)/enable (41) scrambling
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x01, Qinj), # default (37), Q injected amplitude
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x05, 0x00), # default (01)
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x06, 0x80), # default (00)
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x07, 0x38), # default (01)
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x1C, threshold['regA']), # default (20), signal threshold pixel 1
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x1D, threshold['regB']), # default (80), signal threshold (only first two bits belong to pixel 1 the rest belong to pixel 2)
            #    ('w', i2c.r.ETROC_REGB_ADDRESS, 0x04, 0x00), # default (00), Phase setting
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x05, 0x01), ### 01 on, 00 off. disables Q INJ (I2C A REG 05)
            #    ('w', i2c.r.ETROC_REGA_ADDRESS, 0x06, 0x00),  ### 00 regardless. disables Q INJ (I2C A REG 06)
            #]

            i2c.run(commands)
            print("Setting threshold to {} {} {} {}, Setting phase to {}".format(threshold['binary'], hex(threshold['regB']), hex(threshold['regA']), idx, hex(phase)))

            #os.system('./run_read_buffer.sh 10000 constant True')
            os.system('./run_read_buffer.sh {} tdc True'.format(nEvents))
            with open('etl-kcu105-ipbus/etroc_readout.dat') as f:
                lines = f.read().splitlines()
    
                nHits = 0
                for l in lines:
                    word = int(l, 16)
                    nHits += word % 2
    
                dataTuple.append((threshold['binary'], idx, lines, nHits, phase))
    
    #################################################
    # Save recored data to nTuples
    #################################################
    root_file = ROOT.TFile(outfile, "RECREATE")
    tree = ROOT.TTree("tree","tree")
    thresholdDAC_ = array('I',[0])
    nHits_ = array('I',[0])
    word_ = array('I',[0])
    TOT_ = array('I',[0])
    TOA_ = array('I',[0])
    CAL_ = array('I',[0])
    hitFlag_ = array('I',[0])
    phaseDAC_ = array('I',[0])
    tree.Branch('thresholdDAC', thresholdDAC_, 'thresholdDAC/I')
    tree.Branch('nHits', nHits_, 'nHits/I')
    tree.Branch('word', word_, 'word/I')
    tree.Branch('TOT', TOT_, 'TOT/I')
    tree.Branch('TOA', TOA_, 'TOA/I')
    tree.Branch('CAL', CAL_, 'CAL/I')
    tree.Branch('hitFlag', hitFlag_, 'hitFlag/I')
    tree.Branch('phaseDAC', phaseDAC_, 'phaseDAC/I')
    
    for thresholdBinary, thresholdDAC, lines, nHits, phase in dataTuple:
        thresholdDAC_[0] = thresholdDAC
        nHits_[0] = nHits
        phaseDAC_[0] = phase
        for l in lines:
            word = bin(int(l,16))
            word_[0] = int(l,16)
            TOT_[0] = int(word[4:13],2)
            TOA_[0] = int(word[13:23],2)
            CAL_[0] = int(word[23:33],2)
            hitFlag_[0] = int(word[33],2)
            #print(word, word_[0], TOT_[0], TOA_[0], CAL_[0], hitFlag_[0])        
            tree.Fill()
    
    tree.Write()
    root_file.Close()
