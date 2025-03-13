import unittest
from lib.strategy import is_long_upper_shadow, is_long_lower_shadow

class TestStrategy(unittest.TestCase):
    def test_long_upper_shadow_positive(self):
        # 测试长上引线的情况
        data = {
            'high': '12.431',      # 最高价
            'open': '10.435',       # 开盘价
            'close': '11.331',      # 收盘价
            'low': '10.425',        # 最低价
            '1d_high': '12.430',    # 日最高价
            '1d_low': '10.4'      # 日最低价
        }
        self.assertTrue(is_long_upper_shadow(data))

    def test_long_lower_shadow_positive(self):
        # 测试长下引线的情况
        data = {
            'high': '10.757',       # 最高价
            'open': '10.683',       # 开盘价
            'close': '10.726',      # 收盘价
            'low': '8',        # 最低价
            '1d_high': '11',    # 日最高价
            '1d_low': '9'      # 日最低价
        }
        self.assertTrue(is_long_lower_shadow(data))

    # def test_long_upper_shadow_negative(self):
    #     # 测试非长上引线的情况
    #     data = {
    #         'high': '60',       # 最高价
    #         'open': '55',       # 开盘价
    #         'close': '50',      # 收盘价
    #         'low': '45',        # 最低价
    #         '1d_high': '65',    # 日最高价
    #         '1d_low': '40'      # 日最低价
    #     }
    #     self.assertFalse(is_long_upper_shadow(data))

    # def test_long_lower_shadow_positive(self):
    #     # 测试长下引线的情况
    #     data = {
    #         'high': '60',       # 最高价
    #         'open': '55',       # 开盘价
    #         'close': '50',      # 收盘价
    #         'low': '20',        # 最低价
    #         '1d_high': '65',    # 日最高价
    #         '1d_low': '25'      # 日最低价
    #     }
    #     self.assertTrue(is_long_lower_shadow(data))

    # def test_long_lower_shadow_negative(self):
    #     # 测试非长下引线的情况
    #     data = {
    #         'high': '60',       # 最高价
    #         'open': '55',       # 开盘价
    #         'close': '50',      # 收盘价
    #         'low': '45',        # 最低价
    #         '1d_high': '65',    # 日最高价
    #         '1d_low': '40'      # 日最低价
    #     }
    #     self.assertFalse(is_long_lower_shadow(data))

    # def test_inverted_candle(self):
    #     # 测试收盘价高于开盘价的情况
    #     data = {
    #         'high': '100',      # 最高价
    #         'open': '45',       # 开盘价
    #         'close': '50',      # 收盘价
    #         'low': '40',        # 最低价
    #         '1d_high': '90',    # 日最高价
    #         '1d_low': '35'      # 日最低价
    #     }
    #     self.assertTrue(is_long_upper_shadow(data))

if __name__ == '__main__':
    unittest.main()
