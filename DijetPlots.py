import pyroot_logon
from ROOT import *

processes = ['qcd', '30', '40', '50', '60']
xsecs = { 'qcd' : 9.720e-10 * 1e12,
          '30' : 2.28e-11 * 1e12,
          '40' : 9.86e-13 * 1e12,
          '50' : 4.38e-14 * 1e12,
          '60' : 2.22e-15 * 1e12,
          } # xsec in fb

effs = { 'qcd' : 11402./1.e5,
          '30' : 8395./1.e4,
          '40' : 8866./1.e4,
          '50' : 8756./1.e4,
          '60' : 8222./1.e4
          } # overal efficiency * acceptances

colors = { '30' : kRed + 1,
           '40' : kCyan + 2,
           '50' : kGreen + 1,
           '60' : kMagenta +2
           }

lumis = [ 1,
          100,
          1000,
          3000,
          ] # integrated luminosities in fb

def qcdPdf(ws, mass=None):
    if not mass:
        mass = ws.var('mass')

    ws.factory('c_qcd[-0.2158, -5, 0]')
    ws.factory('turnOn_qcd[25.33, 0., 100]')
    ws.factory('width_qcd[5.94, 0., 20.]')

    ws.factory('RooErfExpPdf::qcd(%s,c_qcd,turnOn_qcd,width_qcd)' % mass.GetName())

    return ws.pdf('qcd')

def qstar30Pdf(ws, mass=None):
    if not mass:
        mass = ws.var('mass')

    ws.factory('sigma_comb_30TeV[8.6, 0., 20.]')
    ws.factory('mean_comb_30TeV[35.5, 0., 100.]')
    ws.factory('RooGaussian::comb_30TeV(%s,mean_comb_30TeV,sigma_comb_30TeV)' % mass.GetName())

    ws.factory('mean_30TeV[30.92, 0., 100.]')
    ws.factory('sigma_30TeV[2.4, 0., 20.]')
    ws.factory('f_peak_30TeV[0.663, 0., 1.]')

    ws.factory('RooGaussian::peak_30TeV(%s,mean_30TeV,sigma_30TeV)' % mass.GetName())
    ws.factory('SUM::qstar_30TeV(f_peak_30TeV*peak_30TeV, comb_30TeV)')

    return ws.pdf('qstar_30TeV')

def qstar40Pdf(ws, mass=None):
    if not mass:
        mass = ws.var('mass')

    ws.factory('mean_40TeV[40.43, 0., 100.]')
    ws.factory('sigma_40TeV[2.2, 0., 20.]')
    ws.factory('f_peak_40TeV[0.672, 0., 1.]')

    ws.factory('RooGaussian::peak_40TeV(%s,mean_40TeV,sigma_40TeV)' % mass.GetName())

    ws.factory('sigma_comb_40TeV[9.27, 0., 20.]')
    ws.factory('RooGaussian::comb_40TeV(%s,mean_40TeV,sigma_comb_40TeV)' % mass.GetName())
    ws.factory('SUM::qstar_40TeV(f_peak_40TeV*peak_40TeV, comb_40TeV)')

    return ws.pdf('qstar_40TeV')

def qstar50Pdf(ws, mass=None):
    if not mass:
        mass = ws.var('mass')

    ws.factory('mean_50TeV[50.07, 0., 100.]')
    ws.factory('sigma_50TeV[2.19, 0., 20.]')
    ws.factory('f_peak_50TeV[0.712, 0., 1.]')

    ws.factory('RooGaussian::peak_50TeV(%s,mean_50TeV,sigma_50TeV)' % mass.GetName())

    ws.factory('sigma_comb_50TeV[11.14, 0., 20.]')
    ws.factory('mean_comb_50TeV[45.96, 0., 100.]')
    ws.factory('RooGaussian::comb_50TeV(%s,mean_comb_50TeV,sigma_comb_50TeV)' % mass.GetName())
    ws.factory('SUM::qstar_50TeV(f_peak_50TeV*peak_50TeV, comb_50TeV)')

    return ws.pdf('qstar_50TeV')

def qstar60Pdf(ws, mass=None):
    if not mass:
        mass = ws.var('mass')

    ws.factory('mean_60TeV[59.47, 0., 100.]')
    ws.factory('sigma_60TeV[2.23, 0., 20.]')
    ws.factory('f_peak_60TeV[0.664, 0., 1.]')
    ws.factory('RooGaussian::peak_60TeV(%s,mean_60TeV,sigma_60TeV)' % mass.GetName())

    ws.factory('m_on_60TeV[24.9, 0., 100.]')
    ws.factory('width_on_60TeV[7.5, 0., 20.]')
    ws.factory('RooErfPdf::comb_on_60TeV(%s, m_on_60TeV, width_on_60TeV)' % mass.GetName())

    ws.factory('m_off_60TeV[67., 0., 100.]')
    ws.factory('width_off_60TeV[9.2, 0., 20.]')
    ws.factory('EXPR::comb_off_60TeV("(1-TMath::Erf((@0-@1)/@2))/2", %s, m_off_60TeV, width_off_60TeV)' % mass.GetName())

    ws.factory('PROD::comb_60TeV(comb_on_60TeV,comb_off_60TeV)')

    ws.factory('SUM::qstar_60TeV(f_peak_60TeV*peak_60TeV, comb_60TeV)')

    return ws.pdf('qstar_60TeV')

