import pyshark
import argparse
import socket
import subprocess
import time


def parse_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("ports")
    args = parser.parse_args()
    ports = [int(x) for x in args.ports.split(',')]
    return args.target, ports


def get_connection(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sock.settimeout(1)
        sock.connect_ex((target, port))
    except socket.error as msg:
        print("Connection failed to target %s at port %d: %s" % (target, port, msg))


if __name__ == '__main__':
    file_name = "tmp.pcap"
    target, ports = parse_commands()
    command = ["tshark", "-i", "3", "-w", f"{file_name}", "-a", f"duration:{len(ports)}"]
    subprocess.Popen(command)
    time.sleep(1.5)

    for port in ports:
        get_connection(target, port)

    ip_addr = socket.gethostbyname(target)
    filtered_cap = pyshark.FileCapture(file_name, display_filter=f'ip.src == {ip_addr} && tcp')
    open_ports = set()
    for packet in filtered_cap:
        open_ports.add(int(packet.tcp.srcport))
    filtered_cap.close()

    filtered_ports = set()
    cap = pyshark.FileCapture(file_name, display_filter=f'ip.dst == {ip_addr} && tcp')
    for packet in cap:
        if int(packet.tcp.dstport) in open_ports:
            continue
        else:
            filtered_ports.add(int(packet.tcp.dstport))
    cap.close()

    print('PORT\tSTATE\tSERVICE')
    for port in open_ports:
        print(f"{port}\topen\t{socket.getservbyport(port)}")

    for port in filtered_ports:
        print(f"{port}\tfiltered\t{socket.getservbyport(port)}")
