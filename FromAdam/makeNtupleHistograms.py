import ROOT
import sys
import os

def main() :
    if len(sys.argv) < 2:
        print("Incorrect usage!")
        sys.exit(1)
    
    #input file
    nameFile = sys.argv[1]
    fileIn=nameFile+".root"
    outputDir= 'ntuplePlots'
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
    histogramDict["TOA"]=ROOT.TH1D("TOAHist","TOAHist",100,0,100)
    histogramDict["TOT"]=ROOT.TH1D("TOTHist","TOTHist",100,0,100)
    histogramDict["Cal"]=ROOT.TH1D("CalHist","CalHist",100,0,100)
    histogramDict["hitFlag"]=ROOT.TH1D("hitFlagHist","hitFlagHist",100,0,100)
    
    outputFile  = ROOT.TFile(outputDir+"/"+nameFile+"Histograms"+".root", "RECREATE" )
       
    for entry in inputTree:
        print(float(entry.thresholdDAC))
        
    for key in histogramDict.keys():
        histogramDict[key].Write()

    outputFile.Close()
    inputFile.Close()
 
if __name__ == '__main__':
    main()
