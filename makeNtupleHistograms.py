#!/bin/env python3
import ROOT
import os

def main() :
    #nameFile = "data_Qinj_FF"
    #nameFile = "data_Qinj_CF"
    #nameFile = "data_Qinj_87"
    #nameFile = "data_Qinj_80"
    #nameFile = "data_Qinj_37"
    nameFile = "data" 
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
    histogramDict= {}       
    histogramDict["TOA"]=ROOT.TH1D("TOAHist","TOAHist",1024,0,1024)
    histogramDict["TOT"]=ROOT.TH1D("TOTHist","TOTHist", 512,0,512)
    histogramDict["TOTvsTOA"]=ROOT.TH2D("TOTvsTOAHist","TOTvsTOAHist", 512,0,512, 1024,0,1024)
    histogramDict["CAL"]=ROOT.TH1D("CALHist","CALHist",1024,0,1024)
    histogramDict["thresholdDAC"]=ROOT.TH1D("thresholdDAC","thresholdDAC",1024,0,1024)
    histogramDict["hitFlag"]=ROOT.TH1D("hitFlagHist","hitFlagHist",10,0,10)
    
    outputFile  = ROOT.TFile(outputDir+"/"+nameFile+"Histograms"+".root", "RECREATE" )
       
    for entry in inputTree:
        TOA = int(entry.TOA)
        TOT = int(entry.TOT)
        CAL = int(entry.CAL)
        thresholdDAC = int(entry.thresholdDAC)
        hitFlag = int(entry.hitFlag)

        if hitFlag:
            histogramDict["TOA"].Fill(TOA)
            histogramDict["TOT"].Fill(TOT)
            histogramDict["TOTvsTOA"].Fill(TOT, TOA)
            histogramDict["CAL"].Fill(CAL)
            histogramDict["thresholdDAC"].Fill(thresholdDAC)
        
    for key in histogramDict.keys():
        histogramDict[key].Write()

    outputFile.Close()
    inputFile.Close()
 
if __name__ == '__main__':
    main()
