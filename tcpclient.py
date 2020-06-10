import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = sys.argv[1]
port = 10000
server_address = (host, port)
print >>sys.stderr, 'Connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    n = 1
    while True:
        message_sent = '{:05d}'.format(n)
        message_expected = '{:05d}'.format(n + 1)
        message_received = ''
        sock.sendall(message_sent)

        bytes_received = 0
        bytes_expected = len(message_expected)
        while bytes_received < bytes_expected:
            data = sock.recv(bytes_expected - bytes_received)
            message_received = message_received + data
            bytes_received += len(data)

        if message_expected == message_received:
            print >>sys.stdout, 'Message sent: %s. Message received: %s.' % (message_sent, message_received)
            n = n + 1
            if n == 99999:
                print >>sys.stdout, 'Client is terminating...'
                exit(0)
        else:
            print >>sys.stderr, 'Ooops! Message received from the server %s differs from expected %s' % (message_received, message_expected)

        time.sleep(3)
finally:
    sock.close()
