from optparse import OptionParser

parser = OptionParser()
(opts, args) = parser.parse_args()


import pyroot_logon

from ROOT import gSystem

gSystem.Load("Delphes-3.0.9/libDelphes")

from ROOT import *
from array import array

cuts = [
    'Jet[0].PT > 10000',
    'Jet[1].PT > 10000',
    'Jet[0].Eta < 1',
    'Jet[1].Eta < 1',
    ]

def passSelection(event):
    for cut in cuts:
        passing = eval("event.%s" % cut)
        # print cut,passing
        if not passing:
            return False
    return True
    

f = TFile.Open(args[0])

Delphes = f.Get("Delphes")

fout = TFile(args[0].replace('.root', '_histograms.root'), "recreate")

bins = [20.]
while (bins[-1] < 100.):
    bins.append(bins[-1] + int(bins[-1]*0.05))

binEdges = array('d', bins)
print bins

massSpectrum = TH1F("massSpectrum", "dijet mass", len(bins)-1, binEdges)
genSpectrum = TH1F("genSpectrum", "dijet gen spectrum", len(bins)-1, binEdges)

for (eventN, event) in enumerate(Delphes):

    if eventN % 5000 == 0:
        print "processing event %i" % eventN
        
    if not passSelection(event):
        continue

    jet1 = TLorentzVector()
    jet1.SetPtEtaPhiM(event.Jet[0].PT, event.Jet[0].Eta,
                      event.Jet[0].Phi, event.Jet[0].Mass)
    jet2 = TLorentzVector()
    jet2.SetPtEtaPhiM(event.Jet[1].PT, event.Jet[1].Eta,
                      event.Jet[1].Phi, event.Jet[1].Mass)
    dijet = jet1 + jet2
    massSpectrum.Fill(dijet.M()/1000.)


    gjet1 = TLorentzVector()
    gjet1.SetPtEtaPhiM(event.GenJet[0].PT, event.GenJet[0].Eta,
                       event.GenJet[0].Phi, event.GenJet[0].Mass)
    gjet2 = TLorentzVector()
    gjet2.SetPtEtaPhiM(event.GenJet[1].PT, event.GenJet[1].Eta,
                       event.GenJet[1].Phi, event.GenJet[1].Mass)
    gdijet = gjet1 + gjet2      
    genSpectrum.Fill(gdijet.M()/1000.)

    # print "dijet pt", dijet.Pt(), "eta", dijet.Eta(), "phi", dijet.Phi(),
    # print "mass", dijet.M()

    # if eventN > 1000:
    #     break


fout.Write()

print 'events in mass spectrum:', massSpectrum.Integral()
print 'events in underflow:', massSpectrum.GetBinContent(0)

c1 = TCanvas("c1", "Reco dijet")
massSpectrum.Scale(1., "width")
massSpectrum.Draw()

c2 = TCanvas("c2", "Gen dijet")
genSpectrum.Scale(1., "width")
genSpectrum.Draw()
