__author__ = "Maarten in 't Hout"
# MultiBus Client example

from multibus import BusCore,BusClient

if __name__ == '__main__':
    c = BusClient.BusClient(10001)
    c.send(BusCore.Packet(BusCore.PacketType.TEST, {"test": "TESTING"}))
