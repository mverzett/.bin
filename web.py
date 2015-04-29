#!/usr/bin/env python

import os
import glob
import sys
import re
import web_templates as templates
import host
from pdb import set_trace

__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"
__doc__ = """Script to update the web-page to show pictures and dirs in a reasonable way"""
from optparse import OptionParser

parser = OptionParser(description=__doc__)
parser.add_option('--columns-number', '-c', type=int, default = 1,
                  help='number of columns to be used to print the plots',dest='columns')
parser.add_option('--picsize', '-s', type=int, default = 640,
                  help='size in pixels of the pics',dest='psize')

options, dirs_to_map = parser.parse_args()
chunk_list = lambda l,n: [l[i:i+n] for i in range(0, len(l), n)]

def make_web_page(path):
    #print 'building web page for path: ' + path
    objects = os.listdir(path)
    if '.donotupdate' in objects:
        return
    html    = open( os.path.join(path,'index.html'), 'w' )
    parent  = '' if path == host.public_html else '/'.join(path.replace(host.public_html,'').rstrip('/').split('/')[:-1])
    dirs    = filter(lambda x: os.path.isdir( os.path.join(path,x) ), objects)
    pics    = filter(lambda x: '.png' in x and x not in dirs, objects)
    pics    = chunk_list(pics, options.columns)
    tabs    = filter(lambda x: '.raw_txt' in x and x not in dirs and x not in pics, objects)
    rest    = filter(lambda x: x not in dirs and x not in pics and x not in tabs and x != 'index.html', objects)
    dir_html= '\n'.join( [templates.create_main_list_element(i) for i in dirs] )
    pic_html= '\n'.join( [templates.create_pic_list_element(*i, size=options.psize)  for i in pics] )
    tab_html= '\n'.join( [templates.create_tab_list_element(i, open(os.path.join(path,i)).read())  for i in tabs] )
    res_html= '\n'.join( [templates.create_file_list_element(i) for i in rest] )
    page    = templates.page_template.substitute(
        HOME       = host.web_home,
        PARENT     = parent,
        PATH       = path.split(host.root_dir)[1],
        DIR_LIST   = dir_html,
        PIC_LIST   = pic_html,
        TABLES     = tab_html,
        OTHER_LIST = res_html,
        )
    html.write(page)
    for d in dirs:
        make_web_page( os.path.join(path, d) )

if len(dirs_to_map):
    for i in dirs_to_map:
        make_web_page(i)
else:
    make_web_page(host.public_html)
