import unittest
from basic.learn_generator import *
from basic.learn_coroutine import *

class GeneratorTest(unittest.TestCase):
  def test_expr_generator(self):
    r = [1, 2, 3, 4, 5]
    self.assertEqual(list(expr_generator(1, 6)), r)
    g = expr_generator(1, 3)
    self.assertEqual(next(g), 1)
    self.assertEqual(next(g), 2)
    with self.assertRaises(StopIteration) as e:
      next(g)
    self.assertIsNone(e.exception.value)

  def test_fib_generator(self):
    r = [1, 1, 2, 3, 5, 8, 13]
    self.assertEqual(list(fib_generator(7)), r)

class CoroutineTest(unittest.TestCase):
  def test_consumer_producer(self):
    with self.assertLogs(level=logging.INFO):
      c = consumer()
      self.assertEqual(producer(c), 6)
