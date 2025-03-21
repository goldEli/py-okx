import unittest
from lib.strategy_utils import is_bottom_lower_strategy

class TestBottomLowerStrategy(unittest.TestCase):
    def test_is_bottom_lower_strategy(self):
        # 测试场景1：满足 strategy1 条件
        # - 有明显下引线 (lower_shadow_length/low > 0.004)
        # - 是底部 (low < low_1d * 1.002)
        # - 是针形 (lower_shadow_length/candle_length > 0.5)
        data1 = {
            'high': '102',
            'open': '101',
            'close': '100',
            'low': '95',
            '1d_high': '110',
            '1d_low': '96'
        }
        self.assertTrue(is_bottom_lower_strategy(data1))

        # 测试场景2：满足 strategy2 条件
        # - 是底部
        # - 下引线长度是实体长度的1倍以上
        data2 = {
            'high': '105',
            'open': '101',
            'close': '100',
            'low': '96',
            '1d_high': '110',
            '1d_low': '97'
        }
        self.assertTrue(is_bottom_lower_strategy(data2))

        # 测试场景3：都不满足条件的情况
        data3 = {
            'high': '105',
            'open': '103',
            'close': '102',
            'low': '101',
            '1d_high': '110',
            '1d_low': '95'
        }
        self.assertFalse(is_bottom_lower_strategy(data3))

        # 测试场景4：下引线不够长的情况
        data4 = {
            'high': '105',
            'open': '101',
            'close': '100',
            'low': '99.9',
            '1d_high': '110',
            '1d_low': '100'
        }
        self.assertFalse(is_bottom_lower_strategy(data4))

        # 测试场景5：不是底部的情况
        data5 = {
            'high': '105',
            'open': '101',
            'close': '100',
            'low': '95',
            '1d_high': '110',
            '1d_low': '90'
        }
        self.assertFalse(is_bottom_lower_strategy(data5))

if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/test__is_bottom_lower_strategy.py