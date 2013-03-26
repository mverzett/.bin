#! /usr/bin/env python

import os
import glob
import sys
import subprocess
import time

if len(sys.argv) < 4:
    print "Usage: hierarchicalHadd.py [output name] [sources (must be a string!)] [files per chunck]"
    sys.exit(0)

#print sys.argv
cwd = os.getcwd()+'/'
in_endfname = cwd+sys.argv[-3]
in_sources = glob.glob(cwd+sys.argv[-2])
in_filesperjobs = int(sys.argv[-1])

if not os.environ.has_key('CMSSW_BASE'):
    print 'cms environment not set! running cmsenv'
    subprocess.call(['cmsenv'])

if not os.environ.has_key('CMSSW_BASE'):
    print 'impossible to set cms environment, exiting...'
    sys.exit(0)

chunk_list = lambda l,n: [l[i:i+n] for i in range(0, len(l), n)]

def hierarchicalHadd(endfname,sources,filesperjobs,level=1):
    #chunks the files in groups of n
    chunkedSources = chunk_list(sources,filesperjobs)
    print "hierarchicalHadd: level: %s # of chunks: %s" % (level,len(chunkedSources))
    counter = 0
    processes = []
    #runs hadd on every chunk
    for chunk in chunkedSources:
        chunkName = endfname.replace('.root','_chunk_%s_lv_%s.root' % (counter,level))
        command = ['hadd',chunkName]
        command.extend(chunk)
        #print command
        #subprocess.call(command)
        #parallels hadd
        processes.append(subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        counter+=1
        #limiter to four processes running at the same time
        while len(processes)  == 4:
            time.sleep(5)
            #filter out unfinisced processes
            processes = filter(lambda p: p.poll() == None, processes)

    #waits the last processes to finish
    for p in processes:
        p.wait()
    #checks the output files
    outFiles = glob.glob( endfname.replace('.root','_chunk_*_lv_%s.root' % level) )
    #if the files are temporary (mid way between beginning and end) deletes the sources
    if len(outFiles) >= 1 and level > 1:
        command = ['rm']
        command.extend(sources)
        subprocess.call(command)
    #increases the level, if more then one output file is produced runs the function on the output
    level+=1
    if len(outFiles) > 1:
        hierarchicalHadd(endfname,outFiles,filesperjobs,level)
    elif len(outFiles) == 1:
        subprocess.call(['mv',outFiles[0],endfname])
    else:
        return sys.exit(-1)


hierarchicalHadd(in_endfname,in_sources,in_filesperjobs)
