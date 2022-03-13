import unittest
from bot.utils.date import Date
from datetime import date as dt

td = dt.today()

class TestDate(unittest.TestCase):
    def setUp(self):
        self.date1 = Date()
        self.date2 = Date(1, 1, 2005)
        self.date3 = Date(31, 12, 2005)
        self.date4 = Date(28, 2, 2005)
        self.date5 = Date(29, 2, 2008)
        self.date6 = Date(1, 3, 2005)
        self.date7 = Date(1, 3, 2008)
        
    def test_get_current_day(self):
        self.assertEqual(self.date1.get_current_day(), td.day)
        self.assertEqual(self.date2.get_current_day(), td.day)
        self.assertEqual(self.date3.get_current_day(), td.day)
    
    def test_get_current_month(self):
        self.assertEqual(self.date1.get_current_month(), td.month)
        self.assertEqual(self.date2.get_current_month(), td.month)
        self.assertEqual(self.date3.get_current_month(), td.month)
    
    def test_get_current_year(self):
        self.assertEqual(self.date1.get_current_year(), td.year)
        self.assertEqual(self.date2.get_current_year(), td.year)
        self.assertEqual(self.date3.get_current_year(), td.year)
    
    def test_get_formated_date(self):
        self.assertEqual(self.date1.get_formated_date(separator="sep"), f'{"0" + str(td.day) if td.day < 10 else td.day}sep{"0" + str(td.month) if td.month < 10 else td.month}sep{td.year}')
        self.assertEqual(self.date2.get_formated_date(separator=".", reversed=True), "2005.01.01")
        self.assertEqual(self.date3.get_formated_date(), "31-12-2005")
        
    def test_get_previous_day_date(self):
        prev_date2 = self.date2.get_previous_day_date()
        prev_date3 = self.date3.get_previous_day_date()
        prev_date6 = self.date6.get_previous_day_date()
        prev_date7 = self.date7.get_previous_day_date()
        self.assertEqual(prev_date2.get_formated_date(), "31-12-2004")
        self.assertEqual(prev_date3.get_formated_date(), "30-12-2005")
        self.assertEqual(prev_date6.get_formated_date(), "28-02-2005")
        self.assertEqual(prev_date7.get_formated_date(), "29-02-2008")
        
    def test_get_next_day_date(self):
        next_date2 = self.date2.get_next_day_date()
        next_date3 = self.date3.get_next_day_date()
        next_date4 = self.date4.get_next_day_date()
        next_date5 = self.date5.get_next_day_date()
        
        self.assertEqual(next_date2.get_formated_date(), "02-01-2005")
        self.assertEqual(next_date3.get_formated_date(), "01-01-2006")
        self.assertEqual(next_date4.get_formated_date(), "01-03-2005")
        self.assertEqual(next_date5.get_formated_date(), "01-03-2008")
        
if __name__ == "__main__":
    unittest.main()