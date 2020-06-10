import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 10000
server_address = (host, port)
print >>sys.stdout, 'Server is listening on port %d...' % port

sock.bind(server_address)
sock.listen(1)
print >>sys.stdout, 'Waiting for client...'

connection, client_address = sock.accept()
print >>sys.stdout, 'Client connected: ', client_address

try:
    n = 1
    while True:
        message_expected = '{:05d}'.format(n)
        message_received = ''
        bytes_received = 0
        bytes_expected = len(message_expected)
        while bytes_received < bytes_expected:
            data = connection.recv(bytes_expected - bytes_received)
            message_received = message_received + data
            bytes_received += len(data)

        if message_received == message_expected:
            n_plus_1 = int(message_received) + 1
            message_sent = '{:05d}'.format(n_plus_1)
            connection.sendall(message_sent)
            print >>sys.stdout, 'Message received: %s. Message sent: %s' % (message_received, message_sent)
        else:
            print >>sys.stdout, 'Ooops! Message received from the client %s differs from expected %s' % (message_received, message_expected)

        n = n + 1
finally:
    connection.close()
