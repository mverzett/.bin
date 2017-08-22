#! /bin/env python
import subprocess
import os
import time
from argparse import ArgumentParser
import json
from pdb import set_trace
import sys

parser = ArgumentParser('program to make graph of a time changing quantity')
parser.add_argument("cmds", nargs='*', help="command to be used. MUST return a float")
parser.add_argument("-o", dest='out', default='graph.pdf', help="output")
parser.add_argument("-w", dest='wait', type=int, default=5, help="point spacing (waiting time)")
parser.add_argument("-l", dest='log', help="json log")
parser.add_argument("--from", dest='json', help="json log")
args = parser.parse_args()

#sanitize inputs because ROOT is a little crying brat
sys.argv = []
from ROOT import TGraph, TCanvas, gROOT
import ROOT
gROOT.SetBatch()
ROOT.gErrorIgnoreLevel = ROOT.kWarning
entries = []
if args.json:
   entries = json.loads(open(args.json).read())

canvas = TCanvas('aa','asd', 800, 800)
for count in xrange(10000 if not args.json else 1):
   vals = []
   if not args.json:
      for cmd in args.cmds:
         proc  = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, shell=True
            )
         out, err = proc.communicate()
         code = proc.wait()
         if code != 0:
            raise RuntimeError('The command "%s" \n failed with message: \n\n%s' % (cmd, err))
         
         try:
            val = float(out)
         except:
            raise RuntimeError('Could not convert the output value (%s) to float' % out)
         vals.append(val)

      entries.append({
            'time' : time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()),
            'delta': count*args.wait,
            'value': vals,
            })
   graphs = [TGraph(len(entries)) for _ in range(len(args.cmds) if not args.json else len(entries[0]['value']))]
   m, M = float('inf'), float('-inf')
   for i, entry in enumerate(entries):      
      x = entry['delta']
      for y, g in zip(entry['value'], graphs):
         m = min(m, y)
         M = max(M, y)
         g.SetPoint(i, x, y)
   colors = [1, 2, 8, 9, 28]
   first = True
   for g, color in zip(graphs, colors):
      g.SetLineColor(color)
      g.SetMarkerStyle(20)
      g.SetLineWidth(2)
      if first:
         first = False
         g.Draw('AL')
         g.SetMinimum(m*0.8)
         g.SetMaximum(M*1.2)
         g.Draw('AL')
      else:
         g.Draw('L same')
   canvas.SaveAs(args.out)

   if args.log:
      with open(args.log, 'w') as log:
         log.write(json.dumps(entries))
   time.sleep(args.wait)
   
