import unittest
from lib.strategy import is_long_upper_shadow, is_long_lower_shadow

class TestStrategy(unittest.TestCase):
    def test_is_long_upper_shadow(self):
        # 测试正常长上引线的情况
        data = {
            'high': '100',
            'open': '50',
            'close': '45',
            'low': '40'
        }
        self.assertTrue(is_long_upper_shadow(data))

        # 测试非长上引线的情况
        data = {
            'high': '100',
            'open': '95',
            'close': '90',
            'low': '85'
        }
        self.assertFalse(is_long_upper_shadow(data))

        # 测试负值情况（应该返回False）
        data = {
            'high': '50',
            'open': '60',
            'close': '55',
            'low': '45'
        }
        self.assertFalse(is_long_upper_shadow(data))

    def test_is_long_lower_shadow(self):
        # 测试正常长下引线的情况
        data = {
            'high': '80',
            'open': '60',
            'close': '70',
            'low': '2'
        }
        self.assertTrue(is_long_lower_shadow(data))

        # # 测试非长下引线的情况
        data = {
            'high': '100',
            'open': '95',
            'close': '90',
            'low': '85'
        }
        self.assertFalse(is_long_lower_shadow(data))

        # 测试负值情况（应该返回False）
        data = {
            'high': '50',
            'open': '45',
            'close': '55',
            'low': '40'
        }
        self.assertFalse(is_long_lower_shadow(data))

if __name__ == '__main__':
    unittest.main()
