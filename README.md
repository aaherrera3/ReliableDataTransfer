# ReliableDataTransfer
The goal of this assignment is to implement both non-pipelined and pipelined versions of the reliable data transfer protocol: (1) Stop-and-wait (SnW) protocol and (2) Go-Back-N (GBN) Protocol.

# Stop-and-Wait
1) In a terminal run the Receiver.py 
    1.1)make sure to uncomment out the send_snw(sock) and comment the send_GBN(sock) in main
2) In a difrent terminal run Sender.py
    1.1)make sure to uncomment out the send_snw(sock) and comment the send_GBN(sock) in main
3) once Sender.py is running it will ask for the name of the file to send input it in the terminal.
    3.1) Make sure the name of the file is correct before submitting it. 
4) In the end both processes will terminate and in the sender side you will see how many files where sent and how many had to be resent. You will also see the time it took to complete the sent. 

# Go-Back-N
1) In a terminal run the Receiver.py 
    1.1)make sure to comment out the send_snw(sock) and uncomment the send_GBN(sock) in main
2) In a difrent terminal run Sender.py
    2.1)make sure to comment out the send_snw(sock) and uncomment the send_GBN(sock) in main
3) once Sender.py is running it will ask for the name of the file to send input it in the terminal.
    3.1) Make sure the name of the file is correct before submitting it. 
4) In the end both processes will terminate and in the sender side you will see how many files where sent and how many had to be resent. You will also see the time it took to complete the sent. 
