# Haoji Liu
import sys

import zmq

usage_msg = 'Usage: python3.py <user_name>'
conn_success_msg = 'User[%s] Connected to the chat server'
localhost = '127.0.0.1'
# temp ports
chat_port = 8080
display_port = 8081

def bind_chat_port(context):
    # to send message to
    chat_sock = context.socket(zmq.REQ)
    connect_string = 'tcp://{}:{}'.format(
        localhost, chat_port)
    chat_sock.connect(connect_string)
    return chat_sock

def bind_display_port(context):
    # to receive messages from
    display_sock = context.socket(zmq.SUB)
    connect_string = 'tcp://{}:{}'.format(
        localhost, display_port)
    display_sock.connect(connect_string)
    display_sock.setsockopt(zmq.SUBSCRIBE, b"")
    return display_sock

def display(poller, display_sock, uname):
    while True:
        events = dict(poller.poll(50))
        if events.get(display_sock) == zmq.POLLIN:
            data = display_sock.recv_json()
            username, display_msg = data['username'], data['message']
            if username != uname:
                print('[{}]: {}'.format(username, display_msg))
        else:
            return

def main(uname):
    # ZeroMQ Context
    context = zmq.Context()
    chat_sock = bind_chat_port(context)
    display_sock = bind_display_port(context)

    poller = zmq.Poller()
    poller.register(display_sock, zmq.POLLIN)

    print(conn_success_msg % uname)

    while True:
        message = input('[%s] > ' % uname)
        data = {
            'username': uname,
            'message': message}
        # send
        chat_sock.send_json(data)
        # wait for response
        resp = chat_sock.recv()
        # blocking-style display
        display(poller, display_sock, uname)

if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except:
        print(usage_msg)
        exit(0)
    main(username)
