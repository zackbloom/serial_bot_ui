import serial
import threading
import Queue as queue

def serial_connection(url='/dev/ttyS1', rate=19200):
    ser = serial.serial_for_url(url)
    ser.port = url
    ser.baudrate = rate
    ser.timeout = 1

    # Note: Use context interface (with) or open/close, not actually opened yet
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

class Channel(CleanThread):
    def __init__(self, connection, on_func=None):
        CleanThread.__init__(self)

        self.conn = connection
        self.queue = queue.Queue(1000)

        self.on_func = on_func

    def __len__(self):
        return len(self.queue)

class Reader(Channel):
    def iterate(self):
        try:
            line = self.conn.readline().strip()
            if line:
                try:
                    self.read_queue.put(line, False)
                except queue.Full:
                    pass

                if self.on_func:
                    self.on_func(line)

        except serial.SerialTimeoutException:
            pass

    def read(self, block=False):
        try:
            msg = self.queue.get(block)
            self.queue.task_done()

            return msg
        except queue.Empty:
            return None
   
class Writer(Channel):
    def iterate(self):
        try:
            line = self.queue.get(False)
        except queue.Empty:
            return

        self.conn.write(line + '\n')
        if self.on_func:
            self.on_func(line)

        self.queue.task_done()

    def write(self, message):
        try:
            self.queue.put(message)
        except queue.Full:
            pass

class Connection(object):
    """
    A bidirectional connection.
    """
    def __init__(self, connector=serial_connection()):
        self.connector = connector
        self.conn = self.connector.open()

        self.reader = Reader(self.conn, self._call_on_read)
        self.writer = Writer(self.conn)

        self.reader.start()
        self.writer.start()

        self.on_read_funcs = []

    def __enter__(self):
        return self

    def __exit__(self, *errs):
        self.close()

        return True

    def close(self):
        self.reader.join()
        self.writer.join()

        self.conn.close()

    def __len__(self):
        return len(self.reader)

    def write(self, message):
        """
        Write a message.
        
        The call will always return immediatly, even before the message is written.
        """
        self.writer.write(message)

    def read(self, block=False):
        """
        Read a message.

        If block is False (the default), None will be returned if no message is waiting.
        If block is True, the call will block until a message is recv'd.
        """
        return self.reader.read(block)

    def on_read(self, func):
        self.on_read_funcs.append(func)

    def _call_on_read(self, msg):
        for func in self.on_read_funcs:
            func(msg)
