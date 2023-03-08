def expr_generator(a: int, b: int):
  return (x for x in range(a, b))

def fib_generator(n: int):
  a = 0
  b = 1
  for i in range(n):
    yield b
    a, b = b, a + b
