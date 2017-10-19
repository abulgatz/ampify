#!/usr/bin/python

# Denon amp implementation

__author__ = 'Pascal Hahn <ph@lxd.bz>'

import ampify
import socket
import string

class Denon3312(ampify.Amplifier):
  COMMANDS = {
      'SleepTimer': {
        'off': 'SLPOFF',
        'on': 'SL%i',
      },
      'Status': {
        'onscreen': 'NSE',
      },
    }

  def __init__(self, amp_ip):
    super(Denon3312, self).__init__(self.__class__.COMMANDS, DenonIpConnector(amp_ip))

class DenonIpConnector(ampify.BaseConnector):
  def __init__(self, amp_ip, timeout=2, amp_port=23, limit=135):
    self.amp_ip = amp_ip
    self.amp_port = amp_port
    self.timeout = timeout
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.amp_ip, self.amp_port))
    self.buffer = ''
    self.limit = limit

  def execute(self, command):
    self.sock.send(command + '\r')

  def close(self):
    self.sock.close()

  def response(self):
    data = self.sock.recv(self.limit)

    if data.endswith('\r'):
      return data
    else:
      return data + self.response()

  def response_list(self):
    return filter(None, string.split(self.response(), '\r'))

  def print_utf8_list(self, my_list):
    for item in my_list:
      print u"{}".format(item).encode('UTF-8')


if __name__ == '__main__':
  myamp = Denon3312('192.168.1.31')
