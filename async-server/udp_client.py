import socket

if __name__ == '__main__':
  s = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_DGRAM,
  )
  s.connect(('127.0.0.1', 1235))
  # addr = ('127.0.0.1', 1235)
  while True:
    msg = input('send: ')
    s.send(msg.encode())
    if msg == 'bye':
      break
    data, addr = s.recvfrom(1024)
    msg = data.decode()
    print(f'recv: {msg}')

  s.close()
