import socket
import sys
import argparse
import errno


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
        sock.settimeout(0.5)
        res = sock.connect_ex((target, port))
        print(res)
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = ""
        if res == 0:
            status = "open"
        elif (res == errno.EWOULDBLOCK) | (res == errno.EAGAIN):
            status = "filtered"
        return status, service
    except socket.error as msg:
        print("Connection failed to target %s at port %d: %s" % (target, port, msg))


if __name__ == '__main__':
    # print(errno.errorcode[10035])
    target, ports = parse_commands()
    for port in ports:
        res = get_connection(target, port)