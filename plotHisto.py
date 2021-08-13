#!/bin/env python3
import ROOT
import os
ROOT.gROOT.SetBatch(True)

def main() :
    f1 = ROOT.TFile.Open("ntuplePlots/data_Qinj_37_workingHistograms.root")
    f2 = ROOT.TFile.Open("ntuplePlots/data_Qinj_87_workingHistograms.root")
    f3 = ROOT.TFile.Open("ntuplePlots/data_Qinj_CF_workingHistograms.root")
    f4 = ROOT.TFile.Open("ntuplePlots/data_Qinj_FF_workingHistograms.root")
    #f5 = ROOT.TFile.Open("ntuplePlots/data_noQInjHistograms.root")

    histos = [("thresholdDAC_hit", 1000.0), ("TOAvsthresholdDAC_hitMean", 1024.0), ("TOTvsthresholdDAC_hitMean", 512.0), ("TOAvsthresholdDAC_hitSTD", 2.0), ("TOTvsthresholdDAC_hitSTD", 2.0), 
              ("TOAHist_hit_dac375", 320.0), ("TOTHist_hit_dac375", 320.0), ("TOATimeHist_hit_dac375", 320.0), ("TOTTimeHist_hit_dac375", 320.0), ("CALHist_hit_dac375", 320.0)]

    for hName, maximum in histos:
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
        h1.SetMinimum(0.0)
        h1.SetMaximum(maximum)
        #h1.GetXaxis().SetRangeUser(360,390)
        #h1.GetYaxis().SetTitle("Events")
        #h1.GetXaxis().SetTitle("Threshold DAC")
        #h1.GetYaxis().SetTitleSize(0.05)
        #h1.GetYaxis().SetLabelSize(0.035)
        #h1.GetYaxis().SetTitleOffset(1.0)
        #h1.GetXaxis().SetTitleSize(0.05)
        #h1.GetXaxis().SetLabelSize(0.035)
        #h1.GetXaxis().SetTitleOffset(0.95)

        h1.Draw("h")
        h2.Draw("h same")
        h3.Draw("h same")
        h4.Draw("h same")
        #h5.Draw("h same")

        legend = ROOT.TLegend(0.70,0.65,0.80,0.85);
        legend.SetBorderSize(0)
        legend.SetTextSize(0.03)
        legend.AddEntry(h1, "Qinj Amp 0x37")
        legend.AddEntry(h2, "Qinj Amp 0x87")
        legend.AddEntry(h3, "Qinj Amp 0xCF")
        legend.AddEntry(h4, "Qinj Amp 0xFF")
        #legend.AddEntry(h5, "Baseline")
        legend.Draw();

        canvas.SaveAs("{}_multi.gif".format(hName))
 
if __name__ == '__main__':
    main()
