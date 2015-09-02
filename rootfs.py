#! /bin/env python

import argparse
import os
from pdb import set_trace

parser = argparse.ArgumentParser('rootfs is a way to treat root files like a normal file system. paths are structured as filename.root:internal/path')
subparsers = parser.add_subparsers()

def parse_path(rpath):
   return tuple(rpath.split(':'))

def open_mode(tfname):
   return 'update' if os.path.isfile(tfname) else 'create'

def cp(args):
   def rcp(source, target, target_name, recursive):
      new_target = None
      if source.InheritsFrom('TDirectory'):
         #do not copy the dir, just make a new one and 
         #keep the pointer for possible recursive use
         new_target = target.mkdir(target_name)
      else:
         target.WriteTObject(
            source,
            target_name
            )
      if recursive and source.InheritsFrom('TDirectory'):
         for key in source.GetListOfKeys():
            name = key.GetName()
            new_src = key.ReadObj()
            rcp(new_src, new_target, name, recursive)

   tfname, tobj_path = parse_path(args.source)
   source_file = ROOT.TFile.Open(tfname)
   source_obj  = source_file.Get(tobj_path)

   tfname, tobj_path = parse_path(args.target)
   mode = open_mode(tfname) 
   target_file = ROOT.TFile.Open(tfname, mode)
   target_dir_name = os.path.dirname(tobj_path)
   target_name = os.path.basename(tobj_path)
   target_dir = target_file.Get(target_dir_name) if target_dir_name else target_file
   
   rcp(source_obj, target_dir, 
       target_name if target_name != '.' else source_obj.GetName(),
       args.recursive)
   source_file.Close()
   target_file.Close()

parser_cp = subparsers.add_parser('cp', help='copies within the file or to a new file')
parser_cp.add_argument('source')
parser_cp.add_argument('target')
parser_cp.set_defaults(op=cp)
parser_cp.add_argument('-r', action='store_true', dest='recursive', help='copy recursive')

def mkdir(args):
   tfname, tobj_path = parse_path(args.target)
   target_file = ROOT.TFile.Open(
      tfname,
      open_mode(tfname)
      )
   target_file.mkdir(tobj_path)
   target_file.Close()

parser_mkdir = subparsers.add_parser('mkdir', help='creates a directory tree in a file')
parser_mkdir.add_argument('target')
parser_mkdir.set_defaults(op=mkdir)

def rm(args):
   tfname, tobj_path = parse_path(args.target)
   target_file = ROOT.TFile.Open(
      tfname,
      open_mode(tfname)
      ) 
   target_dir_name = os.path.dirname(tobj_path)
   target_name = os.path.basename(tobj_path)
   target_dir = target_file.Get(target_dir_name) if target_dir_name else target_file
   target_dir.Delete(target_name)
   target_file.Close()

parser_rm = subparsers.add_parser('rm', help='removes the object from the file. DOES NOT FREE DISK SPACE! Because REASONS!')
parser_rm.add_argument('target')
parser_rm.set_defaults(op=rm)
#parser_rm.add_argument('-r', action='store_true', dest='recursive', help='recursive')

args = parser.parse_args()
import ROOT

args.op(args)
