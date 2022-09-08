#!/bin/env python3
import ROOT
import os
ROOT.gROOT.SetBatch(True)
import optparse

def main() :
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option('--Qinj', dest='Qinj', type='int', default = 4, help="Set Qinj register value")
    options, args = parser.parse_args()

    extra = 'NewModule_linear_0V_noBitShift'

    #files = ROOT.TFile.Open("ntuplePlots/addPix_20fC_DAQScan_CheckMode_LGAD_ETROC2_Histograms.root")
    #files = ROOT.TFile.Open("ntuplePlots/allPixels_Qinj_6fC_DAQScan_CheckMode_linear.root")
    #files = ROOT.TFile.Open("ntuplePlots/allPixels_Qinj_6fC_DAQScan_CheckMode_powerboard_v5.root")
    files = ROOT.TFile.Open("ntuplePlots/SRO_Mode_sCurve_"+extra+"_Qinj0xFF_phase0.rootHistograms.root")

    histos2D = [
        ("Jitter2D_TOATimevsthresholdDAC_Pixels_hit",0.0,30.0), ("Baseline2D_thresholdDAC_Pixels_hit",200.0,500.0), ("Jitter2D_TOAvsthresholdDAC_Pixels_hit",0.0,1.6),
    ]

    for hName, minimum, maximum in histos2D:
        h1 = files.Get(hName)
        h1.SetLineColor(ROOT.kBlue)
        h1.SetLineWidth(2)

        canvas = ROOT.TCanvas("cv"+hName,"cv"+hName,900,800)
        ROOT.gPad.SetLeftMargin(0.16)
        ROOT.gPad.SetRightMargin(0.16)
        ROOT.gPad.SetTopMargin(0.08)
        ROOT.gPad.SetBottomMargin(0.12)
        ROOT.gPad.SetTicks(1,1)
        
        h1.SetStats(0)
        #h1.SetTitle("Threshold Scan")
        h1.SetMinimum(minimum)
        h1.SetMaximum(maximum)
        #if xlow and xhigh:
        #    h1.GetXaxis().SetRangeUser(xlow, xhigh)
        #h1.GetYaxis().SetTitle("Events")
        #h1.GetXaxis().SetTitle("Threshold DAC")
        #h1.GetYaxis().SetTitleSize(0.05)
        #h1.GetYaxis().SetLabelSize(0.035)
        #h1.GetYaxis().SetTitleOffset(1.0)
        #h1.GetXaxis().SetTitleSize(0.05)
        #h1.GetXaxis().SetLabelSize(0.035)
        #h1.GetXaxis().SetTitleOffset(0.95)

        h1.Draw("colz text")

        #legend = ROOT.TLegend(0.78,0.70,0.88,0.90);
        #legend.SetBorderSize(0)
        #legend.SetTextSize(0.03)
        #legend.AddEntry(h1, " 4 fC Q_{inj}")
        #legend.AddEntry(h2, " 5 fC Q_{inj}")
        #legend.AddEntry(h3, " 6 fC Q_{inj}")
        #legend.AddEntry(h4, " 8 fC Q_{inj}")
        #legend.AddEntry(h5, "10 fC Q_{inj}")
        #legend.AddEntry(h6, "15 fC Q_{inj}")
        #legend.AddEntry(h7, "20 fC Q_{inj}")
        #legend.Draw();

        canvas.SaveAs("{}.gif".format(hName))
        canvas.SaveAs("{}_linear.pdf".format(hName))
 
if __name__ == '__main__':
    main()
