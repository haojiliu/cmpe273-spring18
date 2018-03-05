# Referenced https://docs.python.org/2/library/curses.html and
# https://github.com/jnthnwn/zmq-chat/blob/master/zmqchat.py
# Haoji Liu
import curses
import sys
import threading
import time

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

def display(window, display_sock, uname):
    window.clear()
    window.refresh()
    window_lines, window_cols = window.getmaxyx()
    bottom_line = window_lines - 1
    window.bkgd(curses.A_NORMAL, curses.color_pair(2))
    window.scrollok(1)
    window.addstr(bottom_line, 1, conn_success_msg % uname)
    window.move(bottom_line, 1)
    window.scroll(1)
    window.refresh()

    while True:
        # TODO: display logic should be on a separate thread/screen
        data = display_sock.recv_json()
        username, message = data['username'], data['message']
        window.addstr(bottom_line, 1, '[{}]: {}'.format(username, message))
        window.scroll(1)
#        window.move(bottom_line, 1)
        window.refresh()

def chat(window, chat_sock, uname):
    window.clear()
    window.bkgd(curses.A_NORMAL, curses.color_pair(2))
    window.box()
    window.refresh()

    prompt_msg = '[%s] > ' % uname
    len_prompt_msg = len(prompt_msg)

    while True:
        window.clear()
        window.box()
        window.addstr(1, 1, prompt_msg)
        window.refresh()

        s = window.getstr(1, len_prompt_msg+1).decode('utf-8')
        if s is not None and s != "":
            data = {
                'username': uname,
                'message': s}
            # send
            chat_sock.send_json(data)
            # wait for response
            resp = chat_sock.recv()
        time.sleep(0.05)

def main(stdscr):
    try:
        username = sys.argv[1]
    except:
        print(usage_msg)
        exit(0)

    # ZeroMQ Context
    context = zmq.Context()
    chat_sock = bind_chat_port(context)
    display_sock = bind_display_port(context)

    # curses set up
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # # ensure that user input is echoed to the screen
    curses.echo()
    curses.curs_set(0)

    window_height = curses.LINES
    window_width = curses.COLS
    division_line =  int(window_height * 0.8)

    # instaniate two pads - one for displaying received messages
    # and one for showing the message the user is about to send off
    top_pad = stdscr.subpad(division_line, window_width, 0, 0)
    bottom_pad = stdscr.subpad(window_height - division_line, window_width, division_line, 0)

    top_thread = threading.Thread(target=display, args=(top_pad, display_sock, username))
    top_thread.daemon = True
    top_thread.start()

    bottom_thread = threading.Thread(target=chat, args=(bottom_pad, chat_sock, username))
    bottom_thread.daemon = True
    bottom_thread.start()

    top_thread.join()
    bottom_thread.join()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt as e:
        pass
    except:
        raise
