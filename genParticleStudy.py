from optparse import OptionParser

parser = OptionParser()
(opts, args) = parser.parse_args()


import pyroot_logon

from ROOT import gSystem

from DataFormats.FWLite import Events, Handle

from ROOT import *
from array import array

events = Events (args)
handle = Handle('vector<reco::GenParticle>')

label = ('genParticles')

def printParticleDecayTree(mom, prefix = '', statusCutoff = 1):
    if mom.status() >= statusCutoff:
        print prefix+'id:',mom.pdgId(),'status:',mom.status(),\
            'nDau:',mom.numberOfDaughters(),'(pt,eta,phi,m):',\
            '(%.1f,%.1f,%.1f,%.0f)' % (mom.pt(), mom.eta(), mom.phi(),
                                       mom.mass())
        for dau in range(0, mom.numberOfDaughters()):
            daughter = mom.daughter(dau)
            if daughter.status() >= statusCutoff:
                printParticleDecayTree(daughter, '  ' + prefix, statusCutoff)

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

for (eventN, event) in enumerate(events):

    if eventN % 5000 == 0:
        print "processing event %i" % eventN

    event.getByLabel(label, handle)
    genParts = handle.product()
        
    # printParticleDecayTree(genParts[0], "", 3)

    foundParticle = False
    for genParticle in genParts:
        if abs(genParticle.pdgId()) in [4000001, 4000002]:
            # printParticleDecayTree(genParticle, "", 3)
            massSpectrum.Fill(genParticle.mass()/1000.)
            foundParticle = True
            break

    if not foundParticle:
        printParticleDecayTree(genParts[0], "", 3)
    # massSpectrum.Fill(dijet.M()/1000.)

    # if eventN > 9:
    #     break

fout.Write()

massSpectrum.Scale(1., "width")
massSpectrum.Draw()

