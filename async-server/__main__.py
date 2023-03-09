# from .async_tcp_server import *
from .async_udp_server import *

if __name__ == '__main__':
  # server = AsyncTCPServer(1234)
  server = AsyncUDPServer(1235)
  server.run()
