#! /usr/bin/env python

__doc__     = "shell-like environment to navigate in root files. Similar to rootpy roosh, but with no rootpy deps and faster to load"
__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"

import sys
from cStringIO import StringIO
import os
import re
import fnmatch
from optparse import OptionParser
import rootfind
import ROOT
import shlex
import time
import subprocess
ROOT.gROOT.SetBatch()

sys.stdout = os.fdopen(os.dup(sys.stdout.fileno()), 'w')
c_stdout = ".session.%s.c_stdout" % int(time.mktime(time.gmtime())) 
class stdout_locker(object):
    def __init__(self):
        self.c_stdout = c_stdout
        self.locked = False
        self.backup = None
        
    def lock(self):
        if not self.locked:
            self.backup = sys.stdout 
            sys.stdout  = StringIO()
            ROOT.gROOT.ProcessLine('freopen("%s", "w", stdout);' % self.c_stdout)
            self.locked = True
            
    def read(self):
        if self.locked:
            ret = sys.stdout.getvalue()
            sys.stdout.close()       # close the stream
            ROOT.gROOT.ProcessLine('fclose (stdout);')
            sys.stdout = self.backup # restore original stdout
            ret += open(self.c_stdout).read()
            os.system("rm %s" % self.c_stdout)
            self.locked = False
            return ret

class CommandException(Exception):
    def __init__(self,*args,**kwargs):
        super(CommandException, self).__init__(*args,**kwargs)

#most probably redundant
global __main_dir 
global __file     
global __file_name
global __PWD      
global __env_vars

__main_dir         = None
__file             = None
__file_name        = None
__PWD              = ''
__env_vars_regex   = re.compile("\$\w+")
__BLUE             = '\033[94m'
__GREEN            = '\033[92m'
__RED              = '\033[91m'
__END_COL          = '\033[0m'
__locker           = stdout_locker()
__file_map         = {}
__path_regex       = '(?:(?:\.\.|\w+)/?)+'
__history          = []
__max_history_len  = 500
__def_canvas       = ROOT.TCanvas('__def_canvas','__def_canvas',800,600)
__tmp_file         = '.session.%s' % int(time.mktime(time.gmtime()))
__vars             = {}

def history_append(cmd):
    if len(__history) == 500:
        __history.pop(0)
    __history.append(cmd)
    

def write_file_map_entry(name, title, obj_type):
    color = ''
    if rootfind.inherits_from(obj_type, ROOT.TH1):
        color = __RED
    elif rootfind.inherits_from(obj_type, ROOT.TTree):
        color = __GREEN
    elif rootfind.inherits_from(obj_type, ROOT.TDirectory):
        color = __BLUE

    return {
        'name' : name,
        'color': color,
        'cname': str(obj_type).replace("<class '",'').replace("'>",''),
        'title': title,
        }

def MapDirStructure( directory, dirName ):
    dirContent = rootfind.GetContent(directory)
    for obj_type, name, title in dirContent:
        pathname = os.path.join(dirName, name)
        __file_map[pathname] = write_file_map_entry(name, title, obj_type)
        if rootfind.inherits_from(obj_type, ROOT.TDirectory):
            entry= directory.Get(name)
            MapDirStructure(entry, pathname)

def get_proper_path(path):
    'relative to absolute path translation'
    ret = re.sub('\w+/\.\./?','',path)
    ret = ret.replace('//','/')
    ret = ret.replace('./','')
    ret = ret.strip('/')
    if ret == path:
        return ret
    else:
        return get_proper_path(ret)

def absolute_to_relative(path):
    'absolute to relative path translation'
    #Finds the longest common prefix of two strings, as effecicient as possible since it is likely to be repeated multiple times
    if path == __PWD: #special case to avoid empty string
        return '../'+path.split('/')[-1]
    dir_pwd = __PWD.split('/')
    dir_pat = path.split('/')
    max_len = min( len(dir_pwd), len(dir_pat) )
    char    = max_len
    for i in xrange(max_len):
        if dir_pwd[i] != dir_pat[i]:
            char = i
    ret = '/'.join(dir_pat[char:])
    backs = len(dir_pwd[char:]) if __PWD != '' else 0
    return '../'*backs+ret
        
    
def get_object(path):
    'gets the root object'
    return __file.Get(path) if path != '' else __file

def expand_vars(string):
    ret = string
    for var in __env_vars_regex.findall(string):
        if var.strip('$') in os.environ:
            ret = ret.replace(var,os.environ[var.strip('$')])
    return ret

