from socket import socket, AF_INET, SOCK_STREAM

if __name__ == '__main__':
  s = socket(family=AF_INET, type=SOCK_STREAM)
  s.connect(('127.0.0.1', 1234))
  while True:
    data = s.recv(1024)
    print(f'recv: {data.decode()}')
    msg = input('input:')
    print(f'send: {msg}')
    s.send(msg.encode())
    if msg == 'bye':
      s.close()
      break
  print('exit')
