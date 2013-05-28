__author__ = 'Maarten'
#MultiBus for interprocess comminucation

from multiprocessing.connection import Listener, Client
from multiprocessing import Process, Queue


class Packet():
    def __init__(self, action=PacketType.EMPTY, data={}):
        self.action = action
        self.data = data


class PacketType():
    EMPTY, TEST, SETMOTOR, PROCESSPICTURE, STARTSCAN, CALIBRATE, DONEPICTURE, DONESCAN = range(8)


class BusBase():
    def __init__(self, port, debug=True):
        self.port = port
        self.pwd = b"notasecret"
        self.debug = debug

    def _printDebug(self, msg):
        if self.debug:
            print(msg)


class BusServer(BusBase):
    def __init__(self, port, debug=True):
        BusBase.__init__(self, port, debug)
        self.queue = Queue()

    def getPacket(self):
        return self.queue.get()

    def queueEmpty(self):
        return self.queue.empty()

    def listen(self):
        p = Process(target=self._listenThread)
        p.start()

    def _listenThread(self):
        address = ('localhost', self.port)     # family is deduced to be 'AF_INET'
        listener = Listener(address, authkey=self.pwd)
        while True:
            conn = listener.accept()
            self._printDebug('MultiBus,Listner: connection accepted from' + str(listener.last_accepted))
            p = Process(target=self._connThread, args=(conn,))
            p.start();

    def _connThread(self, conn):
        self._printDebug("MultiBus,Conn: New process")
        while True:
            msg = conn.recv()
            if isinstance(msg, Packet):
                self.queue.put(msg)
                self._printDebug("MultiBus,Conn: Packet added")

            if msg == 'close':
                conn.close()
                self._printDebug("MultiBus,Conn: closed")
                break


class BusClient(BusBase):
    def send(self, packet):
        address = ('localhost', self.port)
        conn = Client(address, authkey=self.pwd)
        self._printDebug("MultiBus,Client: send")
        conn.send(packet)
        conn.send('close')
        conn.close()