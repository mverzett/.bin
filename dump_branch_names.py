#! /usr/bin/env python
'''
Like edmDumpEventContent, but for custom trees.
The --type option prints together with the branch
name also the C++ type for the branch
'''

import sys
if len(sys.argv) < 3 or '-h' in sys.argv or '--help' in sys.argv:
    print 'Usage dump_branch_names.py file.root path/to/Tree (--type, -t)'
    print __doc__
    sys.exit(1)

print_type = '--type' in sys.argv or '-t' in sys.argv
#Open sample file
import ROOT
ROOT.gROOT.SetBatch(True)
tfile = ROOT.TFile.Open(sys.argv[-2])

tree = tfile.Get(sys.argv[-1])
#Get All the branches
if print_type:
    print '\n'.join(['%20s %20s' % (branch.GetTypeName() if hasattr(branch, 'GetTypeName') else branch.GetClassName(), branch.GetName()) \
                         for branch in tree.GetListOfBranches()])
else:
    print '\n'.join([branch.GetName() for branch in tree.GetListOfBranches()])
tfile.Close()
