import unittest
from lib.strategy_utils import is_top_upper_strategy

class TestStrategyUtils(unittest.TestCase):
    def test_is_top_upper_strategy(self):
        # 测试场景1：满足 strategy1 条件
        # - 有明显上引线 (upper_shadow_length/high > 0.004)
        # - 是顶部 (high > high_1d * 0.998)
        # - 是针形 (upper_shadow_length/candle_length > 0.5)
        data1 = {
            'high': '100',
            'open': '95',
            'close': '94',
            'low': '93',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_top_upper_strategy(data1))

        # 测试场景2：满足 strategy2 条件
        # - 是顶部
        # - 上引线长度是实体长度的1倍以上
        data2 = {
            'high': '100',
            'open': '96',
            'close': '95',
            'low': '94',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_top_upper_strategy(data2))

        # 测试场景3：都不满足条件的情况
        data3 = {
            'high': '95',
            'open': '94',
            'close': '93',
            'low': '92',
            '1d_high': '100',
            '1d_low': '90'
        }
        self.assertFalse(is_top_upper_strategy(data3))

        # 测试场景4：上引线不够长的情况
        data4 = {
            'high': '95.1',
            'open': '95',
            'close': '94',
            'low': '93',
            '1d_high': '95',
            '1d_low': '90'
        }
        self.assertFalse(is_top_upper_strategy(data4))

if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/test__is_top_upper_strategy.py