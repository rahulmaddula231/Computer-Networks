from socket import *
import os
import sys
import array
import struct
import time
import select
import signal
import binascii
from ICMPChecksum import ICMPchecksum
icmpechotype= 8
imcpechotype1=0

def sPing(s, destinationaddress, Identifier):
    Initalchecksumvalue = 0
    dsend='HI LOCAL SERVER'
    Packetheader = struct.pack("bbHHh", icmpechotype, 0, Initalchecksumvalue, Identifier, 1)
    timetakenforpacket=time.time()
    payloadportion = struct.pack("d248s", timetakenforpacket,dsend.encode())
    Initalchecksumvalue = ICMPchecksum(Packetheader + payloadportion)
    if sys.platform == 'darwin':
        Initalchecksumvalue = htons(Initalchecksumvalue) & 0xffff
    Packetheader = struct.pack("bbHHh", icmpechotype, 0, Initalchecksumvalue, Identifier, 1)
    totalICMPpacket = Packetheader + payloadportion
    s.sendto(totalICMPpacket, (destinationaddress, 0))
    print("Client sent requests to Server Successfully !!!")

def rPing(s, number, timetakenforpacket):
    strb = 248
    dsend='HI LOCAL SERVER'
    b = struct.calcsize("d")
    Servertimetaken = time.time()
    while True:
        packetrecieved, addr = s.recvfrom(1024)
        tr = time.time()
        packetheader = packetrecieved[20:28]
        typeoficmp, codeonicmpheader, icmpchecksum, identifier, sequencenumber = struct.unpack("bbHHh", packetheader)
        if identifier == number and typeoficmp != 8:
            senttimerequest = struct.unpack("d", packetrecieved[28:36])[0]
            ICMPpacketpayload = struct.unpack("d", packetrecieved[36:36 + b])[0]
            print("Requests received by server from client Successfully !!!")
            #ICMPpacketpayload=ICMPpacketpayload.decode()
            print('Time taken to sent requests from local client to local server '+str(senttimerequest)+ ' ms')
            print('Time taken to sent replies from local server to local client '+str(senttimerequest)+' ms')
            print('Time Delay '+str(tr - senttimerequest)+' ms')
            OUTPUTtextfile=open('ICMPPINGOUTPUT.txt','a')
            print('Time Taken to sent requests from local client to local server in ms',senttimerequest,file=OUTPUTtextfile)
            print('Time Taken to sent replies from local server to local client in ms',tr,file=OUTPUTtextfile)
            print('The ICMP MESSAGE TIME DELAY is:', tr - senttimerequest, file=OUTPUTtextfile)
            print('The Message',dsend,file=OUTPUTtextfile)
        amountoftimeremaining = time.time() - Servertimetaken
        break
        if amountoftimeremaining >=9:
            return "Request timed out."

def ICMPPINGING():
    icmp = getprotobyname("icmp")
    s = socket(AF_INET, SOCK_RAW, icmp)
    ICMPidentifier = os.getpid() & 0xFFFF
    Counter = 0
    while True:
        OUTPUTtextfile=open('ICMPPINGOUTPUT.txt','a')
        if Counter==1:
            print(' ')
            print(' ')
        print('Pinging starts for '+str(Counter+1)+' th ICMP Request')
        print('**********************************************************************************',file=OUTPUTtextfile)
        print('Pinging starts for '+str(Counter+1)+' th ICMP Request',file=OUTPUTtextfile)
        print('Client sending requests to local server')
        time.sleep(2)
        server='localhost'
        #server='www.google.com'
        #server='www.cisco.com'
        localserver = server
        if (localserver == "1"):
            s.close()
            exit()
        destinationaddress = gethostbyname(localserver)
        print('The Local Server',destinationaddress,file=OUTPUTtextfile)
        OUTPUTtextfile.close()
        print('Sending '+str(Counter+1)+' ICMP message of Size 256 Bytes in data to ',destinationaddress)
        time.sleep(2)
        sPing(s, destinationaddress, ICMPidentifier)
        rPing(s, ICMPidentifier, timeout)
        time.sleep(2)
        Counter = Counter + 1
        if Counter>1:
            exit(0)
ICMPPINGING()
