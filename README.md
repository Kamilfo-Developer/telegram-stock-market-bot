# telegram-stock-market-bot
A stock market bot that uses the API of Moscow Exchange and Central Bank of Russia

# How to start the bot?
If you want to start the bot, you need to create a .db file (for example "users.db"), 
then you need to go to "config.py" file and change the value of USER_DATABASE_PATH 
to the current system path of the database.

Then go to @BotFather in Telegram and create a new bot. After doing this create file bot_token.py in bot directory and write next code: TOKEN = "TOKEN". Instead of writing TOKEN in double quotes you need to write your token without deleting the quotes.

IF YOU USE WINDOWS:
Open Windows cmd or PowerShell, choose the directory of the package and enter "pip install -r requirements.txt", after 
installing all dependencies enter "python -m bot.py". 

IF YOU USE LINUX:
Open terminal (usually it is Bash), choose the directory of the package and firstly enter "pip install -r requirements.txt", after 
installing all dependencies enter "python3 -m bot.py"

In both cases Python 3 and pip needed.
