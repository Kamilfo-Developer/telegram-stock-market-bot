import unittest
from bot.msm_share import MSMShare

class TestMSMShare(unittest.TestCase):
    
    def setUp(self):
        self.share_data1 = MSMShare("YNDX")
        self.share_data2 = MSMShare("GAZP")
    
    def test_get_share_name(self):
        self.assertEqual(self.share_data1.get_share_name(), "Yandex clA")
        self.assertEqual(self.share_data2.get_share_name(), "ГАЗПРОМ ао")
        
    
    def test_get_share_price(self):
        self.assertEqual(type(self.share_data1.get_share_price()) is int, True)
        self.assertEqual(type(self.share_data2.get_share_price()) is int, True)
        
        
        with self.assertRaises(ValueError): 
            self.share_data3 = MSMShare("ABCDsdf")
        
if __name__ == "__main__":
    unittest.main()