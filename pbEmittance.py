import ROOT
from array import array
import copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
import optparse

def getSTD(pix, histInfo, name):
    f = ROOT.TFile.Open(name)
    t = f.Get("tree")
    t.Draw("TOA>>h{}{}({})".format(name,pix,histInfo),"hitFlag==1&&pixNum=={}&&thresholdDAC==500&&HEAD==2".format(pix))
    h = getattr(ROOT,"h"+name+"{}".format(pix))
    std = h.GetStdDev()
    return std

def makeGraph(allFiles, color):
    x, y = array( 'd' ), array( 'd' )
    for p, std in allFiles:
        x.append(p)
        y.append(std)

    g = ROOT.TGraph(len(x), x, y)
    g.SetLineColor( color )
    g.SetLineWidth( 4 )
    g.SetLineStyle(ROOT.kDashed)
    g.SetMarkerColor( color)
    g.SetMarkerStyle( 20 )
    return g

def main() :

    histInfo = "80,480,560"
    allFiles = [
    (0,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_touching.root")),
    (1,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_0cm.root")),
    (2,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_1cm.root")),
    (3,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_2cm.root")),
    (4,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_3cm.root")),
    (5,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_4cm.root")),
    (6,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_5cm.root")),
    (7,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_6cm.root")),
    (8,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_7cm.root")),
    (9,  getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_8cm.root")),
    (10, getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_9cm.root")),
    (11, getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_10cm.root")),
    (12, getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_11cm.root")),
    (13, getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_12cm.root")),
    (18, getSTD(0, histInfo, "Sep6_0V_linear_FF_powerboardOn_18cm.root")),
    ]

    histInfo = "60,280,340"
    allFilesOnPix0 = [
        (0.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_0cm_upright.root")),
        (0.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_0.5cm_upright.root")),
        (1.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_1cm_upright.root")),
        (1.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_1.5cm_upright.root")),
        (2.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_2cm_upright.root")),
        (2.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_2.5cm_upright.root")),
        (3.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_3cm_upright.root")),
        (3.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_3.5cm_upright.root")),
        (4.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_4cm_upright.root")),
        (5.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_5cm_upright.root")),
        (6.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_6cm_upright.root")),
        (8.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_8cm_upright.root")),
        (10.0, getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_10cm_upright.root")),
        (20.0, getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOn_20cm_upright.root")),
    ]    
    allFilesOffPix0 = [
        (0.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_0cm_upright.root")),
        (0.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_0.5cm_upright.root")),
        (1.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_1cm_upright.root")),
        (1.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_1.5cm_upright.root")),
        (2.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_2cm_upright.root")),
        (2.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_2.5cm_upright.root")),
        (3.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_3cm_upright.root")),
        (3.5,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_3.5cm_upright.root")),
        (4.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_4cm_upright.root")),
        (5.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_5cm_upright.root")),
        (6.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_6cm_upright.root")),
        (8.0,  getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_8cm_upright.root")),
        (10.0, getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_10cm_upright.root")),
        (20.0, getSTD(0, histInfo, "Sep7_0V_linear_FF_powerboardOff_20cm_upright.root")),
    ]
    allFilesOnPix13 = [
        (0.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_0cm_upright.root")),
        (0.5,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_0.5cm_upright.root")),
        (1.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_1cm_upright.root")),
        (1.5,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_1.5cm_upright.root")),
        (2.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_2cm_upright.root")),
        (2.5,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_2.5cm_upright.root")),
        (3.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_3cm_upright.root")),
        (3.5,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_3.5cm_upright.root")),
        (4.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_4cm_upright.root")),
        (5.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_5cm_upright.root")),
        (6.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_6cm_upright.root")),
        (8.0,  getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_8cm_upright.root")),
        (10.0, getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_10cm_upright.root")),
        (20.0, getSTD(13, histInfo, "Sep7_0V_linear_FF_powerboardOn_20cm_upright.root")),
    ]  

    gOnPix0OldData = makeGraph(allFiles, ROOT.kBlack)
    gOnPix0 = makeGraph(allFilesOnPix0, ROOT.kRed)
    gOffPix0 = makeGraph(allFilesOffPix0, ROOT.kGreen +2)
    gOnPix13 = makeGraph(allFilesOnPix13, ROOT.kBlue)

    canvas = ROOT.TCanvas("cv","cv",800,800)
    ROOT.gPad.SetLeftMargin(0.16)
    ROOT.gPad.SetRightMargin(0.05)
    ROOT.gPad.SetTopMargin(0.08)
    ROOT.gPad.SetBottomMargin(0.12)
    ROOT.gPad.SetTicks(1,1)
    htemp = ROOT.TH1D("","",10,0,20)
    htemp.SetMaximum(10)
    htemp.SetMinimum(0)
    htemp.GetXaxis().SetTitle("Distance [cm]")
    htemp.GetYaxis().SetTitle("Jitter")
    htemp.Draw()
    gOnPix0OldData.Draw("LP same")
    gOnPix0.Draw("LP same")
    gOffPix0.Draw("LP same")
    gOnPix13.Draw("LP same")

    legend = ROOT.TLegend(0.38,0.65,0.88,0.90);
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    legend.AddEntry(gOnPix0OldData, "Pix 0: connected PB On Old data", "lp")
    legend.AddEntry(gOnPix0,  "Pix 0: connected PB On",  "lp")
    legend.AddEntry(gOffPix0, "Pix 0: connected PB Off", "lp")
    legend.AddEntry(gOnPix13, "Pix 13: not connected PB On", "lp")
    legend.Draw()


    canvas.SaveAs("pbEmittanceResults.gif")
    canvas.SaveAs("pbEmittanceResults.pdf")

if __name__ == '__main__':
    main()