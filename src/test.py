import unittest
from src.templates import signalstemp


class MyTestCase(unittest.TestCase):
    def build_grain(self):
        signalstemp.build_grain()


if __name__ == '__main__':
    unittest.main()
