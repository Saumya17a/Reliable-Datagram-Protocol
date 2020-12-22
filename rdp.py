from socket import *
import sys
import datetime
import os
def gdt():
    return datetime.datetime.now().strftime('%a %b %d %H:%M:%S PDT %Y')

def connection_start():
    syn = f"SYN\r\nSequence: 0\r\nLength: 0\r\n\r\n"
    ack_start = f"ACK\r\nAcknowledgement: 1\r\nWindow: {window_receive}\r\n\r\n"
    sock.sendto(syn.encode(),address)
    print(f"{gdt()}: Send; SYN; Sequence: 0; Length: 0")
    while(1):
        data,addr = sock.recvfrom(2000000)
        header = data.decode("utf-8").split("\r\n")[0]
        if(header == "SYN"):
            print(f"{gdt()}: Receive; SYN; Sequence: 0; Length: 0")
            sock.sendto(ack_start.encode(),address)
            print(f"{gdt()}: Send; ACK; Acknowledgement: {1}; Window: {window_receive}")
        break
    while(1):
        data,addr  = sock.recvfrom(2000000)
        header = data.decode("utf-8").split("\r\n")[0]
        if(header == "ACK"):
            print(f"{gdt()}: Receive; ACK; Acknowledgement: {1}; Window: {window_receive}")
        break
#----------------------------------------------------------------------------------------
def connection_end():
#     print("In")
    end_seq = ack1
    end_ack = ack1 + 1
    fin = f"FIN\r\nSequence: {end_seq}\r\nLength: 0\r\n\r\n"
    ack_end = f"ACK\r\nAcknowledgement: {end_ack}\r\nWindow: {window_receive}\r\n\r\n"
    sock.sendto(fin.encode(),address)
    print(f"{gdt()}: Send; FIN; Sequence: {end_seq}; Length: 0")
    while(1):
        data,addr = sock.recvfrom(2000000)
        header = data.decode("utf-8").split("\r\n")[0]
        if(header == "FIN"):
            print(f"{gdt()}: Receive; FIN; Sequence: {end_seq}; Length: 0")
            sock.sendto(ack_end.encode(),address)
            print(f"{gdt()}: Send; ACK; Acknowledgement: {end_ack}; Window: {window_receive}")
        break
    while(1):
        data,addr  = sock.recvfrom(2000000)
        header = data.decode("utf-8").split("\r\n")[0]
        if(header == "ACK"):
            print(f"{gdt()}: Receive; ACK; Acknowledgement: {end_ack}; Window: {window_receive}")
        break
        
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_all_packets_sent():
    s = f.read(1)
    if s == b'':
        return True
    else:
        f.seek(-1,os.SEEK_CUR)
        return False
    
#-----------------------------------------------------------------------------------
""" Setup"""
host = str(sys.argv[1])
port = int(sys.argv[2])
address = ("10.10.1.100", 8888)
source = str(sys.argv[3])
destination = str(sys.argv[4])
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((host, port))
buffer  = []   #list of sequence number as per order of sending  
window_send = 2048
window_receive = 2048
recd_packets = []
f = open(source,"rb")
d = open(destination, "w")
seq ,ack= 1, 0
payload_length = 0
connection_start()
done_sending = False
#-----------------------------------------------------------------------------------------
while(1):
    if(len(buffer) == 0 and done_sending == True):
        break
        
    if(window_send > 0 and done_sending == False):
#         print("Here")
        if(check_all_packets_sent() == False):
            p = f.read(1024)
            text  = p.decode("utf-8")
            payload_length = len(p)
            packet = f"DAT\r\nSequence: {seq}\r\nLength: {len(p)}\r\n\r\n{text}\r\n\r\n"
            buffer.append(seq)       
            sock.sendto(packet.encode(),address)
            window_send -= len(p)
            print(gdt()+": Send DAT; Sequence: " + str(seq) +" Length: "+str(len(p)))
            seq += len(p)

        else:
            done_sending = True
            
    else:
        while(True):
            if len(recd_packets) == 0:
                data, addr = sock.recvfrom(200000000)
                recd_packets += data.decode("utf-8").split("\r\n\r\n")
#                 print(recd_packets)
                recd_packets.pop()
            packet = recd_packets.pop(0)
            header = packet.split("\r\n")[0]
#             print("Up")
            if(header == "DAT"):
                content =  recd_packets.pop(0)
                recv_seq = int(packet.split("\r\n")[1].split(": ")[1])
                recv_length = int(packet.split("\r\n")[2].split(": ")[1])
#                 print(recv_length)
                if(recv_seq == buffer[0]):
                    print(f"{gdt()}: Receive; DAT; Sequence: {recv_seq}; Length: {recv_length}")
                    ack = recv_seq + recv_length
                    window_receive -=  recv_length
                    ack_packet = f"ACK\r\nAcknowledgement: {ack}\r\nWindow: {window_receive}\r\n\r\n"
                    sock.sendto(ack_packet.encode(), address)
                    print(f"{gdt()}: Send; ACK; Acknowledgement: {ack}; Window: {window_receive}")
                    d.write(content)
                    window_receive += recv_length
                    buffer.pop(0)
#                     print("Again")
            else:
                ack1 = int(packet.split("\r\n")[1].split(": ")[1])
                window1 = int(packet.split("\r\n")[2].split(": ")[1])
                window_send = window1
#                 print(recv_seq, ack1,window1)
                print(f"{gdt()}: Receive ACK; Acknowledgement:{ack1} Window;{window1}")
                if seq == ack1:
                    break
f.close()
d.close()
connection_end()