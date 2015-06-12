"""ck2_mps

Usage:
  ck2_mps.py [<server-ip>]
  ck2_mps.py (-h | --help)

Options:
  -h --help     Show this screen.

"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import pyHook
import pythoncom
import requests
import pyautogui
from docopt import docopt

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(204)
        self.end_headers()

    def do_PUT(self):
        content_length = 0
        for header_name, header_value in self.headers.items():
            if header_name == 'Content-Length':
                content_length = int(header_value)
                break

        content = self.rfile.read(content_length).decode('utf-8')
        character = json.loads(content).get('character')
        if character == '+':
            pyautogui.press('add')
        elif character == '-':
            pyautogui.press('subtract')

        self._set_headers()

class Client(object):
    server_ip = None

    def __init__(self, server_ip):
        Client.server_ip = server_ip
        hm = pyHook.HookManager()
        hm.KeyDown = Client.on_keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()

    @staticmethod
    def on_keyboard_event(event):
        if chr(event.Ascii) in ('+', '-'):
            requests.put('http://{}:8080'.format(Client.server_ip),
                         data=json.dumps({'character': chr(event.Ascii)}))
        # return True to pass the event to other handlers
        return True

def server(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

def main(server_ip):
    if server_ip:
        Client(server_ip)
    else:
        server()

if __name__ == "__main__":
    args = docopt(__doc__)
    main(args['<server-ip>'])
