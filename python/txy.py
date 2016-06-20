#!/usr/bin/python

import sys

def sgn(i):
  if (i > 32767): i-=65536
  return i

def color(c):
   lu=15  #   Range of colors for look up table
   if c<0: c=0
   if c>lu: c=lu
   blut=[40,44,104,100,42,102,46,106,47,107,103,105,101,43,45,41]
   flut=[39,39,39,39,39,39,39,39,30,30,30,30,30,30,30,30]
  #       0  1   2  3  4   5  6  7  8  9  10  11 12   13  14  15
   return '\033[%sm\033[%sm' % (blut[c],flut[c])

class tcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def at(x, y, text, color=''):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, color + text))
     sys.stdout.flush()

def cls():
  sys.stderr.write("\x1b[2J\x1b[H")  # Clear screen

def header(title):
  at(0,0, title, tcolor.OKGREEN)

def psplit(data):
  i=0
  for line in data:
    print "%s: %s" % (i,line)
    i+=1

