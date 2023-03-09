from .async_tcp_server import *

if __name__ == '__main__':
  server = AsyncServer(1234)
  server.run()
