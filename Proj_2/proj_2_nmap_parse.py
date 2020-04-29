import pyshark
import socket

path_to_file = input("Enter path to .pcap file: ")

filtered_cap = pyshark.FileCapture(path_to_file, display_filter='ip.src == 192.241.168.54 && tcp')

open_ports = set()
for packet in filtered_cap:
    open_ports.add(int(packet.tcp.srcport))
filtered_cap.close()

filtered_ports = set()
cap = pyshark.FileCapture(path_to_file, display_filter='ip.dst == 192.241.168.54 && tcp')
for packet in cap:
    if int(packet.tcp.dstport) in open_ports:
        continue
    else:
        filtered_ports.add(int(packet.tcp.dstport))

print('PORT\tSTATE\tSERVICE')
for port in open_ports:
    print(f"{port}\topen\t{socket.getservbyport(port)}")

for port in filtered_ports:
    print(f"{port}\tfiltered\t{socket.getservbyport(port)}")
