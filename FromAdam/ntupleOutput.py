#!/bin/env python
from __future__ import print_function
import sys
import numpy as np
import ROOT as rt

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect usage!")
        print("usage: ntupleOutput.py inFileName")
        sys.exit(1)
    
    # input file
    nameFile = sys.argv[1]
    print("File name: " , nameFile+".rawf")
    fileIn = open(nameFile+".rawf","r")

    header_pattern = "101010101010" # for readout test pattern generator
    #header_pattern = "10" #for normal readout

    lines = fileIn.readlines()
    nFrames=len(lines)-1
    nBytes=int(lines[0][-4:-2])
    nWords=int(nBytes/4)
    print("nFrames =  %d; nBytes = %d"%(nFrames, nBytes))
    Counter = np.zeros((nFrames, nWords), dtype=int) 
    TOT = np.zeros((nFrames, nWords), dtype=int)
    TOA = np.zeros((nFrames, nWords), dtype=int)
    Cal = np.zeros((nFrames, nWords), dtype=int)
    hitFlag = np.zeros((nFrames, nWords), dtype=int)
    words_binary = []


    # convert word to 32 bit binary
    for iLine in range(nFrames):
        line = lines[iLine+1].split()
        words_line_binary = []
        for iW in range(nWords):
            word = "0x"
            #for idx in range(4):
            for idx in [1,0,3,2]: # swap bytes
                word += str.format('{:02x}', int(line[iW*4 + idx + 1], 16))
            word_binary = str.format('{:032b}', int(word, 16))
            if iW == 1:
                print(word_binary)
            words_line_binary.append(word_binary)
        words_binary.append(words_line_binary)
   
    # find header, and shift to make each line begin with header_pattern
    for iW in range(nWords):
        for idx_check in range(32):
            isHead=True
            for iLine in range(len(words_binary)-1): 
                if words_binary[iLine][iW][0:len(header_pattern)] != header_pattern:
                    isHead=False
                    break
            if isHead: #header is found at the  beginning
                print("header_pattern found at "+str(idx_check))
                if(idx_check > 0): #header is in the middle, the last line is invalid beacase of missing bits not readout
                    words_binary[len(words_binary)-1][iW] = header_pattern+str.format('{:0'+str(32-len(header_pattern))+'b}',0)
                break
            #header is not found at the beginning, left shit one for each line
            for iLine in range(len(words_binary)-1): 
                words_binary[iLine][iW] = words_binary[iLine][iW][1:]+words_binary[iLine+1][iW][0]
            words_binary[len(words_binary)-1][iW] = words_binary[len(words_binary)-1][iW][1:]+"0"

    print("after left shift (now each line begins with header_pattern):")
    # extract Counter, TOT, TOA, etc from each word
    for iLine in range(len(words_binary)):
        for iW in range(nWords):
            word_binary = words_binary[iLine][iW]
            ## check header
            if word_binary[0:len(header_pattern)] != header_pattern: # header not found in this line, set to zero...
                word_binary = str.format('{:032b}',0)
            if iW == 1:
                print(word_binary)
            Counter[iLine][iW] = int(word_binary[16:], 2)
            TOT[iLine][iW] = int(word_binary[2:11], 2)
            TOA[iLine][iW] = int(word_binary[11:21], 2)
            Cal[iLine][iW] = int(word_binary[21:31], 2)
            hitFlag[iLine][iW] = int(word_binary[31], 2)
 
    for x in range(nWords):
         Counter[:,x]=Counter[:,x]-Counter[0,x]

    print(Counter)
    print("Counter values:")
    print(Counter[:-1,1])
    #print(TOT[:,1])
    #print(TOA[:,1])
    #print(Cal[:,1])
    #print(hitFlag[:,1])
	
    # save variables into ROOT tree
    rt.gROOT.ProcessLine("struct MyStructTOT{int TOT["+str(nWords)+"];};")
    rt.gROOT.ProcessLine("struct MyStructTOA{int TOA["+str(nWords)+"];};")
    rt.gROOT.ProcessLine("struct MyStructCal{int Cal["+str(nWords)+"];};")
    rt.gROOT.ProcessLine("struct MyStructhitFlag{int hitFlag["+str(nWords)+"];};")
    rt.gROOT.ProcessLine("struct MyStructCounter{int Counter["+str(nWords)+"];};")
    rt.gROOT.ProcessLine("struct MyStructnFrame{int nFrame;};")

    from ROOT import MyStructnFrame
    from ROOT import MyStructTOT
    from ROOT import MyStructTOA
    from ROOT import MyStructCal
    from ROOT import MyStructhitFlag
    from ROOT import MyStructCounter

    my_s_TOT =  MyStructTOT()
    my_s_TOA =  MyStructTOA()
    my_s_Cal =  MyStructCal()
    my_s_hitFlag =  MyStructhitFlag()
    my_s_Counter= MyStructCounter()
    my_s_nFrame =  MyStructnFrame() 

    fileOut = rt.TFile(nameFile+".root", "RECREATE")
    tree = rt.TTree("tree", "ntuple from ETROC output")
    tree.Branch("TOT", rt.addressof(my_s_TOT, "TOT"), "TOT["+str(nWords)+"]/I")
    tree.Branch("TOA", rt.addressof(my_s_TOA, "TOA"), "TOA["+str(nWords)+"]/I")
    tree.Branch("Cal", rt.addressof(my_s_Cal, "Cal"), "Cal["+str(nWords)+"]/I")
    tree.Branch("hitFlag", rt.addressof(my_s_hitFlag,"hitFlag"), "hitFlag["+str(nWords)+"]/I")
    tree.Branch("Counter", rt.addressof(my_s_Counter, "Counter"), "Counter["+str(nWords)+"]/I")
    tree.Branch("nFrame", rt.addressof(my_s_nFrame, "nFrame"), "nFrame/I")

    for iFr in range(nFrames):
        for iW in range(nWords):
            my_s_TOT.TOT[iW] =int(TOT[iFr][iW])
            my_s_TOA.TOA[iW] = int(TOA[iFr][iW])
            my_s_Cal.Cal[iW] = int(Cal[iFr][iW])
            my_s_hitFlag.hitFlag[iW] = int(hitFlag[iFr][iW])
            my_s_Counter.Counter[iW] = int(Counter[iFr][iW])
            my_s_nFrame.nFrame = iFr
        tree.Fill()
    tree.Write()
   


