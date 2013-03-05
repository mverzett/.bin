#!/usr/bin/env python

import os
import glob
import sys
import re
import web_templates as templates

__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"
__doc__ = """Script to update the web-page to show pictures and dirs in a reasonable way"""

public_html = '/afs/hep.wisc.edu/home/%s/public_html/' % os.environ['USER']
def make_web_page(path):
    print 'building web page for path: ' + path
    objects = os.listdir(path)
    html    = open( os.path.join(path,'index.html'), 'w' )
    parent  = '' if path == public_html else '/'.join(path.replace(public_html,'').rstrip('/').split('/')[:-1])
    dirs    = filter(lambda x: os.path.isdir( os.path.join(path,x) ), objects)
    pics    = filter(lambda x: '.png' in x and x not in dirs, objects)
    tabs    = filter(lambda x: '.raw_txt' in x and x not in dirs and x not in pics, objects)
    rest    = filter(lambda x: x not in dirs and x not in pics and x not in tabs and x != 'index.html', objects)
    dir_html= '\n'.join( [templates.create_main_list_element(i) for i in dirs] )
    pic_html= '\n'.join( [templates.create_pic_list_element(i)  for i in pics] )
    tab_html= '\n'.join( [templates.create_tab_list_element(i, open(os.path.join(path,i)).read())  for i in tabs] )
    res_html= '\n'.join( [templates.create_file_list_element(i) for i in rest] )
    page    = templates.page_template.substitute(
	PARENT     = parent,
        PATH       = path.split('public_html')[1],
        DIR_LIST   = dir_html,
        PIC_LIST   = pic_html,
	TABLES     = tab_html,
        OTHER_LIST = res_html,
        )
    html.write(page)
    for d in dirs:
        make_web_page( os.path.join(path, d) )
        
make_web_page(public_html)
