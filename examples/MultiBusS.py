__author__ = "Maarten in 't Hout"
# MultiBus Server example

from multibus import BusCore, BusServer

def parseAction(x):
    return {
        BusCore.PacketType.EMPTY: 'empty',
        BusCore.PacketType.TEST: 'test',
        BusCore.PacketType.STARTSCAN: 'start scan'
    }.get(x, 'someting else')

if __name__ == '__main__':
    print("Test Server: init")
    s = BusServer.BusServer(10001);
    s.listen();
    while True:
        packet = s.getPacket();

        print("Test Server: incoming packet Type: " + parseAction(packet.action))