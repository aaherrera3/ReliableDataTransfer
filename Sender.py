import socket
import sys
# import _thread
import time
import string
import packet
import udt
import random
from timer import Timer


# Some already defined parameters
PACKET_SIZE = 512
RECEIVER_ADDR = ('localhost', 8080)
SENDER_ADDR = ('localhost', 9090)
SLEEP_INTERVAL = 0.05 # (In seconds)
TIMEOUT_INTERVAL = 0.5
WINDOW_SIZE = 4
num_sent_packets = 0
num_resent_packets = 0

# You can use some shared resources over the two threads
# base = 0
# mutex = _thread.allocate_lock()
# timer = Timer(TIMEOUT_INTERVAL)

# Need to have two threads: one for sending and another for receiving ACKs

# Generate random payload of any length
def generate_payload(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str


# Send using Stop_n_wait protocol
def send_snw(sock):
    seq = 0
    global num_sent_packets
    global num_resent_packets
    start_time = time.time()
    f = open(input("FileName: "), 'rb')
    while True:
        data = f.read(PACKET_SIZE)
        if not data:
            break
        pkt = packet.make(seq,data)
        print("Sending seq# ", seq, "\n")
        udt.send(pkt, sock, RECEIVER_ADDR)
        num_sent_packets += 1
        seq = seq+1
        time.sleep(TIMEOUT_INTERVAL)
        receive_snw(sock,pkt)
    pkt = packet.make(seq, "END".encode())
    udt.send(pkt, sock, RECEIVER_ADDR)
    num_sent_packets += 1
    end_time = time.time()
    print("Total number of packets sent:", num_sent_packets, "\n")
    print("Number of packets resent:", num_resent_packets, "\n")
    print("Time taken to complete file transfer:", end_time - start_time, "seconds")

# Send using GBN protocol
def send_gbn(sock):

    return

# Receive thread for stop-n-wait
def receive_snw(sock, pkt):
    global num_resent_packets
    sock.settimeout(0.5)
    acknowledged = False
    while not acknowledged:
        try:
            ACK, senderaddr = udt.recv(sock)
            ack, data = packet.extract(ACK)
            print("Confirm seq#: ", ack, "\n")
            acknowledged = True
        except socket.timeout:
            print("Resending")
            udt.send(pkt, sock, RECEIVER_ADDR)
            num_resent_packets += 1
    return



# Receive thread for GBN
def receive_gbn(sock):
    # Fill here to handle acks
    return


# Main function
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)

    # filename = sys.argv[1]

    send_snw(sock)
    sock.close()