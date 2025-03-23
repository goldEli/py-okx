import unittest
from lib.strategy_utils import is_normal_lower_strategy

class TestNormalLowerStrategy(unittest.TestCase):
    def test_is_normal_lower_strategy(self):
        # 测试场景1：满足普通下引线策略条件
        # - 有明显下引线
        # - 下引线长度超过实体长度的0.5倍
        data1 = {
            'high': '0.00010239',
            'open': '0.00010192',
            'close': '0.00009932',
            'low': '0.00009687',
            '1d_high': '0.0001042',
            '1d_low': '0.0001042'
        }
        self.assertTrue(is_normal_lower_strategy(data1))

     

if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/test__is_normal_lower_strategy.py