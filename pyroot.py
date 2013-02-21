#Simple macro to emulate many things of root in python, to be executer at startup in interactive session
import sys
from ROOT import *

tfiles = filter(lambda x: x.find('.root') != -1, sys.argv)
for f in tfiles:
    print 'attaching %s as file%s' % (f,tfiles.index(f))
    globals()['file%s' % tfiles.index(f)] = TFile.Open(f) 
