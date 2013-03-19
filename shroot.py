#! /usr/bin/env python

__doc__     = "shell-like environment to navigate in root files. Similar to rootpy roosh, but with no rootpy deps and faster to load"
__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"

import sys
import os
import re
from fnmatch import fnmatch
from optparse import OptionParser
import rootfind
import ROOT 

#most probably redundant
global __main_dir 
global __file     
global __file_name
global __PWD      
global __env_vars

__main_dir = None
__file     = None
__file_name= None
__PWD      = ''
__env_vars = re.compile("\$\w+")

## TFile.Open(f)
def get_proper_path(path):
    ret = re.sub('\w+/\.\./','',path)
    ret = ret.replace('//','/')
    ret = ret.replace('./','')
    ret = ret.strip('/')
    if ret == path:
        return ret
    else:
        return get_proper_path(ret)

def get_object(path):
    'gets the root object'
    return __file.Get(path) if path != '' else __file

def expand_vars(string):
    ret = string
    for var in __env_vars.findall(string):
        if var.strip('$') in os.environ:
            ret = ret.replace(var,os.environ[var.strip('$')])
    return ret

def ls(*args):
    parser = OptionParser(description='List information about the OBJECTSs (the current directory by default).')
    parser.add_option('--color', action='store_true', default = False,
                      help='allows the search for a particular pattern', dest='color')
    parser.add_option('-l', action='store_true', default = False, dest='list',
                      help='use a long listing format')
    args = list(args)
    try:
        options, arguments = parser.parse_args(args=args)
    except SystemExit:
        return 0
    directory = arguments[0] if len(arguments) else ''
    dir_condtent = rootfind.GetContent(get_object(get_proper_path(__PWD+'/'+directory)))
    for obj in dir_condtent:
        if not options.list:
            print '%40s' % obj.GetName(),
        else:
            print '%30s%30s       %s' % (obj.ClassName(), obj.GetName(), obj.GetTitle())
    print
    return 0

def cd(*args):
    new_pwd = get_proper_path(globals()['__PWD']+'/'+args[0]) #for some reason it sees it as local and local only
    obj     = get_object(new_pwd)
    if obj and obj.InheritsFrom('TDirectory'):
        globals()['__PWD'] = new_pwd
        return 0
    elif obj:
        print "%s does not exist"
        return 1
    else:
        print "%s is not a direcotry!"
        return 1

def find(*args):
    args = list(args)
    try:
        (options, directory) = rootfind.parse_options(args)
    except SystemExit:
        return 0
    directory = directory[0]
    rootfind.rootfind( get_object(get_proper_path(__PWD+'/'+directory)), directory, **vars(options) )
    return 0

def sys_exit(*args):
    exit()
    
__cmds = {
    'ls'   : ls,
    'cd'   : cd,
    'find' : find,
    'exit' : sys_exit,
    }
def shell():
    while True:
        cmd = raw_input("%s:%s> " % (__file_name,__PWD) )
        #remove leading/trailing spaces
        cmd = cmd.strip()
        #expand env variables to their values
        cmd = expand_vars(cmd)
        argvs = cmd.split(' ')
        if argvs[0] in __cmds:
            __cmds[argvs[0]](*argvs[1:])

if __name__ == '__main__':
    __file_name= sys.argv[-1]
    __file     = ROOT.TFile.Open(__file_name)
    shell()
    
