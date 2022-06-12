#!/bin/env python3
import ROOT
import os
ROOT.gROOT.SetBatch(True)

def main() :
    f1 = ROOT.TFile.Open("ntuplePlots/data_Qinj_37_pix1_powerboard2_RetryTrue_tdcHistograms.root")
    f2 = ROOT.TFile.Open("ntuplePlots/data_Qinj_87_pix1_powerboard2_RetryTrue_tdcHistograms.root")
    f3 = ROOT.TFile.Open("ntuplePlots/data_Qinj_CF_pix1_powerboard2_RetryTrue_tdcHistograms.root")
    f4 = ROOT.TFile.Open("ntuplePlots/data_Qinj_FF_pix1_powerboard2_RetryTrue_tdcHistograms.root")
    #f5 = ROOT.TFile.Open("ntuplePlots/data_noQInjHistograms.root")

    #maxEvent = 100000.0
    maxEvent = 10000.0

    thresholdLow = 397.0
    thresholdHigh = 650.0

    histos = [
        ("thresholdDAC_hit", 0.0,maxEvent, thresholdLow,thresholdHigh), ("Mean_TOAvsthresholdDAC_hit", 0.0,550.0, thresholdLow,thresholdHigh), ("Mean_TOTvsthresholdDAC_hit", 0.0,140.0, thresholdLow,thresholdHigh), 
        ("STD_TOAvsthresholdDAC_hit", 0.0,5.0, thresholdLow,thresholdHigh), ("STD_TOTvsthresholdDAC_hit", 0.0,2.0, thresholdLow,thresholdHigh), ("TOAHist_hit_dac410", 0.0,0.32*2*maxEvent, 485,510), 
        ("STD_TOATimevsthresholdDAC_hit", 0.0,0.1, thresholdLow,thresholdHigh),
        #("TOTHist_hit_dac410", 0.0,0.32*2*maxEvent, 50,80), ("TOATimeHist_hit_dac410", 0.0,0.32*2*maxEvent, 8.9,9.5), ("TOTTimeHist_hit_dac410", 0.0,0.32*2*maxEvent, 1.8,2.8), 
        #("CALHist_hit_dac410", 0.0,0.32*2*maxEvent, 162.0,175.0)
    ]

    for hName, minimum, maximum, xlow, xhigh in histos:
        h1 = f1.Get(hName)
        h2 = f2.Get(hName)
        h3 = f3.Get(hName)
        h4 = f4.Get(hName)
        #h5 = f5.Get(hName)

        h1.SetLineColor(ROOT.kRed)
        h2.SetLineColor(ROOT.kBlack)
        h3.SetLineColor(ROOT.kGreen + 2)
        h4.SetLineColor(ROOT.kBlue)
        #h5.SetLineColor(ROOT.kMagenta)

        canvas = ROOT.TCanvas("cv"+hName,"cv"+hName,800,800)
        ROOT.gPad.SetLeftMargin(0.16)
        ROOT.gPad.SetRightMargin(0.05)
        ROOT.gPad.SetTopMargin(0.08)
        ROOT.gPad.SetBottomMargin(0.12)
        ROOT.gPad.SetTicks(1,1)
        
        h1.SetStats(0)
        #h1.SetTitle("Threshold Scan")
        h1.SetMinimum(minimum)
        h1.SetMaximum(maximum)
        if xlow and xhigh:
            h1.GetXaxis().SetRangeUser(xlow, xhigh)
        #h1.GetYaxis().SetTitle("Events")
        #h1.GetXaxis().SetTitle("Threshold DAC")
        #h1.GetYaxis().SetTitleSize(0.05)
        #h1.GetYaxis().SetLabelSize(0.035)
        #h1.GetYaxis().SetTitleOffset(1.0)
        #h1.GetXaxis().SetTitleSize(0.05)
        #h1.GetXaxis().SetLabelSize(0.035)
        #h1.GetXaxis().SetTitleOffset(0.95)

        h1.Draw("hist")
        h2.Draw("hist same")
        h3.Draw("hist same")
        h4.Draw("hist same")
        #h5.Draw("h same")

        legend = ROOT.TLegend(0.78,0.70,0.88,0.90);
        legend.SetBorderSize(0)
        legend.SetTextSize(0.03)
        legend.AddEntry(h1, " 7 fC Q_{inj}") #0x37
        legend.AddEntry(h2, "17 fC Q_{inj}") #0x87
        legend.AddEntry(h3, "26 fC Q_{inj}") #0xCF
        legend.AddEntry(h4, "32 fC Q_{inj}") #0xFF
        #legend.AddEntry(h5, "Baseline")
        legend.Draw();

        canvas.SaveAs("{}_multi.gif".format(hName))
 
if __name__ == '__main__':
    main()
