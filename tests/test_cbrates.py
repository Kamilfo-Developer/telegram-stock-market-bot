import unittest
from bot.cbrates import CBRates

class TestCBRates(unittest.TestCase):
    def setUp(self):
        self.rates = CBRates(20, 1, 2022)
        
    def test_data(self):
        data = self.rates.data
        
        keys = data.keys()
        
        self.assertTrue("prices" in keys)
        self.assertTrue("nominal" in keys)
        self.assertTrue("names" in keys)
        
        self.assertEqual(data["prices"]["USD"], "76,4408")
    
    def test_get_previous_exchange_rates(self):
        prev_data = self.rates.get_previous_exchange_rates().data
        
        keys = prev_data.keys()
        
        self.assertTrue("prices" in keys)
        self.assertTrue("nominal" in keys)
        self.assertTrue("names" in keys)
        
        self.assertEqual(prev_data["prices"]["USD"], "76,8697")

if __name__ == "__main__":
    unittest.main()