def buildPdfs(ws, mass=None):
    qcdPdf(ws, mass)
    qstar30Pdf(ws, mass)
    qstar40Pdf(ws, mass)
    qstar50Pdf(ws, mass)
    qstar60Pdf(ws, mass)

def makeSumPdf(ws, component, Nqcd, Nqstar):
    return ws.factory('SUM::sum_%sTeV(%.4f*qstar_%sTeV,qcd)' % \
                      (component, Nqstar/float(Nqcd+Nqstar), component))

ws_qstar = RooWorkspace('qstar', 'qstar')
mass = ws_qstar.factory('mass[20, 100]')
mass.setUnit('TeV')
mass.SetTitle('dijet mass')
mass.setPlotLabel(mass.GetTitle())
mass.setBins(80)
obs = RooArgSet(mass)

buildPdfs(ws_qstar, mass)

for L in lumis:
    # L = lumis[2]
    plot = mass.frame()
    N_qcd = 0
    print 'Lumi:',L
    for component in processes:
        N = xsecs[component]*effs[component]*L
        print "N",component,N
        if component == 'qcd':
            N_qcd = N
            ws_qstar.pdf('qcd').plotOn(
                plot,
                RooFit.Normalization(N, RooAbsReal.NumEvent),
                RooFit.LineColor(kBlue+2)
                )
        else:
            # makeSumPdf(ws_qstar, component, N_qcd, N).plotOn(
            ws_qstar.pdf('qstar_%sTeV' % component).plotOn(
                plot,
                RooFit.Normalization(N, RooAbsReal.NumEvent),
                RooFit.LineStyle(kDashed),
                RooFit.LineColor(colors[component])
                )
            mean = ws_qstar.var('mean_%sTeV' % component).getVal()
            sigma = ws_qstar.var('sigma_%sTeV' % component).getVal()
            mass.setRange('signal_%s' % component, mean-2*sigma,
                          mean+2*sigma)

            qcdIntegral = ws_qstar.pdf('qcd').createIntegral(obs, obs, 'signal_%s' % component).getVal()
            signalIntegral = ws_qstar.pdf('qstar_%sTeV' % component).createIntegral(obs, obs, 'signal_%s' % component).getVal()
            print 'within range', mean-2*sigma, '< m <', mean+2*sigma
            print 'signal integral', signalIntegral,
            print 'signal yield', signalIntegral*N
            print 'background integral', qcdIntegral,
            print 'background yield', qcdIntegral*N_qcd

plot.GetYaxis().SetTitle('Events / TeV')
plot.SetMinimum(0.01)
plot.SetMaximum(1e5)
plot.Draw()
gPad.SetLogy()
gPad.Update()

import math

logline = 4
line = 2*10**logline
logLineSpace = 5e3/line
print logline, line, logLineSpace
L = TLatex()
L.SetTextFont(42);
L.SetTextAlign(31);
L.DrawLatex(95., line, 'jets: |#eta| < 1., p_{T} > 10 TeV')
logline -= logLineSpace
line *= logLineSpace
print logline, line
L.DrawLatex(95, line, '100TeV pp VLHC')
logline -= logLineSpace
line *= logLineSpace
print logline, line
L.DrawLatex(95., line, '#scale[0.5]{#lower[-0.15]{#it{#int}}}#it{L} dt = 3 ab^{-1}')

gPad.Update()



gPad.Print('qstar_100TeV.png')
gPad.Print('qstar_100TeV.pdf')


c2 = TCanvas()
L2 = TLatex()
L2.SetTextFont(42);
c2.SetLogy()
gr = TGraph('ExpectedLimits.txt')
gr.SetName('expLimits')
gr.Draw('al')
gr.SetLineColor(kBlue+2)
gr.SetLineWidth(2)
gr.SetLineStyle(kDashed)
gPad.Update()
gr.GetXaxis().SetLimits(30, 60)
gr.GetXaxis().SetTitle('q* mass (TeV)')
gr.GetYaxis().SetTitle('95% CL expected limit #sigma/#sigma_{theory}')
OneAxis = TLine(30., 1., 60., 1.)
OneAxis.SetLineColor(kRed)
OneAxis.SetLineWidth(2)
OneAxis.Draw()
L2.DrawLatex(32, 5., '100TeV pp VLHC')
L2.DrawLatex(32, 2.5, '#scale[0.5]{#lower[-0.15]{#it{#int}}}#it{L} dt = 3 ab^{-1}')
gPad.Update()

gr2 = TGraph(gr.GetN(), gr.GetY(), gr.GetX())
print 'exclusion upto q* mass of %.2f TeV' % gr2.Eval(1.)

gPad.Print('qstar_limits.png')
gPad.Print('qstar_limits.pdf')


