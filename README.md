# telegram-stock-market-bot
The stock market bot uses the API of Moscow exchange and Central Bank of Russia

If you want to start the bot, you need to create a .db file (for example "users.db"), 
then you need to go to "config.py" file and change the value of USER_DATABASE_PATH 
to the current system path of the database.

Then go to @BotFather in Telegram and create a new bot. After doing this change TOKEN in config.py 
to the value of token @BotFather sent you.

# IF YOU USE WINDOWS
Open Windows cmd or PowerShell, choose the directory of the package and enter "python -m bot.py". 

# IF YOU USE LINUX
Open terminal (usually it is Bash), choose the directory of the package and enter "python3 -m bot.py"

In both cases Python 3 needed.
