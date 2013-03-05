#! /usr/bin/env python

import sys
import os
from fnmatch import fnmatch
from optparse import OptionParser
import ROOT 

__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"
__doc__ = """script to look at the content of the root file:\n\n
Usage: rootfind file.root [options]"""

parser = OptionParser(description=__doc__)
parser.add_option('--name', metavar='pattern', type=str, help='allows the search for a particular pattern',dest='name',default = '*')
parser.add_option('--type', metavar='class'  , type=str, help='searches only for objects matching (or inheriting from) a particular class', dest='type',default = '')
parser.add_option('--exec', metavar='code'   , type=str, help='executes a class method on each object found (beware of errors!) and returns the result together with the found object path', dest='code', default = '')

(options,file_name) = parser.parse_args()
tfile = ROOT.TFile.Open(file_name[0])

def GetContent(dir):
    tempList = dir.GetListOfKeys()
    retList = []
    for it in range(0,tempList.GetSize()):
       retList.append(tempList.At(it).ReadObj())
    return retList

def rootfind( directory, dirName='' ):
    dirContent = GetContent(directory)
    for entry in dirContent:
        path = os.path.join(dirName,entry.GetName())
        if fnmatch(path,options.name):
            if not options.type or entry.InheritsFrom(options.type):
                toeval  = 'entry.%s' % options.code
                addenda = '%s' % eval(toeval) if options.code else ''
                print path,addenda
        if entry.InheritsFrom('TDirectory'):
            subdirName = os.path.join(dirName,entry.GetName())
            rootfind(entry, subdirName)

rootfind( tfile )
