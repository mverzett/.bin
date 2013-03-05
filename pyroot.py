#Simple macro to emulate many things of root in python, to be executer at startup in interactive session
import sys
import re
from ROOT import *
print 'you can navigate the file just using cd(file/directory) (as string) and ls(). ls() shows directories in blue, trees in green the rest in black. You can ask pwd() to know which is the current position'


tfiles = filter(lambda x: x.find('.root') != -1, sys.argv)
for f in tfiles:
    print 'attaching %s as file%s' % (f,tfiles.index(f))
    globals()['file%s' % tfiles.index(f)] = TFile.Open(f) 

## __main_dir = gDirectory
## __PATH     = ''
## __BLUE     = '\033[94m'
## __GREEN    = '\033[92m'
## __ENDC     = '\033[0m'
## __color    = lambda txt, color: ''.join([color,txt,__ENDC])

## def __reduce_dots(path):
##     ret = re.sub('\w+/\.\./','',path)
##     if ret == path:
##         return ret
##     else
##         return __reduce_dots(ret)
    
## def ls(folder=''):
##     if '..' in folder:
##         pass
##     else:
##         tempList = gDirectory.GetListOfKeys() if folder=='' else gDirectory.Get(folder).GetListOfKeys()
##     retList = []
##     for it in range(0,tempList.GetSize()):
##         obj  = tempList.At(it).ReadObj()
##         name = obj.GetName()
##         if obj.InheritsFrom('TDirectory'):
##             name = __color(name,__BLUE)
##         if obj.InheritsFrom('TTree'):
##             name = __color(name,__Green)
            
##        retList.append()
##     return retList

## def cd(folder=''):
##     if isinstance(folder, TFile):
##         gDirectory = folder
##         __main_dir = folder
##         __PATH     = folder.GetName()+' :'
##     elif isinstance(folder, str):
        
##         gDirectory
##     tempList = __current_dir.GetListOfKeys() if dir=='' else __current_dir.Get(dir).GetListOfKeys()
##     retList = []
##     for it in range(0,tempList.GetSize()):
##         obj  = tempList.At(it).ReadObj()
##         name = obj.GetName()
##         if obj.InheritsFrom('TDirectory'):
##             name = __color(name,__BLUE)
##         if obj.InheritsFrom('TTree'):
##             name = __color(name,__Green)
            
##        retList.append()
##     return retList
