#! /bin/env python

from argparse import ArgumentParser
from pdb import set_trace

parser = ArgumentParser()
parser.add_argument('paths', nargs='+', help='histograms to compare root_file_path:histo_path[:other_histo], if no histogram name is provided the previous one is used.')
parser.add_argument('--legend', '-l', help='coma-sparated list of legend entries to be used')
parser.add_argument('-o', default='out.png', help='output file')
#add ratio option

args = parser.parse_args()

import ROOT #would be much nicer with roopy, but is way less portable

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()

histos = []
tfiles = []
last_path = ''
for inpath in args.paths:
   paths = inpath.split(':')
   tfpath = paths[0]
   hpaths = paths[1:] if len(paths) > 1 else [last_path]
   if len(paths) == 1 and not last_path:
      raise ValueError('No histogram path provided, and there is no previous path available! (%s)' % inpath)
   last_path = hpaths[-1]
   tfile = ROOT.TFile.Open(tfpath)
   tfiles.append(tfile)
   for hpath in hpaths:
      histo = tfile.Get(hpath)
      histo.SetLineWidth(2)
      histos.append(
         histo
         )
      
colors = [1, ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kCyan, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kYellow+1]
for histo, color in zip(histos, colors):
   histo.SetLineColor(color)

canvas = ROOT.TCanvas()
first = True
for h in histos:
   opts = 'hist' if first else 'hist same'
   first = False
   h.Draw(opts)

if args.legend:
   leg = ROOT.TLegend(0.1,0.7,0.48,0.9)
   ## if args.title:
   ##    leg.SetHeader(args.title)
   for h, n in zip(histos, args.legend.split(',')):
      leg.AddEntry(h, n, 'l')
   leg.Draw()

canvas.SaveAs(args.o)
