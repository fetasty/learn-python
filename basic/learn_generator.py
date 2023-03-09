# 生成式定义的生成器, 语法上与列表生成式类似
def expr_generator(a: int, b: int):
  return (x for x in range(a, b))

# 函数定义的生成器, yield执行后, 返回一个值, 暂存当前的函数状态并返回(让出CPU)
# 当下次next调用或者迭代时, 继续从上次yield之后的位置执行, 直到再次碰到yield放弃CPU
def fib_generator(n: int):
  a = 0
  b = 1
  for i in range(n):
    yield b
    a, b = b, a + b
