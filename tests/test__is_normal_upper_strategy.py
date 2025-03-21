import unittest
from lib.strategy_utils import is_normal_upper_strategy

class TestNormalUpperStrategy(unittest.TestCase):
    def test_is_normal_upper_strategy(self):
        # 测试场景1：满足普通上引线策略条件
        # - 有明显上引线
        # - 上引线长度超过实体长度的0.5倍
        data1 = {
            'high': '100',
            'open': '95',
            'close': '94',
            'low': '93',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_normal_upper_strategy(data1))

        # 测试场景2：上引线长度不够的情况
        data2 = {
            'high': '95.2',
            'open': '95',
            'close': '94',
            'low': '93',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertFalse(is_normal_upper_strategy(data2))

        # 测试场景3：没有上引线的情况（收盘价等于最高价）
        data3 = {
            'high': '95',
            'open': '94',
            'close': '95',
            'low': '93',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertFalse(is_normal_upper_strategy(data3))

        # 测试场景4：下跌K线但有长上引线
        data4 = {
            'high': '100',
            'open': '96',
            'close': '94',
            'low': '93',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_normal_upper_strategy(data4))

        # 测试场景5：上涨K线且有长上引线
        data5 = {
            'high': '100',
            'open': '94',
            'close': '96',
            'low': '93',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_normal_upper_strategy(data5))

if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/test__is_normal_upper_strategy.py