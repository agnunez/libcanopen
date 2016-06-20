#!/usr/bin/python
debug=False

import sys, time, math
if not debug:
  from pycanopen import *

'''
 CAN specific
'''
try:
  canopen = CANopen()
except:
  print "Error 0: CANopen construct failed"

def rx(node,address,data):
  return canopen.SDOUploadExp(node, address, data)

def pos(node,mcm):
  return canopen.SDOUploadExp(node, 0x6401, mcm)

def mcmgain(node,mcm):
  if debug:
    return 5300
  else:
    return rx(node, 0x6411, mcm)

def mcmoffset(node,mcm):
  if debug:
    offset=0
  else:
    return rx(node, 0x6411, mcm+6)

def mcmtemp(node,mcm):
  if debug:
    return 23
  else:
    return rx(node, 0x6404, mcm)

def mcmhumid(node,mcm):
  if debug:
    return 50
  else:
    return rx(node, 0x6404, mcm+6)

def init(node):
  if debug:
    return 0,0,0
  else: 
    vendor = rx(node, 0x1018, 0x01)
    prodid = rx(node, 0x1018, 0x02)
    swver  = rx(node, 0x1018, 0x03)
    return vendor,prodid,swver

def findmcms(node):
  '''
  count number of MCM with
  rs-canopen-sdo-upload can-interface NODE INDEX SUBINDEX
  '''
  mcms=[]                                         # create an empty list of MCM's
  nomcm = 0
  if debug:
    nomcm = 6
    for i in range(6):
      mcms.append(i+1)
    print "mcms: ",mcms
  else:
    try:
      mcmmask = rx(node, 0x2020, 0x00)           # mask with no. of MCM's connected and items position
      nomcm = (mcmmask & 0b11100000000) >> 8     # number of MCM's
      for i in range (1,7):
        if ((mcmmask & (1 << (i-1))) >> (i-1)): 
          mcms.append(i)
      print "No. MCM's: %s" % nomcm
    except:
      print "Wrong number of MCM's"
  return nomcm, mcms

def rms(buffer):
  result=0.0
  size=len(buffer)
  for i in buffer:
    result+=i*i
  return math.sqrt(result/size)

def sgn(i):
  if (i > 32767): i-=65536
  return i

def rmspos(node,mcm,samples):
  t0 = time.time()
  delta = 0
  pos = []
  noise = []
  avg= 0.0
  if debug:
    pos = 1.25+0.001*np.clip(np.random.randn(samples,1), -4.0, 4.0)
    avg= np.average(pos)
    time.sleep(0.0004*samples)
    t1 = time.time()
    time.sleep(0.0044)
    t1 = time.time()
    delta += (t1-t0)
  else:
    for i in range(0,samples):
      position = sgn(canopen.SDOUploadExp(node, 0x6401, mcm))
      position = ((float(position)+32768.)/65635.*2.5)
      avg+=position
      pos.append(position)
      time.sleep(0.0044)
      t1 = time.time()
      delta += (t1-t0)
      t0=t1
    avg/=samples
  delta = delta / samples
  for i in range(0,samples):
    noise.append(pos[i]-avg)
  t1 = time.time()
  return avg,rms(noise),delta
