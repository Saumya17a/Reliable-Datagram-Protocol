# Reliable-Datagram-Protocol
RDP follows HTTP design, using full text, line-by-line control headers to establish (SYN) and release (FIN) connection, and
Sequence number in data (DAT) packet of PAYLOAD Length and Acknowledgment number in
acknowledgment (ACK) packet to reorder out-of-order packets, acknowledge received packets and identify lost
packets for retransmission. To be efficient, RDP cannot use stop-and-wait (i.e., transmit a packet, wait for
acknowledgment, and retransmit until it is received), and has to support flow control using Window size (i.e.,
multiple packets can be transmitted back-to-back within the Window, and lost packets will be recovered
through retransmission by timeout or three duplicate acknowledgments).
How to run RDP
python3 rdp.py ip_address port_number read_file_name write_file_name
on H1 will bind rdp to ip_address and port_number to send or receive UDP packets, and to transfer a file with
read_file_name from the RDP sender to receiver saved with write_file_name. After the file transfer is finished,
diff read_file_name write_file_name
on H1 can tell you whether the received file is different from the sent file of length greater than 10,240 bytes.
In addition to saving the received file for diff, RDP also outputs a log to the screen in the following format
DATE: EVENT; COMMAND; Sequence|Acknowledgment: Value; Length|Window: Value
where DATE is timestamp and EVENT := Send|Receive. For example,
Fri Oct 2 16:54:09 PDT 2020: Send; SYN; Sequence: 0; Length: 0
Fri Oct 2 16:54:09 PDT 2020: Receive; SYN; Sequence: 0; Length: 0
Fri Oct 2 16:54:09 PDT 2020: Send; ACK; Acknowledgment: 1; Window: 2048
Fri Oct 2 16:54:09 PDT 2020: Receive; ACK; Acknowledgment: 1; Window: 2048
Fri Oct 2 16:54:09 PDT 2020: Send; DAT; Sequence: 1; Length: 1024
Fri Oct 2 16:54:10 PDT 2020: Receive; DAT; Sequence: 1; Length: 1024
Fri Oct 2 16:54:10 PDT 2020: Send; ACK; Acknowledgment: 1025; Window: 1024
Fri Oct 2 16:54:10 PDT 2020: Receive; ACK; Acknowledgment: 1025; Window: 1024
Fri Oct 2 16:54:10 PDT 2020: Send; FIN; Sequence: 1025; Length: 0
Fri Oct 2 16:54:10 PDT 2020: Receive; FIN; Sequence: 1025; Length: 0
Fri Oct 2 16:54:10 PDT 2020: Send; ACK; Acknowledgment: 1026; Window: 2048
Fri Oct 2 16:54:10 PDT 2020: Receive; ACK; Acknowledgment: 1026; Window: 2048
