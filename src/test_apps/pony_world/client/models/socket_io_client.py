from socketIO_client import SocketIO
import asyncio
import threading


class SocketIOClient:
    def __init__(self, host, port):
        self.socketIO = SocketIO(host, port)

    def get_sid(self):
        return self.socketIO._engineIO_session.id

    def send_message(self, message):
        self.socketIO.emit('location_message', message)

    def handle_message(self, handler):
        def task():
            self.socketIO.on('location_message', handler)
            self.socketIO.wait()

        thread = threading.Thread(target=task)
        thread.start()