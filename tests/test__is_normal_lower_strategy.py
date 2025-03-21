import unittest
from lib.strategy_utils import is_normal_lower_strategy

class TestNormalLowerStrategy(unittest.TestCase):
    def test_is_normal_lower_strategy(self):
        # 测试场景1：满足普通下引线策略条件
        # - 有明显下引线
        # - 下引线长度超过实体长度的0.5倍
        data1 = {
            'high': '102',
            'open': '101',
            'close': '100',
            'low': '95',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_normal_lower_strategy(data1))

        # 测试场景2：下引线长度不够的情况
        data2 = {
            'high': '102',
            'open': '101',
            'close': '100',
            'low': '99.8',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertFalse(is_normal_lower_strategy(data2))

        # 测试场景3：没有下引线的情况（开盘价等于最低价）
        data3 = {
            'high': '102',
            'open': '95',
            'close': '100',
            'low': '95',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertFalse(is_normal_lower_strategy(data3))

        # 测试场景4：上涨K线但有长下引线
        data4 = {
            'high': '102',
            'open': '98',
            'close': '100',
            'low': '95',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_normal_lower_strategy(data4))

        # 测试场景5：下跌K线且有长下引线
        data5 = {
            'high': '102',
            'open': '100',
            'close': '98',
            'low': '95',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_normal_lower_strategy(data5))

        # 测试场景6：实体很小但下引线明显的情况
        data6 = {
            'high': '100.2',
            'open': '100',
            'close': '100.1',
            'low': '93',
            '1d_high': '99',
            '1d_low': '90'
        }
        self.assertTrue(is_normal_lower_strategy(data6))

if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/test__is_normal_lower_strategy.py