import unittest
from configuration.tool.tools import *

class ToolsTestCase(unittest.TestCase):
    def test_tools(self):
        self.assertEqual(exists(EntType.PROMO, 89), (False, []))


if __name__ == '__main__':
    unittest.main()
