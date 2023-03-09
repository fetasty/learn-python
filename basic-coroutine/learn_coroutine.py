import logging, asyncio
from pathlib import Path

logging.basicConfig(
  format='%(asctime)s [%(levelname)5s]: %(message)s',
  level=logging.DEBUG,
  filename=f'{Path(__file__).name}.log'
)

def consumer():
  logging.info('-' * 5 +'consumer start')
  r = 0
  while True:
    p = yield r
    logging.info(f'comsume: {p}')
    if not p:
      break
    r += p
  logging.info('-' * 5 +'consumer exit')

def producer(c):
  logging.info('-' * 5 + 'producer start')
  r = 0
  # 使用send启动生成器, 必须传入参数None
  c.send(None)
  for i in range(3):
    logging.info(f'procude: {i + 1}')
    r = c.send(i + 1)
    logging.info(f'result: {r}')
  # 调用close可以关闭生成器, 生成器将从最后的yield处退出, 而不会打印后面的exit日志
  # 也可send(None), 让生成器自然退出, 但是会抛出StopIteration异常需要处理
  c.close()
  logging.info('-' * 5 +'producer exit')
  return r

async def async_consumer(name:str, q: asyncio.Queue):
  logging.info(f'{"-" * 5} async_consumer({name}) start')
  while True:
    v = await q.get() # 取出任务
    # 消费耗时1秒
    await asyncio.sleep(1)
    logging.info(f'{name} consume: {v}')
    q.task_done() # 告知任务完成

async def async_producer(name: str, q: asyncio.Queue):
  logging.info(f'{"-" * 5} async producer({name}) start')
  for i in range(6):
    # 生产耗时0.5秒
    await asyncio.sleep(0.5)
    v = f'{name}-{i}'
    logging.info(f'{name} produce: {v}')
    await q.put(v)
  logging.info(f'{"-" * 5} async producer({name}) exit')

async def async_consumer_producer_main():
  logging.info('main create tasks')
  q = asyncio.Queue()
  # 将协程打包为task, 就可以在loop循环中并发运行
  producers = [asyncio.create_task(async_producer(f'p{i + 1}', q)) for i in range(2)]
  consumers = [asyncio.create_task(async_consumer(f'c{i + 1}', q)) for i in range(2)]
  # 创建task之后就已经进入loop循环, 只要当前main协程await挂起后, loop中的其它task就能得以执行
  # await asyncio.sleep(5)
  logging.info('main wait producers done')
  # 不需要协程结果, 则使用wait; 若需要协程结果, 可以使用gather
  await asyncio.wait(producers)
  logging.info('main wait all queue tasks done')
  await q.join()
  logging.info('main cancel consumers')
  for t in consumers:
    t.cancel()
  logging.info('main wait cancel consumers')
  await asyncio.wait(consumers)
  logging.info('main exit')
