# Author: Haoji Liu
import zmq

# they will be on the same physical machine
display_host = '127.0.0.1'
chat_host = display_host
# temp ports
chat_port = 8080
display_port = 8081

class Server(object):

    def __init__(self, chat_port, display_port):
        self.chat_port = chat_port
        self.display_port = display_port
        self.chat_sock = None
        self.display_sock = None
        self.context = zmq.Context()

    def bind_chat_port(self):
        self.chat_sock = self.context.socket(zmq.REP)
        chat_bind_string = 'tcp://{}:{}'.format(
            chat_host, self.chat_port)
        self.chat_sock.bind(chat_bind_string)

    def bind_display_port(self):
        self.display_sock = self.context.socket(zmq.PUB)
        display_bind_string = 'tcp://{}:{}'.format(
            display_host, self.display_port)
        self.display_sock.bind(display_bind_string)

    def main(self):
        self.bind_chat_port()
        self.bind_display_port()
        while True:
            data = self.chat_sock.recv_json()
            self.chat_sock.send(b'\x00')
            self.display_sock.send_json(data)

if '__main__' == __name__:
    try:
        server = Server(chat_port, display_port)
        server.main()
    except KeyboardInterrupt:
        pass
