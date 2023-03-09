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

