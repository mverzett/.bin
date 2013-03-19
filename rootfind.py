#! /usr/bin/env python

import sys
import os
from fnmatch import fnmatch
from optparse import OptionParser
import ROOT 


__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"
__doc__ = """script to look at the content of the root file:\n\n
Usage: rootfind file.root [options]"""

def GetContent(dir):
    tempList = dir.GetListOfKeys()
    retList = []
    for it in range(0,tempList.GetSize()):
       retList.append(tempList.At(it).ReadObj())
    return retList

def rootfind( directory, dirName='', **kwargs ):
    if 'max_depth' in kwargs and kwargs['max_depth'] == 0:
        return
    elif 'max_depth' in kwargs:
        kwargs['max_depth'] -= 1
        
    dirContent = GetContent(directory)
    for entry in dirContent:
      path = os.path.join(dirName,entry.GetName())
      if 'name' not in kwargs or fnmatch(path,kwargs['name']):
          if 'type' not in kwargs or \
              not kwargs['type'] or \
              entry.InheritsFrom(kwargs['type']):
              toeval  = 'entry.%s' % kwargs['code']
              addenda = '%s' % eval(toeval) if ('code' in kwargs and kwargs['code']) else ''
              print path,addenda
      if entry.InheritsFrom('TDirectory'):
         subdirName = os.path.join(dirName,entry.GetName())
         rootfind(entry, subdirName, **kwargs)

def parse_options(arguments=sys.argv[1:]):
   parser = OptionParser(description=__doc__)
   parser.add_option('--name', metavar='pattern', type=str, default = '*',
                     help='allows the search for a particular pattern',dest='name')
   parser.add_option('--type', metavar='class'  , type=str, dest='type',default = '',
                     help='searches only for objects matching (or inheriting from) a particular class')
   parser.add_option('--exec', metavar='code'   , type=str,  dest='code', default = '',
                     help='executes a class method on each object found (beware of errors!) and returns the result together with the found object path')
   parser.add_option('--show-errors', action='store_true', dest='show_errors', default = False,
                     help='prints out root error messages when opening the file (usually a bit annoying and therefore suppressed by default)')
   parser.add_option('--max-depth', dest='max_depth', default = -1, type=int,
                     help='maximum depth where to search')

   return parser.parse_args(args=arguments)
   

if __name__ == '__main__':
    (options,file_names) = parse_options()
    tfiles = [ROOT.TFile.Open(name) for name in file_names if '.root' in name]
    
    if not options.show_errors:
        ROOT.gErrorIgnoreLevel = ROOT.kError+1 #Suppress anything that is not an exception

    for tfile in tfiles:
        print "In %s:" % tfile.GetName()
        rootfind( tfile, **vars(options))