def ls(*args):
    parser = OptionParser(description='List information about the OBJECTSs (the current directory by default).')
    parser.add_option('--no-colors', action='store_true', default = False,
                      help='allows the search for a particular pattern', dest='no_color')
    parser.add_option('-l', action='store_true', default = False, dest='list',
                      help='use a long listing format')
    args = list(args)
    try:
        options, arguments = parser.parse_args(args=args[1:])
    except SystemExit:
        return 0

    def _color_name(entry, tocolor):
        if options.no_color or not entry['color']:
            return  tocolor
        else:
            return  entry['color']+tocolor+__END_COL
    
    directory = arguments[0] if len(arguments) else '*'
    pattern   = get_proper_path(__PWD+'/'+directory)
    # add /* in case it's a directory FIXME add -d option
    pattern   = pattern+'/*' if (pattern in __file_map and __file_map[pattern]['color'] == __BLUE) else pattern
    pattern   = '*' if pattern == '' else pattern
    pattern   = fnmatch.translate(pattern) #translate linux-like matching into regex
    pattern   = pattern.replace('.*','\w*') #the translation is not perfect, / is not treated as special
    regex     = re.compile(pattern)
    for path, entry in __file_map.iteritems():
        if regex.match(path):
            if not options.list:
                print  _color_name( entry, absolute_to_relative(path) )
            else:
                print  '%30s%30s       %s' % (entry['cname'], _color_name( entry, absolute_to_relative(path) ), entry['title']) 
    print
    return 0

def cd(*args):
    #raise Exception( '%s' % args.__repr__())
    new_pwd = get_proper_path( globals()['__PWD']+'/'+args[1]) #for some reason it sees it as local and local only
    obj     = get_object(new_pwd)
    if obj and obj.InheritsFrom('TDirectory'):
        globals()['__PWD'] = new_pwd
        del obj
        return 0
    elif obj:
        print "%s does not exist"
        return 1
    else:
        print "%s is not a direcotry!"
        del obj
        return 1

def find(*args):
    args = list(args)
    try:
        (options, directory) = rootfind.parse_options(args[1:])
    except SystemExit:
        return 0
    directory = directory[0]
    rootfind.rootfind( get_object(get_proper_path(__PWD+'/'+directory)), directory, **vars(options) )
    return 0

def history(*args):
    for i,entry in enumerate(__history):
        print '%s    %s' % (i, entry)

def sys_exit(*args):
    if os.path.isfile(__tmp_file):
        os.system('rm %s' % __tmp_file)
    if os.path.isfile(c_stdout):
        os.system('rm %s' % c_stdout)
    exit()

def call_shell(*args):
    '''interfaces with the shell
    to implement some commands'''
    p = subprocess.Popen(list(args)+[__tmp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #FIXME actually can send to stdin, but no need by now
    out, err = p.communicate()
    exitcode = p.wait()
    if exitcode != 0:
        print err
    ##     raise Exception(err)
    print out
    
__cmds = {
    'ls'      : ls,
    'cd'      : cd,
    'find'    : find,
    'exit'    : sys_exit,
    'history' : history,
    'awk'     : call_shell,
    'head'    : call_shell,
    'tail'    : call_shell,
    'grep'    : call_shell,
    }

def flush(*args):
    cmd = args[0]
    if any(i in cmd for i in ['.png', '.eps', '.pdf', '.jpg', '.root', '.C']): #is a picture!
        __def_canvas.Update()
        __def_canvas.Print(cmd)
    else:
        with open(cmd,'w') as outfile:
            with open(__tmp_file) as infile:
                outfile.write(infile.read())

def root_evaluate(*args):
    line = ' '.join(args)
    path  = re.match('(?P<path>'+__path_regex+')\.\w+\(',line).group('path')
    full_path = get_proper_path(__PWD+'/'+path)
    if full_path not in __file_map:
        print "%s: no such object" % path
        return
    elif full_path not in __vars: #loads variable to keep it persistent
        __vars[full_path] = __file.Get(full_path)
    obj  = __vars[full_path]
    line = line.replace(path,'obj')
    #FIXME: should catch exceptions instead of exiting!
    print eval(line)
    return
  

def parse_command(cmd):
    '''finds the first character able to interrupt a command:
    | or > return its position together with the cation to take'''
    tokenized = shlex.split(cmd, posix=False)
    parse_sequence = []
    args           = []
    command        = None
    for token in tokenized:
        if token == '|' or token == '>':
            parse_sequence.append((command,args))
            args    = []
            command = None if token == '|' else flush
        elif not command:
            if token in __cmds:
                command = __cmds[token]
                args.append(token)
            elif re.match(__path_regex+'\.\w+\(',token):
                command = root_evaluate
                args.append(token)
            else:
                raise CommandException("command %s does not exist" % token)
        else:
            args.append(token)
    parse_sequence.append((command,args))
    return parse_sequence

def execute_command( cmd ):
    try:
        parse_sequence = parse_command(cmd)
    except CommandException as e:
        print '%s' % e
        return
    stdout         = ''
    counter        = len(parse_sequence)
    for command, args in parse_sequence:
        if command is not None:
            counter -= 1
            #__locker.lock() #chatches stdout
            command(*args)   #call the command
            #stdout = __locker.read()
            #if counter > 0:
            #    with open(__tmp_file,'w') as f:
            #        f.write(stdout)
            #elif stdout != '':
            #    print stdout,
    

def shell():
    while True:
        cmd = raw_input("%s:%s> " % (__file_name,__PWD) )
        #remove leading/trailing spaces
        cmd = cmd.strip()
        #expand env variables to their values
        cmd = expand_vars(cmd)
        history_append(cmd)
        execute_command(cmd)

if __name__ == '__main__':
    __file_name= sys.argv[-1]
    __file     = ROOT.TFile.Open(__file_name)
    MapDirStructure(__file,'') #Initialize file map
    #print __file_map
    shell()
    
