import sqlite3
import config
import json


class UserFavouriteShares:
    
    def __init__(self, user_id, database_path=config.USER_DATABASE_PATH):
        
        self.user_id = user_id
        self.__DATABASE_PATH = database_path
        
        self.__open_sql_connection()
        
        self.__sql_cursor.execute("CREATE TABLE IF NOT EXISTS users_favourite_shares (id INTEGER NOT NULL, favourite_shares TEXT)")
        self.__sql_connection.commit()
        
        self.__close_sql_connection()
        
    def __open_sql_connection(self):
        self.__sql_connection = sqlite3.connect(self.__DATABASE_PATH)
        self.__sql_cursor = self.__sql_connection.cursor()
    
    def __close_sql_connection(self):
        self.__sql_connection.close()
    
    def add_favourite_share(self, mcx):
        self.__open_sql_connection()
        
        data = list(self.__sql_cursor.execute(f"SELECT favourite_shares FROM users_favourite_shares WHERE id = {self.user_id}"))
        
        if not data:
            self.__sql_cursor.execute(f"""INSERT INTO users_favourite_shares (id, favourite_shares) VALUES ({self.user_id}, '["{mcx.upper()}"]')""")
        else:
            current_fav = json.loads(list(data)[0][0])
            if mcx in current_fav:
                raise ValueError(f"""This MCX is already in favorite list of user with next id: {self.user_id}""")
            current_fav.append(mcx.upper())
            current_fav = json.dumps(current_fav, separators=(',', ':'))
            
            self.__sql_cursor.execute(f"""UPDATE users_favourite_shares SET favourite_shares='{current_fav}' WHERE id = {self.user_id}""")
            
        self.__sql_connection.commit()
        self.__close_sql_connection()
        
    def get_favourite_shares(self) -> list:
        self.__open_sql_connection()
        
        data = list(self.__sql_cursor.execute(f"""SELECT favourite_shares FROM users_favourite_shares WHERE id = {self.user_id}"""))
        
        self.__close_sql_connection()
        #if data is empty returns [] else returns favourite_shares

        return json.loads(data[0][0]) if data else []
    
    def remove_from_favourite_shares(self, mcx):
        fav_shares = self.get_favourite_shares()

        self.__open_sql_connection()
                
        result = []
        for i in fav_shares:
            if not i == mcx.upper():
                result.append(i)

        self.__sql_cursor.execute(f"""UPDATE users_favourite_shares SET favourite_shares='{json.dumps(result)}' WHERE id = {self.user_id}""")
        
        self.__sql_connection.commit()
        
        self.__close_sql_connection()
            
    def clear_favourite_shares(self):
        self.__open_sql_connection()

        self.__sql_cursor.execute(f"""UPDATE users_favourite_shares SET favourite_shares='{"[]"}' WHERE id = {self.user_id}""")
        self.__sql_connection.commit()
        
        self.__close_sql_connection()
        
