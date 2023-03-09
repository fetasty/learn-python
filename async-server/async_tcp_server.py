'''
基于asyncio实现一个多协程的基于TCP的echo服务器, 对于客户端发来的消息加上固定前后缀返回
'''
import asyncio, socket, logging

logging.basicConfig(
  level=logging.DEBUG,
  filename=__file__ + '.log',
  format='%(asctime)s [%(levelname)5s] [%(thread)s]: %(message)s'
)

class AsyncTCPServer:
  def __init__(self, port: int):
    self.__port = port
    self.__host = '0.0.0.0' # 在所有ip上监听

  def run(self):
    asyncio.run(self.__main())

  async def __client_handler(self, reader, writer):
    addr = writer.get_extra_info('peername')
    logging.info(f'client({addr}) start deal, send "hi"')
    writer.write(f'hi {addr}'.encode())
    await writer.drain()
    while True:
      recv = await reader.read(1024)
      msg = recv.decode()
      logging.info(f'{addr} >> {msg}')
      if msg == 'bye':
        break
      data = f'echo {msg}'.encode()
      writer.write(data)
      await writer.drain()
    logging.info(f'close client {addr}')
    writer.close()
    await writer.wait_closed()

  async def __on_client_connected(self, reader, writer):
    addr = writer.get_extra_info('peername')
    logging.info(f'on client connected: {addr}')
    await asyncio.create_task(self.__client_handler(reader, writer))

  async def __main(self):
    logging.info('main start')
    # 构建服务器
    self.__server = await asyncio.start_server(
      self.__on_client_connected,
      host=self.__host,
      port=self.__port,
      family=socket.AF_INET, # 使用IPv4
      start_serving=False,
    )

    # 开始监听
    async with self.__server:
      await self.__server.serve_forever()

    logging.info('main exit')