__author__ = 'Maarten'

from multiprocessing.connection import Listener
from multiprocessing import Process, Queue
from multibus import BusCore


class BusServer(BusCore.BusBase):
    def __init__(self, port, debug=True):
        BusCore.BusBase.__init__(self, port, debug)
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
            p.start()

    def _connThread(self, conn):
        self._printDebug("MultiBus,Conn: New process")
        while True:
            msg = conn.recv()
            if isinstance(msg, BusCore.Packet):
                self.queue.put(msg)
                self._printDebug("MultiBus,Conn: Packet added")

            if msg == 'close':
                conn.close()
                self._printDebug("MultiBus,Conn: closed")
                break