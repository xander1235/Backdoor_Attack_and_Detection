#!/usr/bin/env python example is focused on the fields in the Ethernet Frame and IP packet

import dpkt
import datetime
import socket
from dpkt.compat import compat_ord
from page2 import page2

def mac_addr(address):
	return ':' .join('%02x' % compat_ord(b) for b in address)

def inet_to_str(inet):
	try:
		return socket.inet_ntop(socket.AF_INET, inet)
	except ValueError:
		return socket.inet_ntop(socket.AF_INET6, inet)

def print_packets(pcap):
	scount,ncount,gcount,prev,ser,start,q,tot,timeprev,time,inter,numt = 0,0,0,0,0,0,0,0,0,0,0,0
	Line1=[]
	Line2=[]
	Line3=[]
	list1=[]
	list2=[]
	time1=[]
	time2=[]

	for timestamp, buf in pcap:
		eth = dpkt.ethernet.Ethernet(buf)
		list1.append(eth)
		time1.append(timestamp)
		time2.append(timestamp)
		list2.append(eth)
		ncount+=1
		
	
	for k in range(ncount):
		eth=list1.pop(0)
		time=time1.pop(0)
		ser+=1
		if not isinstance(eth.data, dpkt.ip.IP):
			continue
		ip = eth.data
		do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
		more_fragments = bool(ip.off & dpkt.ip.IP_MF)
		fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
		
		if ip.len <= 60:
			scount += 1
			if (k-prev) > 1:
				gcount += 1
			
			if (k-prev) == 1:
				inter += 1
				if (time-timeprev) > 0.1 and (time-timeprev) < 2 :
					numt += 1
			prev = k
		
		timeprev =time

		if ser%8==0:
			t = (scount - gcount - 1)/8
			if inter==0:
				inter=1
			alpha = numt/inter
			if t < 0.2 and alpha > 0.2:
				print('no')
			else:
				end = ser
				scount,gcount,inter,numt,prev,i = 0,0,0,0,0,0
				q=q+8
				for i in range(8):
					eth=list2.pop(0)
					timestamp=time2.pop(0)
					if not isinstance(eth.data, dpkt.ip.IP):
						continue
					ip = eth.data
					do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
					more_fragments = bool(ip.off & dpkt.ip.IP_MF)
					fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
					if ip.len <= 60:
						tot+=1
						s = str(tot)+'  '+'Source-IP: '+str(inet_to_str(ip.src))+'  '+'Dest-IP: '+str(inet_to_str(ip.dst))+'  '+'Len: '+str(ip.len)+'  '+'TTL: '+str(ip.ttl)+'  '+'DM: '+str(do_not_fragment)+'  '+'MF: '+str(more_fragments)+'  '+'Frag_offset: '+str(fragment_offset)
						Line1.append(s)
						s = '    TimeStamp: '+str(datetime.datetime.utcfromtimestamp(timestamp))
						Line2.append(s)
						s=  '    Source-MAC: '+str( mac_addr(eth.src))+'  '+'Dest-MAC: '+str(mac_addr(eth.dst))+'  '+'Eth-Type: '+str(eth.type)
						Line3.append(s)

	
	ncount=ncount-q			
	if ncount > 0:
		t = (scount - gcount - 1)/(ncount)
		if inter==0:
			inter=1
		alpha = numt/inter
		if t < 0.2 and alpha > 0.2:
			print('no')
		else:
			for i in range(ncount):
				eth=list2.pop(0)
				timestamp=time2.pop(0)
				if not isinstance(eth.data, dpkt.ip.IP):
					continue
				ip = eth.data
				do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
				more_fragments = bool(ip.off & dpkt.ip.IP_MF)
				fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
				if  ip.len<60:
					tot+=1
					s = str(tot)+'  '+'Source-IP: '+str(inet_to_str(ip.src))+'  '+'Dest-IP: '+str(inet_to_str(ip.dst))+'  '+'Len: '+str(ip.len)+'  '+'TTL: '+str(ip.ttl)+'  '+'DM: '+str(do_not_fragment)+'  '+'MF: '+str(more_fragments)+'  '+'Frag_offset: '+str(fragment_offset)
					Line1.append(s)
					s = '    TimeStamp: '+str(datetime.datetime.utcfromtimestamp(timestamp))
					Line2.append(s)
					s=  '    Source-MAC: '+str( mac_addr(eth.src))+'  '+'Dest-MAC: '+str(mac_addr(eth.dst))+'  '+'Eth-Type: '+str(eth.type)
					Line3.append(s)

	page2(tot,Line1,Line2,Line3)
	

def test(F):
	with open(F, 'rb') as f:
		pcap = dpkt.pcap.Reader(f)
		print_packets(pcap)
	
		
if __name__ == '__main__':
	test(F)
