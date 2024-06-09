import re
import socket

from roku import Roku


def find_roku_device_lan():
    SSDP_ADDR = "239.255.255.250"
    SSDP_PORT = 1900
    SSDP_MX = 1
    SSDP_ST = "roku:ecp"

    # Send SSDP discovery message
    msg = "\r\n".join(
        [
            "M-SEARCH * HTTP/1.1",
            "HOST: %s:%d" % (SSDP_ADDR, SSDP_PORT),
            'MAN: "ssdp:discover"',
            "MX: %d" % SSDP_MX,
            "ST: %s" % SSDP_ST,
            "",
            "",
        ]
    ).encode("utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (SSDP_ADDR, SSDP_PORT))
    # Receive SSDP response messages
    data, addr = sock.recvfrom(1024)
    return data


def parse_sock_data(data: bytes):
    data_list = data.decode("utf-8").split("\r\n")
    location = [x for x in data_list if x.find("LOCATION") >= 0]
    # if len(location) > 0:
    #    ipaddress = location[0].split(" ")[1].strip()
    ipaddress = re.search(r"http://((\d{1,3}.){3}\d{1,3})", data.decode("utf-8"))[1]
    print(ipaddress)
    return ipaddress


def roku_operation():
    ipaddress = "192.168.0.122"
    roku = Roku(ipaddress)
    roku.poweron()
    roku.poweroff()


if __name__ == "__main__":
    data = find_roku_device_lan()
    parse_sock_data(data)
