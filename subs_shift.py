#!/usr/bin/env python

import re, os
from argparse import ArgumentParser
from pdb import set_trace

class TimeStamp(object):
    def __init__(self, stamp):
        values = tuple([float(i) for i in stamp.replace(',','.').split(':')])
        hrs, mins, secs = 0, 0, 0
        vlen = len(values)
        if vlen == 3:
            hrs, mins, secs = values
        elif vlen == 2:
            mins, secs = values
        else:
            secs = values[0]
        self.time = hrs*(60**2)+mins*60+secs

    def remap(self, fcn):
        self.time = fcn(self.time)

    @property
    def str(self):
        hrs  = int(self.time/(60**2))
        secs = self.time - hrs*(60**2)
        mins = int(secs/60)
        secs -= mins*60
        return ('%02d:%02d:%.3f' % (hrs, mins, secs)).replace('.',',')

    def __gt__(self, val):
        return self.time > val.time
    
    def __lt__(self, val):
        return self.time < val.time

    def __eq__(self, val):
        return self.time > val.time

__max_errs__ = 1
def str_match(inside, total, i1=0, i2=0, errs = 0):
    if errs > __max_errs__:
        return -1
    if i1 == len(inside):
        return 0 if errs > 0 else 1
    elif i2 == len(total):
        return -1
    ret = -1
    if inside[i1] == total[i2]:
        ret = max(ret, str_match(inside, total, i1+1, i2+1, errs))
    else:
        ret = max(ret
                  , str_match(inside, total, i1+1, i2+1, errs+1)
                  , str_match(inside, total, i1  , i2+1, errs+1)
                  )
    ret = max(ret, str_match(inside, total, 0, i2+1, 0))
    return ret
    
    
class Entry(object):
    def __init__(self, text):        
        lines = text.split('\n')
        times = [i.strip() for i in lines[1].split('-->')]
        self.start = TimeStamp(times[0])
        self.stop  = TimeStamp(times[1])
        self.text  = '\n'.join(lines[2:])
        self.tomatch = self.text.lower().replace('\n', ' ')

    def remap(self, fcn):
        self.start.remap(fcn)
        self.stop.remap(fcn)

    def __repr__(self):
        return '"%s" @ %s' % (self.tomatch, self.start.str)
    
    @property
    def string(self):
        return '%s --> %s\n%s' % (self.start.str, self.stop.str, self.text)

    def match(self, text, time, allow_errors=True):
        if allow_errors == False:
            if text in self.tomatch:
                return abs(time.time - self.start.time)
            else:
                return None
        if not allow_errors:
            __max_errs__ = 0
        idx = str_match(text, self.tomatch)
        __max_errs__ = 1
        delta = abs(time.time - self.start.time)
        if idx == -1:
            return None
        elif idx == 0:
            return -1*delta
        else:
            return delta

parser = ArgumentParser()
parser.add_argument('srt')
parser.add_argument('mapping', nargs='+', help='a line of text mapped to when it happens "here you are // 00:01:32", multiple mappings allowed')
parser.add_argument('--fitfunc', '-f', default='[0]*x+[1]', help='function to use when fitting')
parser.add_argument('--out', '-0', default='out.srt', help='output file')
args = parser.parse_args()
srt = open(args.srt).read().replace('\r','')

entries = [Entry(i) for i in srt.split('\n\n') if i]

points = []
for point in args.mapping:
    text, time_txt = tuple([i.strip() for i in point.split('//')])
    time = TimeStamp(time_txt)
    text = text.lower()
    #find corresponding entry
    all_matches = []
    for entry in entries:
        match = entry.match(text, time, False)
        if match is not None:
            all_matches.append((match, entry))

                
    to_use = None
    matches = [i for i in all_matches if i[0] > 0]
    if not matches:
        print '\n----- could not find entries corresponding to "%s" -----' % text
        ans = raw_input('look for possible mistakes? [yY/nN]')

        if ans.lower() == 'n':
            continue

        #repeat allowing errors
        for entry in entries:
            match = entry.match(text, time, True)
            if match is not None:
                all_matches.append((match, entry))

        if all_matches:
            all_matches.sort(key = lambda x: x[0], reversed=True)
            print "did you mean? "
            for i, j in enumerate(all_matches):
                _, entry = j
                print '[%d]' % i, entry
            idx = raw_input('which one should I use? (-1 to abort)')
            idx = int(idx)
            if idx == -1:
                print 'skipping...'
                continue
            _, to_use = matches[idx]
        else:
            print "Nothing found..."
            continue
    elif len(matches) == 1:
        _, to_use = matches[0]
    else:
        print 'multiple matches found for, "%s"' % text
        matches.sort(key = lambda x: x[0])
        for i, j in enumerate(matches):
            _, entry = j
            print '[%d]' % i, entry
        idx = raw_input('which one should I use? ')
        idx = int(idx)
        _, to_use = matches[idx]

    print to_use.start.str, '-->', time.str
    points.append((to_use.start.time, time.time))


#linear fit
from rootpy import ROOT
ROOT.gROOT.SetBatch()
from rootpy.plotting import Graph, F1, Canvas

fcn = F1(args.fitfunc)
graph = Graph(len(points))
for idx, point in enumerate(points):
    x, y = point
    graph.SetPoint(idx, x, y)
graph.fit(fcn)

canvas = Canvas()
graph.Draw()
canvas.SaveAs("shifts.png")

with open(args.out, 'w') as out:
    for i, entry in enumerate(entries):
        entry.remap(fcn)
        out.write('%d\n' % i)
        out.write('%s\n\n' % entry.string)
