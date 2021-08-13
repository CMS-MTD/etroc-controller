#!/bin/env python3
import ROOT
import os
import math

def makeProfileHisto(d, name):
    meanName = name+"Mean"
    d[meanName] = d[name].ProfileX(meanName)
    d[meanName].BuildOptions(0,0,'s')

    stdName = name+"STD"
    d[stdName] = ROOT.TH1D(stdName,stdName,d[meanName].GetNbinsX(), d[meanName].GetBinLowEdge(1), d[meanName].GetBinLowEdge(d[meanName].GetNbinsX()) + d[meanName].GetBinWidth(d[meanName].GetNbinsX()))
    for i in range(d[meanName].GetNbinsX() + 1):
        val = d[meanName].GetBinError(i)
        d[stdName].SetBinContent(i, val)
        d[stdName].SetBinError(i, 0.0)

def main() :
    #nameFile = "data_Qinj_FF_working"
    #nameFile = "data_Qinj_CF_working"
    #nameFile = "data_Qinj_87_working"
    nameFile = "data_Qinj_37_working"
    #nameFile = "data_noQInj"
    #nameFile = "data" 
    fileIn = nameFile+".root"
    outputDir = 'ntuplePlots'
    print(fileIn)
    if not os.path.exists(outputDir):
        print("Output directory does not exist, so making output directory", outputDir)
        os.makedirs(outputDir)

    #Define variables needed for the analyzer here.
    ROOT.TH1.SetDefaultSumw2()        
           
    #will make changes here
    inputFile= ROOT.TFile.Open(fileIn)
    inputTree= inputFile.Get("tree")

    #Create a dictionary to hold onto all the histograms that will be used to write to an output file
    outputFile  = ROOT.TFile(outputDir+"/"+nameFile+"Histograms"+".root", "RECREATE" )
    nBins10Bits = 1024
    nBins09Bits = 512
    thrNbins = 200 #30
    thrLowBin = 350 #360
    thrHighBin = 550 #390
    T3 = 3.125 #ns

    cuts = [("","cut1"),("_hit","cut2"),("_hit_dac375","cut3")]

    histogramDict= {}       
    for suffix, _ in cuts:
        histogramDict["TOA"+suffix]=ROOT.TH1D("TOAHist"+suffix,"TOAHist"+suffix+"; TOA; Events",nBins10Bits,0,nBins10Bits)
        histogramDict["TOT"+suffix]=ROOT.TH1D("TOTHist"+suffix,"TOTHist"+suffix+"; TOT; Events", nBins09Bits,0,nBins09Bits)
        histogramDict["TOTvsTOA"+suffix]=ROOT.TH2D("TOTvsTOAHist"+suffix,"TOTvsTOAHist"+suffix+"; TOT; TOA", nBins09Bits,0,nBins09Bits, nBins10Bits,0,nBins10Bits)
        histogramDict["TOAvsthresholdDAC"+suffix]=ROOT.TH2D("TOAvsthresholdDACHist"+suffix,"TOAvsthresholdDACHist"+suffix+"; thresholdDAC; TOA", thrNbins,thrLowBin,thrHighBin, nBins10Bits,0,nBins10Bits)
        histogramDict["TOTvsthresholdDAC"+suffix]=ROOT.TH2D("TOTvsthresholdDACHist"+suffix,"TOTvsthresholdDACHist"+suffix+"; thresholdDAC; TOT", thrNbins,thrLowBin,thrHighBin, nBins09Bits,0,nBins09Bits)
        histogramDict["CAL"+suffix]=ROOT.TH1D("CALHist"+suffix,"CALHist"+suffix+"; CAL; Events",60,120.0,180.0)
        histogramDict["thresholdDAC"+suffix]=ROOT.TH1D("thresholdDAC"+suffix,"thresholdDAC"+suffix+"; thresholdDAC; Events",thrNbins,thrLowBin,thrHighBin)
        histogramDict["hitFlag"+suffix]=ROOT.TH1D("hitFlagHist"+suffix,"hitFlagHist"+suffix+"; hitFlag; Events",2,-0.5,1.5)
        histogramDict["TOATime"+suffix]=ROOT.TH1D("TOATimeHist"+suffix,"TOATimeHist"+suffix+"; TOA (ns); Events",250,0,25)
        histogramDict["TOTTime"+suffix]=ROOT.TH1D("TOTTimeHist"+suffix,"TOTTimeHist"+suffix+"; TOT (ns); Events",250,0,25)

    for entry in inputTree:
        TOA = int(entry.TOA)
        TOT = int(entry.TOT)
        CAL = int(entry.CAL)
        thresholdDAC = int(entry.thresholdDAC)
        hitFlag = int(entry.hitFlag)
        tdcBin = T3/CAL if CAL > 0.0 else 0.0
        TOATime = tdcBin*TOA
        TOTTime = tdcBin*(2*TOT - math.floor(TOT/32.0))
        cutVal = {"cut1":True,"cut2":hitFlag,"cut3":hitFlag and thresholdDAC == 375}

        for suffix, cut in cuts:
            if cutVal[cut] and CAL != 0.0:
                histogramDict["TOA"+suffix].Fill(TOA)
                histogramDict["TOT"+suffix].Fill(TOT)
                histogramDict["TOAvsthresholdDAC"+suffix].Fill(thresholdDAC, TOA)
                histogramDict["TOTvsthresholdDAC"+suffix].Fill(thresholdDAC, TOT)
                histogramDict["TOTvsTOA"+suffix].Fill(TOT, TOA)
                histogramDict["CAL"+suffix].Fill(CAL)
                histogramDict["thresholdDAC"+suffix].Fill(thresholdDAC)
                histogramDict["hitFlag"+suffix].Fill(hitFlag)
                histogramDict["TOATime"+suffix].Fill(TOATime)
                histogramDict["TOTTime"+suffix].Fill(TOTTime)                

    for suffix, _ in cuts:
        makeProfileHisto(histogramDict, "TOAvsthresholdDAC"+suffix)
        makeProfileHisto(histogramDict, "TOTvsthresholdDAC"+suffix)
        
    for key in histogramDict.keys():
        histogramDict[key].Write()

    outputFile.Close()
    inputFile.Close()
 
if __name__ == '__main__':
    main()
