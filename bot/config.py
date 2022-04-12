#If you want to change start sticker, then write the path here
START_STICKER_PATH = "bot/stickers/StartSticker.webp"
#The path of the database needed to store the lists of favourite shares of users
USER_DATABASE_PATH = "bot/db/users.db"
#Set this constant to False if you don't want to use cache
USE_CACHE = True
#The number represents how much time in seconds sould be passed to update cache 
CACHE_INTERVAL = 900
#The path for tests if you want to use them for some reasons
TEST_DATABASE_PATH = "bot/db/test.db"
#The list of valutes that will be shown to the user when /getrates entered
VALUTES = ["USD", "EUR", "GBP", "JPY", "CNY"]