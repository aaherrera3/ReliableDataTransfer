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
    f = open(input("FileName: "), 'rb')
    while True:
        data = f.read(PACKET_SIZE)
        if not data:
            break
        pkt = packet.make(seq,data)
        print("Sending seq# ", seq, "\n")
        udt.send(pkt, sock, RECEIVER_ADDR)
        seq = seq+1
        time.sleep(TIMEOUT_INTERVAL)
        receive_snw(sock,pkt)
    pkt = packet.make(seq, "END".encode())
    udt.send(pkt, sock, RECEIVER_ADDR)

# Send using GBN protocol
def send_gbn(sock):
    global num_sent_packets
    global num_resent_packets
    seq = 0
    packets = []
    start_time = time.time()
    f = open(input("File Name: "), 'rb')
    data = f.read(PACKET_SIZE)
    while data:
        pkt = packet.make(seq,data)
        packets.append(pkt)
        data = f.read(PACKET_SIZE)
        seq += 1
    pkt = packet.make(seq, "END".encode())
    packets.append(pkt)
    
    while packets:
        packetsSent = []
        for x in range(WINDOW_SIZE):
            pkt = packets.pop(0)
            packetsSent.append(pkt)
            udt.send(pkt, sock, RECEIVER_ADDR)
            num_sent_packets += 1
            time.sleep(TIMEOUT_INTERVAL)
        receive_gbn(sock,packetsSent)
    end_time = time.time()
    print("Total number of packets sent:", num_sent_packets, "\n")
    print("Number of packets resent:", num_resent_packets, "\n")
    print("Time taken to complete file transfer:", end_time - start_time, "seconds")
    return
        

# Receive thread for stop-n-wait
def receive_snw(sock, pkt):
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
    return

received_packets = []
current_ack = 0

# Receive thread for GBN
def receive_gbn(sock, sent):
    global received_packets
    global num_resent_packets
    global current_ack 
    sock.settimeout(0.5*50)
    acknowledged = len(sent)
    count = 0
    while count != acknowledged:
        try:
            for x in range(len(sent)):
                ACK, senderaddr = udt.recv(sock)
                ack, data = packet.extract(ACK)
                if ack not in received_packets and current_ack == ack:
                    print("Confirm seq#: ", ack, "\n")
                    received_packets.append(ack)
                    sent.remove(ACK)
                    current_ack += 1
                    count += 1
                
                
                
                    
        except socket.timeout:
            print("Resending")
            for x in sent:
                udt.send(x, sock, RECEIVER_ADDR)
                num_resent_packets += 1
    return


# Main function
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)

    # filename = sys.argv[1]
    send_gbn(sock)
    #send_snw(sock)
    sock.close()


