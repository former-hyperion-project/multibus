__author__ = "Maarten in 't Hout"
# MultiBus Client example

from MultiBus import BusClient, Packet, PacketType

if __name__ == '__main__':
    c = BusClient(10001)
    c.send(Packet(PacketType.TEST, {"test": "TESTING"}))
