import unittest
from lib.strategy_utils import is_bottom_lower_strategy

class TestBottomLowerStrategy(unittest.TestCase):
    def test_is_bottom_lower_strategy(self):
        # 测试场景1：满足 strategy1 条件
        # - 有明显下引线 (lower_shadow_length/low > 0.004)
        # - 是底部 (low < low_1d * 1.002)
        # - 是针形 (lower_shadow_length/candle_length > 0.5)
        data1 = {
            'high': '0.00010239',
            'open': '0.00010192',
            'close': '0.00009932',
            'low': '0.00009687',
            '1d_high': '0.0001042',
            '1d_low': '0.0001042'
        }
        self.assertTrue(is_bottom_lower_strategy(data1))



if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/test__is_bottom_lower_strategy.py