__author__ = "Maarten in 't Hout"
# MultiBus Server example

from MultiBus import BusServer, PacketType


def parseAction(x):
    return {
        PacketType.EMPTY: 'empty',
        PacketType.TEST: 'test',
        PacketType.STARTSCAN: 'start scan'
    }.get(x, 'someting else')


if __name__ == '__main__':
    print("Test Server: init")
    s = BusServer(10001);
    s.listen();
    while True:
        packet = s.getPacket();

        print("Test Server: incoming packet Type: " + parseAction(packet.action))

