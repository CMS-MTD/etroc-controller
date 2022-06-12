#!/bin/env python3
import ROOT
import os
import math
import optparse

def makeProfileHisto(d, name):
    meanName = "Mean_"+name
    d[meanName] = d[name].ProfileX(meanName)
    d[meanName].BuildOptions(0,0,'s')

    stdName = "STD_"+name
    d[stdName] = ROOT.TH1D(stdName,stdName,d[meanName].GetNbinsX(), d[meanName].GetBinLowEdge(1), d[meanName].GetBinLowEdge(d[meanName].GetNbinsX()) + d[meanName].GetBinWidth(d[meanName].GetNbinsX()))
    for i in range(d[meanName].GetNbinsX() + 1):
        val = d[meanName].GetBinError(i)
        d[stdName].SetBinContent(i, val)
        d[stdName].SetBinError(i, 0.0)

def main() :
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option('--infile', dest='infile', default = "data.root", help="Set output root file name")
    options, args = parser.parse_args()

    fileIn = options.infile
    nameFile = fileIn.strip(".root")
    outputDir = 'ntuplePlots'
    print("infile: {}".format(fileIn))
    if not os.path.exists(outputDir):
        print("Output directory does not exist, so making output directory", outputDir)
        os.makedirs(outputDir)

    #Define variables needed for the analyzer here.
    ROOT.TH1.SetDefaultSumw2()        
           
    #will make changes here
    inputFile= ROOT.TFile.Open(fileIn)
    inputTree= inputFile.Get("tree")

    #Create a dictionary to hold onto all the histograms that will be used to write to an output file
    outFileName = outputDir+"/"+nameFile+"Histograms"+".root"
    print("outfile: {}".format(outFileName))
    outputFile  = ROOT.TFile(outFileName, "RECREATE" )
    nBins10Bits = 1024
    nBins09Bits = 512
    thrNbins = 300 #30
    thrLowBin = 350 #360
    thrHighBin = 650 #390
    T3 = 3.125 #ns
    CALMean = 173
    pDAC = 0
    tDAC = 410

    cuts = [("","cut1"),("_hit","cut2"),("_hit_dac{}".format(tDAC),"cut3"),("_hit_phase{}".format(pDAC),"cut4"),("_hit_dac{}_phase{}".format(tDAC,pDAC),"cut5")]

    histogramDict = {}       
    for suffix, _ in cuts:
        histogramDict["TOA"+suffix]=ROOT.TH1D("TOAHist"+suffix,"TOAHist"+suffix+"; TOA; Events",nBins10Bits,0,nBins10Bits)
        histogramDict["TOT"+suffix]=ROOT.TH1D("TOTHist"+suffix,"TOTHist"+suffix+"; TOT; Events", nBins09Bits,0,nBins09Bits)
        histogramDict["TOTvsTOA"+suffix]=ROOT.TH2D("TOTvsTOAHist"+suffix,"TOTvsTOAHist"+suffix+"; TOT; TOA", nBins09Bits,0,nBins09Bits, nBins10Bits,0,nBins10Bits)
        histogramDict["TOAvsthresholdDAC"+suffix]=ROOT.TH2D("TOAvsthresholdDACHist"+suffix,"TOAvsthresholdDACHist"+suffix+"; thresholdDAC; TOA", thrNbins,thrLowBin,thrHighBin, nBins10Bits,0,nBins10Bits)
        histogramDict["TOTvsthresholdDAC"+suffix]=ROOT.TH2D("TOTvsthresholdDACHist"+suffix,"TOTvsthresholdDACHist"+suffix+"; thresholdDAC; TOT", thrNbins,thrLowBin,thrHighBin, nBins09Bits,0,nBins09Bits)
        histogramDict["CAL"+suffix]=ROOT.TH1D("CALHist"+suffix,"CALHist"+suffix+"; CAL; Events",80,120.0,200.0)
        histogramDict["TOAvsCAL"+suffix]=ROOT.TH2D("TOAvsCALHist"+suffix,"TOAvsCALHist"+suffix+"; TOA; CAL", nBins10Bits,0,nBins10Bits, 80,120.0,200.0)
        histogramDict["TOATimevsCAL"+suffix]=ROOT.TH2D("TOATimevsCALHist"+suffix,"TOATimevsCALHist"+suffix+"; TOA (ns); CAL", 1250,0,25, 80,120.0,200.0)
        histogramDict["thresholdDAC"+suffix]=ROOT.TH1D("thresholdDAC"+suffix,"thresholdDAC"+suffix+"; thresholdDAC; Events",thrNbins,thrLowBin,thrHighBin)
        histogramDict["hitFlag"+suffix]=ROOT.TH1D("hitFlagHist"+suffix,"hitFlagHist"+suffix+"; hitFlag; Events",2,-0.5,1.5)
        histogramDict["TOATime"+suffix]=ROOT.TH1D("TOATimeHist"+suffix,"TOATimeHist"+suffix+"; TOA (ns); Events",1250,0,25)
        histogramDict["TOTTime"+suffix]=ROOT.TH1D("TOTTimeHist"+suffix,"TOTTimeHist"+suffix+"; TOT (ns); Events",1250,0,25)
        histogramDict["phaseDAC"+suffix]=ROOT.TH1D("PhaseHist"+suffix,"PhaseHist"+suffix+"; Phase; Events",250,0.0,250.0)
        histogramDict["TOATimevsphaseDAC"+suffix]=ROOT.TH2D("TOATimevsPhaseHist"+suffix,"TOATimevsPhaseHist"+suffix+"; Phase; TOA (ns)", 250,0.0,250.0, 1250,0,25)
        histogramDict["CALTimevsphaseDAC"+suffix]=ROOT.TH2D("CALvsPhaseHist"+suffix,"CALvsPhaseHist"+suffix+"; Phase; CAL", 250,0.0,250.0, 80,120.0,200.0)
        histogramDict["TOATimevsthresholdDAC"+suffix]=ROOT.TH2D("TOATimevsthresholdDACHist"+suffix,"TOATimevsthresholdDACHist"+suffix+"; thresholdDAC; TOA (ns)", thrNbins,thrLowBin,thrHighBin, 1250,0,25)

    for entry in inputTree:
        TOA = int(entry.TOA)
        TOT = int(entry.TOT)
        CAL = int(entry.CAL)
        thresholdDAC = int(entry.thresholdDAC)
        hitFlag = int(entry.hitFlag)
        phase = int(entry.phaseDAC)
        #tdcBin = T3/CAL if CAL > 0.0 else 0.0
        tdcBin = T3/CALMean
        TOATime = tdcBin*TOA
        TOTTime = tdcBin*(2*TOT - math.floor(TOT/32.0))
        cutVal = {"cut1":True, "cut2":hitFlag and CAL != 0.0, "cut3":hitFlag and CAL != 0.0 and thresholdDAC == tDAC,
                  "cut4":hitFlag and CAL != 0.0 and phase == pDAC,"cut5":hitFlag and CAL != 0.0 and thresholdDAC == tDAC and phase == pDAC}

        for suffix, cut in cuts:
            if cutVal[cut] and CAL != 0.0:
                histogramDict["TOA"+suffix].Fill(TOA)
                histogramDict["TOT"+suffix].Fill(TOT)
                histogramDict["TOAvsthresholdDAC"+suffix].Fill(thresholdDAC, TOA)
                histogramDict["TOTvsthresholdDAC"+suffix].Fill(thresholdDAC, TOT)
                histogramDict["TOTvsTOA"+suffix].Fill(TOT, TOA)
                histogramDict["CAL"+suffix].Fill(CAL)
                histogramDict["TOAvsCAL"+suffix].Fill(TOA, CAL)
                histogramDict["TOATimevsCAL"+suffix].Fill(TOATime, CAL)
                histogramDict["thresholdDAC"+suffix].Fill(thresholdDAC)
                histogramDict["hitFlag"+suffix].Fill(hitFlag)
                histogramDict["TOATime"+suffix].Fill(TOATime)
                histogramDict["TOTTime"+suffix].Fill(TOTTime)                
                histogramDict["phaseDAC"+suffix].Fill(phase)
                histogramDict["TOATimevsphaseDAC"+suffix].Fill(phase,TOATime)
                histogramDict["CALTimevsphaseDAC"+suffix].Fill(phase, CAL)
                histogramDict["TOATimevsthresholdDAC"+suffix].Fill(thresholdDAC,TOATime)


    for suffix, _ in cuts:
        makeProfileHisto(histogramDict, "TOAvsthresholdDAC"+suffix)
        makeProfileHisto(histogramDict, "TOTvsthresholdDAC"+suffix)
        makeProfileHisto(histogramDict, "TOATimevsphaseDAC"+suffix)
        makeProfileHisto(histogramDict, "TOATimevsthresholdDAC"+suffix)

    histogramDict = dict(sorted(histogramDict.items(), key=lambda x:x[0].lower()))        
    for key in histogramDict.keys():
        histogramDict[key].Write()

    outputFile.Close()
    inputFile.Close()
 
if __name__ == '__main__':
    main()
