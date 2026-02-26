#!/usr/bin/env python3
import os
import socket
import subprocess
import nbdkit

conn = None
addr = None
mc = None


def open(readonly):
	global conn,addr,mc
	nbdkit.debug("Opening")
	#Set up socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('localhost', 65300))

	# Start Minecraft
	mc = subprocess.Popen(["flatpak", "run", "org.prismlauncher.PrismLauncher", "-l", "Harder", "-w", "Flatland"])

	# Connect to Minecraft
	nbdkit.debug("Listening")
	server.listen(1)
	
	conn, addr = server.accept()
	nbdkit.debug("Connected")

	# Confirm Connection
	conn.send(b"Hello from NBD")
	response = conn.recv(1024)
	nbdkit.debug(f"Server said: {response.decode()}")
	return 1  # dummy handle

def get_size(h):
	#conn.send(b"SIZE")
	#conn.recv(3) # ACK
	return 51200 #conn.recv(1024).decode()

def pread(h, count, offset):
	conn.send(b"RD " + str(offset).encode() + b" " + str(count).encode())
	nbdkit.debug(f"sent read request for {count} bytes at offset {offset}")
	conn.recv(3) # ACK
	nbdkit.debug("received ack, reading")
	data = conn.recv(count)
	nbdkit.debug(f"read {len(data)} bytes")
	return data

def pwrite(h, buf, offset):
	conn.send(b"WR " + str(offset).encode() + b" " + str(len(buf)).encode())
	nbdkit.debug(f"sent write request for {len(buf)} bytes at offset {offset}")
	conn.recv(3) # ACK
	nbdkit.debug("received ack, writing")
	conn.send(buf)
	nbdkit.debug("sent write")
	conn.recv(3) # END
	nbdkit.debug("received end")
	return 

def close(h):
	conn.close()
	mc.terminate()
	
