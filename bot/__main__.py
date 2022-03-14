from bot.bot import Bot
import bot.bot_token as bot_token

if (__name__ == '__main__'):    
    #initializing the bot 
    try:
        Bot(bot_token.TOKEN).start()

    except Exception as err:
        print(f"The bot stopped. Reason: {err}")