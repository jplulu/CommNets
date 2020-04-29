import pyshark
from ipwhois import IPWhois

path_to_file = input("Enter path to .pcap file: ")
path_to_output = input("Enter path to output file: ")

filtered_cap = pyshark.FileCapture(path_to_file, display_filter='tls.handshake.type == 1')

outputs = set()
for packet in filtered_cap:
    try:
        obj = IPWhois(packet.ip.dst)
        res = obj.lookup_whois()
        organization = res["nets"][0]['description']
        output = '{}, {}, {}, {}\n'.format(packet.ip.src, packet.ip.dst, packet.tls.handshake_extensions_server_name,
                                           organization)
        outputs.add(output)
    except Exception:
        except_output = '{}, {}, {}, Organization not found\n'.format(packet.ip.src, packet.ip.dst,
                                                                      packet.tls.handshake_extensions_server_name)
        outputs.add(except_output)
        print(except_output)
        continue

f = open(path_to_output, "w")
for output in outputs:
    f.write(output)
