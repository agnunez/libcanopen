#!/usr/bin/python
import numpy as np 
from pycanopen import *
from txy import *
from ican import *
import sys,time

'''
  check for number of arguments or help
'''

if len(sys.argv) == 2:
    # get the node address from the first command-line argument
    node = int(sys.argv[1])
else:
    print("usage: %s NODE" % sys.argv[0])
    exit(1)

'''
  node init
'''

vendor,prodid,swver=init(node)
cls()
print("Info Node: %s VendorID: 0x%.8X ProductID: 0x%.8X SoftwareVer: 0x%.8X") % (node,vendor,prodid,swver)
time.sleep(2)  # show node found

nomcms,mcms = findmcms(node)
cls()
header("iCAN ACP TEST")

while 1:
  at(30,1, time.strftime("%a, %d %b %Y %H:%M:%S UT",  time.localtime()) ,tcolor.HEADER)
  for mcm in mcms:
    avg,noise,delta=mcmpos(node,mcm,200)
    at( 1,mcm+2,"MCM( ) Position:      ", tcolor.OKGREEN)
    at( 5,mcm+2,"%s" % mcm, tcolor.WARNING)
    at(17,mcm+2,"%2.5fv" % avg, tcolor.WARNING)
    at(26,mcm+2,"%2.5frms" % noise, tcolor.WARNING)
    gain = mcmgain(node, mcm)
    at(37,mcm+2,"Gain:      ", tcolor.OKGREEN)
    at(43,mcm+2,("%0d" % gain), tcolor.WARNING)
    offset = mcmoffset(node, mcm)
    at(49,mcm+2,"Offset:      ", tcolor.OKGREEN)
    at(57,mcm+2,("%0d" % offset), tcolor.WARNING)
    temp = mcmtemp(node, mcm)
    at(62,mcm+2,"Temp:      ", tcolor.OKGREEN)
    if (temp<40):
      at(68,mcm+2,("%2.1f" % temp), tcolor.WARNING)
    else:
      at(68,mcm+2,("N/A"), tcolor.WARNING)
    hum = mcmhumid(node, mcm)
    at(73,mcm+2,"Hum:        ", tcolor.OKGREEN)
    if (hum>-1):
      at(78,mcm+2,("%0d" % hum), tcolor.WARNING)
    else:
      at(78,mcm+2,("N/A"), tcolor.WARNING)
    at(82,mcm+2,"dt:        ", tcolor.OKGREEN)
    at(85,mcm+2,("%0d" % delta), tcolor.WARNING)

