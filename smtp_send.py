#!/usr/bin/env python3

# Include needed libraries. Do _not_ include any libraries not included with
# Python3 (i.e. do not use `pip`).
from socket import AF_INET, SOCK_STREAM, socket
import sys

""" 
EXAMPLE:
python3 smtp_send.py pigeon.cs.ucsb.edu 2500 alice@ucsb.edu alice@ucsb.edu "Hello" < body.txt
"""
BUFFER_SIZE = 4096

def send_and_recv(cmd, expected):
    s.send(cmd.encode())
    resp = s.recv(BUFFER_SIZE).decode()
    if not resp.startswith(expected):
        raise Exception(f"Expected {expected}, got {resp}")
    return resp

# Parse command-line arguments.
host    = sys.argv[1]
port    = int(sys.argv[2])
from_addr = sys.argv[3]
to_addr   = sys.argv[4]
subject   = sys.argv[5]

# Read the email body from standard input.
body = sys.stdin.read()
# Establish a TCP connection with the SMTP server.
s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))


# Read greeting from the server.
data = s.recv(BUFFER_SIZE)
response = data.decode('utf-8')

if not response.startswith('220'):
    raise Exception('220 reply not received from server.')

# Note: the SMTP spec requires every command to end with \r\n, not just \n.
# This applies to commands (HELO, MAIL FROM, etc.) and to the message headers
# and body sent after DATA.

# Send HELO command and get server response.
send_and_recv('HELO client\r\n', '250')

# Send MAIL FROM command.
send_and_recv(f'MAIL FROM: <{from_addr}>\r\n', '250')


# Send RCPT TO command.
send_and_recv(f'RCPT TO: <{to_addr}>\r\n', '250')


# Send DATA command.
send_and_recv(f'DATA\r\n', '354')


# Send message headers and body.
s.send(f'Subject: {subject}\r\n'.encode())
s.send("\r\n".encode())
s.send(body.encode())

# End message with a line containing only a period.
s.send(f'\r\n.\r\n'.encode())

resp = s.recv(BUFFER_SIZE).decode()
if not resp.startswith("250"):
    raise Exception("Message Error")
# Send QUIT command.
send_and_recv(f'QUIT\r\n', '221')


# Close the socket when finished.
s.close()
