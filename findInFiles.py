#! /usr/bin/env python

__doc__ = 'looks into the directory and sub-dirs performing a regex search in the files.\n\nUsage: findInFiles regex path [options]'

import re
from optparse import OptionParser
import os

parser = OptionParser(description=__doc__)
parser.add_option('--followSymLinks','-f',action="store_true", metavar='',help='follows symbolic links',dest='flinks',default = False)
parser.add_option('--maxDepth','-D',metavar='number', type=int,help='Sets the maximum depth to look at',dest='Mdepth',default = 20)

(options,pars) = parser.parse_args()
path = pars[1]
regex = re.compile(pars[0])

def MapDirStructure( directory, objectList, followLinks, depth=0 ):
    dirContent = os.listdir(directory)
    for entry in dirContent:
        fpath = os.path.join(directory,entry)
        if os.path.islink( fpath ):
            if followLinks:
                fpath = os.path.realpath( fpath )
            else:
                return
        if os.path.isdir( fpath ) and depth <= options.Mdepth:
            MapDirStructure(fpath, objectList, followLinks,depth+1)
        elif os.path.isfile( fpath ):
            objectList.append(fpath)

thisPath     = os.path.join( os.getcwd() , path)
thisRealPath = os.path.realpath( thisPath )

files = []
MapDirStructure( thisRealPath, files, options.flinks)

for f in files:
    
