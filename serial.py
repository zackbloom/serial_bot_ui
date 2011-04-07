import serial
import threading
import queue

def serial_connection():
    ser = serial.Serial()
    ser.port = '/dev/ttyS1'
    ser.baudrate = 19200
    ser.timeout = 1

    # Note: Use context interface (with), not actually opened yet
    return ser

class CleanThread(threading.Thread):
    def __init__(self):
        self._kill_switch = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        while not self._kill_switch.is_set():
            self.iterate()

    def join(self):
        self._kill_switch.set()
        threading.Thread.join(self)

class Communicator(CleanThread):
    def __init__(self, connector):
        CleanThread.__init__(self)

        self.connector = connector

        self.conn = self.connector.open()
        self.read_queue = queue.Queue()
        self.write_queue = queue.Queue()

    def write(self, message):
        self.write_queue.put(message)

    def read(self, block=False):
        try:
            return self.read_queue.get(block)
        except queue.Empty:
            return None

    def _read(self):
        try:
            line = self.conn.readline().strip()
            if line:
                self.read_queue.put(line)

        except serial.SerialTimeoutException:
            pass

    def _write(self):
        try:
            line = self.write_queue.get(False)
        except queue.Empty:
            return

        self.conn.write(line + '\n')

    def iterate(self):
        self._read()
        self._write()
