import unittest
import sqlite3
from bot.data_modules.userfavouriteshares import UserFavouriteShares

DATABASE_PATH = "C:/Users/Валерий/Desktop/Projects/Telegram Market Bot/databases/test.db"
USER_TEST_ID1 = 1
USER_TEST_ID2 = 2
USER_TEST_ID3 = 3
USER_TEST_ID4 = 4

class TestUserFavouriteShares(unittest.TestCase):
    def setUp(self):
        #Drop all the table values
        
        self.userFavouriteShares1 = UserFavouriteShares(USER_TEST_ID1, database_path=DATABASE_PATH)
        self.userFavouriteShares2 = UserFavouriteShares(USER_TEST_ID2, database_path=DATABASE_PATH)
        self.userFavouriteShares3 = UserFavouriteShares(USER_TEST_ID3, database_path=DATABASE_PATH)
        self.userFavouriteShares4 = UserFavouriteShares(USER_TEST_ID4, database_path=DATABASE_PATH)
        
    def tearDown(self):
        self.clear_table()
        
    def clear_table(self):
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute("DELETE FROM users_favourite_shares")
        con.commit()
        con.close()
        
        
    def test_add_favourite_share(self):
                 
        self.userFavouriteShares1.add_favourite_share("YNDX")
        self.userFavouriteShares1.add_favourite_share("GAZP")
        with self.assertRaises(ValueError):
            self.userFavouriteShares1.add_favourite_share("YNDX")
            
        self.assertListEqual(self.userFavouriteShares1.get_favourite_shares(), ["YNDX", "GAZP"])
        
    def test_get_favourite_shares(self):
        share_list2 = self.userFavouriteShares2.get_favourite_shares()
        
        self.assertListEqual(share_list2, [])
        
        self.userFavouriteShares2.add_favourite_share("YNDX")
        self.userFavouriteShares2.add_favourite_share("GMKN")
        self.userFavouriteShares2.add_favourite_share("GAZP")
        
        share_list2 = self.userFavouriteShares2.get_favourite_shares()
        
        self.assertListEqual(share_list2, ["YNDX", "GMKN", "GAZP"])
        
    def test_remove_from_favourite_shares(self):
        
        self.userFavouriteShares3.add_favourite_share("YNDX")
        self.userFavouriteShares3.add_favourite_share("GMKN")
        self.userFavouriteShares3.add_favourite_share("GAZP")
        
        self.userFavouriteShares3.remove_from_favourite_shares("GMKN")

        self.assertListEqual(self.userFavouriteShares3.get_favourite_shares(), ["YNDX", "GAZP"])
        
        
    def test_clear_favourite_shares(self):
    
        self.userFavouriteShares3.add_favourite_share("YNDX")
        self.userFavouriteShares3.add_favourite_share("GMKN")
        self.userFavouriteShares3.add_favourite_share("GAZP")
        
        self.userFavouriteShares4.clear_favourite_shares()
        
        self.assertListEqual(self.userFavouriteShares4.get_favourite_shares(), []) 
        
if __name__ == "__main__":
    unittest.main()