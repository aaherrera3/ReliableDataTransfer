# receiver.py - The receiver in the reliable data transer protocol
import packet
import socket
import sys
import udt

RECEIVER_ADDR = ('localhost', 8080)

# Receive packets from the sender w/ GBN protocol
def receive_gbn(sock):
    # Fill here
    return


# Receive packets from the sender w/ SR protocol
def receive_sr(sock, windowsize):
    # Fill here
    return


# Receive packets from the sender w/ Stop-n-wait protocol
def receive_snw(sock):
   endStr = ''
   f = open("receiver_file_x.txt", "w")
   while endStr!='END':
        pkt, senderaddr = udt.recv(sock)
        seq, data = packet.extract(pkt)
        endStr = data.decode()
        if endStr != "END":
            f.write(endStr)
        print("From: ", senderaddr, ", Seq# ", seq,"Data ", endStr, "\n")
        pkt = packet.make(seq,data)
        udt.send(pkt, sock, senderaddr)


# Main function
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR)
    # filename = sys.argv[1]
    receive_snw(sock)

    # Close the socket
    sock.close()