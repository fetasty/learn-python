import asyncio, logging

logging.basicConfig(
  filename=__file__ + '.log',
  level=logging.DEBUG,
  format='%(asctime)s [%(levelname)5s]: %(message)s'
)

class MyProtocol(asyncio.DatagramProtocol):
  def connection_made(self, transport: asyncio.transports.DatagramTransport) -> None:
    self.transport = transport
    # addr = transport.get_extra_info('peername')
    logging.info('connection made')
    # self.transport.sendto(f'hi {addr}'.encode(), addr)
  def datagram_received(self, data: bytes, addr) -> None:
    msg = data.decode()
    logging.info(f'{addr} >> {msg}')
    msg = 'echo ' + msg
    logging.info(f'{addr} << {msg}')
    self.transport.sendto(msg.encode(), addr)

class AsyncUDPServer:
  def __init__(self, port: int) -> None:
    self.__host = '0.0.0.0'
    self.__port = port

  def run(self):
    asyncio.run(self.__main())

  async def __main(self):
    logging.info('main start')
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
      lambda: MyProtocol(),
      local_addr=(self.__host, self.__port),
    )
    try:
      await asyncio.sleep(3600) # serve for 1 hour
    finally:
      transport.close()
    logging.info('main exit')
