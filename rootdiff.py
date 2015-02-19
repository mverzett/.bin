#! /usr/bin/env python

import sys
import os
from fnmatch import fnmatch
from optparse import OptionParser
import ROOT 
import itertools
import rootfind
from pdb import set_trace

__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"
__doc__ = """script to look at the content of the root file:\n\n
Usage: rootfind file.root [options]"""

def geBins(histo):
   return histo.GetNbinsX(), histo.GetNbinsY(), histo.GetNbinsZ()

def rootdiff(path, obj1, obj2):
   if type(obj1) <> type(obj2):
      print "The two objects provided, named %s, have different type (%s and %s)" % (obj1.GetName(), type(obj1), type(obj2))
   elif isinstance(obj1, ROOT.TH1):
      name = path
      binning1 = geBins(obj1)
      binning2 = geBins(obj2)
      if binning1 <> binning2:
         print "%s: The two histograms have different binning" % name
      xs, ys, zs = binning1
      for xyz in itertools.product(
         xrange(1, xs+1),
         xrange(1, ys+1),
         xrange(1, zs+1)
         ):
         global_bin_num = obj1.GetBin(*xyz)
         center1 = obj1.GetBinCenter(global_bin_num)
         center2 = obj2.GetBinCenter(global_bin_num)
         w1 = obj1.GetBinWidth(global_bin_num)
         w2 = obj2.GetBinWidth(global_bin_num)
         if center1 <> center2 or w1 <> w2:
            print "{name} bin {bin}: have different edges".format(
               name=name,
               bin=xyz.__repr__())
            continue

         c1 = obj1.GetBinContent(*xyz)
         c2 = obj2.GetBinContent(*xyz)

         e1 = obj1.GetBinError(*xyz)
         e2 = obj2.GetBinError(*xyz)
         if c1 <> c2 or e1 <> e2:
            print "{name} bin {bin}: {c1}+/-{e1} --> {c2}+/-{e2}".format(
               name=name,
               bin=xyz.__repr__(),
               c1=c1, e1=e1,
               c2=c2, e2=e2
               )
         
   elif isinstance(obj1, ROOT.TDirectory):
      pass
      #nothing to do here
   else:
      print "WARNING: I do not know how to make diff of: %s" % (type(obj1))
   return

def MapDirStructure( directory, dirName ):
    dirContent = rootfind.GetContent(directory)
    for obj_type, name, _ in dirContent:
        pathname = os.path.join(dirName, name)
        yield pathname
        if rootfind.inherits_from(obj_type, ROOT.TDirectory):
            entry= directory.Get(name)
            for i in MapDirStructure(entry, pathname):
               yield i

if __name__ == '__main__':
   fname2 = sys.argv[-1]
   fname1 = sys.argv[-2]

   tfile1 = ROOT.TFile.Open(fname1)
   tfile2 = ROOT.TFile.Open(fname2)

   dirs1 = set(i for i in MapDirStructure(tfile1, ''))
   dirs2 = set(i for i in MapDirStructure(tfile2, ''))
   
   diff1 = dirs1.difference(dirs2)
   diff2 = dirs2.difference(dirs1)
   if len(diff1) or len(diff2):
      print "different objects in files:"
      for i in diff1:
         print '\t +%s' %i
      for i in diff2:
         print '\t -%s' %i

   for path in dirs1.intersection(dirs2):
      #print "inspecting %s" % path
      obj1 = tfile1.Get(path)
      obj2 = tfile2.Get(path)
      if not obj1 and not obj2:
         print "I could not get %s" % path
      elif not obj1:
         print "I could not get %s from %s" % (path, fname1)
      elif not obj2:
         print "I could not get %s from %s" % (path, fname2)
      else:
         rootdiff(path, obj1, obj2)
      del obj1
      del obj2
