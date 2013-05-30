__author__ = 'Maarten'

from multiprocessing.connection import Client
from multibus import BusCore


class BusClient(BusCore.BusBase):
    def send(self, packet):
        address = ('localhost', self.port)
        conn = Client(address, authkey=self.pwd)
        self._printDebug("MultiBus,Client: send")
        conn.send(packet)
        conn.send('close')
        conn.close()