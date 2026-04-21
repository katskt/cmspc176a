#!/usr/bin/env python3

# Include needed libraries. Do _not_ include any libraries not included with
# Python3 (i.e. do not use `pip`).
from socket import AF_INET, SOCK_STREAM, socket
import sys

BUFFER_SIZE = 4096
PASSWORD = 'password'

""" python3 pop3_read.py pigeon.cs.ucsb.edu 11000 alice@ucsb.edu """
# Parse command-line arguments.
host     = sys.argv[1]
port     = int(sys.argv[2])
username = sys.argv[3]

# Establish a TCP connection with the POP3 server.
s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))

# Read greeting from the server.
data = s.recv(BUFFER_SIZE)
response = data.decode('utf-8')

if not response.startswith('+OK'):
    raise Exception('+OK not received from server.')

# Note: the POP3 spec requires every command to end with \r\n, not just \n.

# Log in with USER and PASS commands.
s.send(f'USER {username}\r\n'.encode())

s.send(f'PASS {PASSWORD}\r\n'.encode())

s.send(f'LIST\r\n'.encode())


# Get the number of messages with the LIST command.
# Note: the LIST response spans multiple lines and ends with a line
# containing only '.'. Do not assume a fixed number of recv() calls will
# capture the full response — depending on the network, the entire response
# may arrive in a single recv() or be split across several. Accumulate data
# until you have seen the terminator.
# 1. get list of messages: ex. 
# 1 23
# 2 45
# 3 92
# .
buffer = ""
while True:
    response = s.recv(BUFFER_SIZE).decode('utf-8')
    buffer += response
    # stop reading when reach end
    if "\r\n.\r\n" in buffer:
        break

# splt the response into a list
inbox_num = buffer.split("\r\n")
# Retrieve and print each message with the RETR command.
# The same caveat about multi-line responses applies here.
# Print messages separated by a line containing only '---'.
poop = ""
for i in inbox_num:
    if i == ".":
        break
    if "+OK" in i:
        continue    
    if "X-" in i:
        continue
    i = i.split(" ")[0] # obtain the RETR numbers from list and RETR it. 
    s.send(f'RETR {i}\r\n'.encode())
    count = 0
    ak47 = ""
    while True: # get response
        response = s.recv(BUFFER_SIZE).decode('utf-8')
        ak47 += response
        poop += response
        if "\r\n.\r\n" in ak47:
            break
            
# display response pretty
poop = poop.split("\n")
for i in (poop):
    if "+OK" in i:
        continue    
    if "X-" in i:
        continue
    if i == ".\r":
        print("---")
    else:
        print(i)
    

# Close the socket when finished.
s.close()
