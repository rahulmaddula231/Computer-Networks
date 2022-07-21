from collections import Counter
from socket import *
import os
import sys
import array
import struct
import time
import select
import signal
import binascii
def ICMPchecksum(ICMPPacket):
    if (len(ICMPPacket) % 2):
        ICMPPacket += "\x00"
    Transform= array.array("H", ICMPPacket)
    if sys.byteorder == "big":
        Transform.bytewap()
    evaluatev = sum(Transform)
    evaluatev &= 0xffffffff  
    while (evaluatev >> 16):
        evaluatev = (evaluatev & 0xFFFF) + (evaluatev >> 16)  
    resultval = ~evaluatev & 0xffff  
    resultval = resultval >> 8 | (resultval << 8 & 0xff00)
    return resultval