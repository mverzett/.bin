#! /usr/bin/env python

'''
Loads an ED event file (PAT, miniAOD, AOD, etc) and loads a collection you want to inspect,
leaves the interpreter open

Author: Mauro Verzetti UR
'''

from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument('file', help='file path')
parser.add_argument('info', nargs='+', help='what to dump, in the form "handle|label(|simplename)", multiple objets supported')
parser.add_argument('--pick', help='which single event to pick')
parser.add_argument('--inrun', action='store_true', help='get collection from the Run and not Event')
args = parser.parse_args()

pick = False
if args.pick:
   pick = tuple([int(i) for i in args.pick.split(':')])

import ROOT
import pprint
from DataFormats.FWLite import Events, Handle, Runs
from pdb import set_trace
ROOT.gROOT.SetBatch()

fname = args.file
if fname.startswith('/store/'):
   fname = 'root://cmsxrootd-site.fnal.gov/%s' % fname

events = Runs(fname) if args.inrun else Events(fname)
iterator = events.__iter__()
handles = {}
handle_names = {}
labels = {}
for info in args.info:
   splitted = info.split('|')
   if len(splitted) == 2:
      name = splitted[1]
   elif len(splitted) == 3:
      name = splitted[2]
   else:
      raise ValueError('The info %s is not properly formatted' % info)
   handles[name] = Handle(splitted[0])
   labels[name]  = splitted[1]
   handle_names[name] = splitted[0]
   
keep_going = True
loop = 0

while keep_going:
   evt = iterator.next()
   loop += 1
   if pick:
      evtid = (evt.eventAuxiliary().run(), evt.eventAuxiliary().luminosityBlock(), evt.eventAuxiliary().event())
      if evtid == pick:
         keep_going = False
   else:
      get_result = all(evt.getByLabel(labels[i], handles[i]) for i in handles)      
      print('loop %d' % loop)
      if not get_result: continue
      objs = {i : j.product() for i, j in handles.iteritems()}
      has_objs = all(objs[i].size() != 0 for i, j in handle_names.iteritems() if 'vector' in j)
      keep_going = not has_objs

print "object/collection successfully loaded into obj, entering debugging mode"
set_trace()
