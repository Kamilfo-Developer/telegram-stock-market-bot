from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from bot.data_modules.msm_share import MSMShare
from bot.data_modules.userfavouriteshares import UserFavouriteShares
from bot.data_modules.cbrates import CBRates
from bot.utils.date import Date

import logging
import bot.config as config

class Bot:
    def __init__(self, token) -> None:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        
        self.logger = logging.getLogger()
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        
        #Setting handlers
        message_handler = MessageHandler(Filters.text & (~Filters.command), 
                                         self.handle_message)
        
        sticker_handler = MessageHandler(Filters.sticker & (~Filters.command & ~Filters.text), 
                                         self.handle_sticker)
        
        start_handler = CommandHandler("start", self.handle_start)
        get_rates_handler = CommandHandler("getrates", self.handle_get_rates, pass_args=True)
        get_favourite_handler = CommandHandler("getfavourite", self.handle_get_favourite)
        clear_favourite = CommandHandler("clearfavourite", self.handle_clear_favourite)
        
        #Setting handlers
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(sticker_handler)
        self.dispatcher.add_handler(get_rates_handler)
        self.dispatcher.add_handler(get_favourite_handler)
        self.dispatcher.add_handler(clear_favourite)
    
    def start(self) -> None:
        self.updater.start_polling()
    
    def handle_start(self, update, context) -> None:
        """Handles "/start" command
        
        """
        chat_id = update.effective_chat.id
        first_name = update.effective_chat.first_name
        full_name = update.effective_chat.full_name
        bot_name = context.bot.get_me().first_name
        
        path = config.START_STICKER_PATH
        
        if path: 
            sti = open(path, 'rb')
            context.bot.send_sticker(chat_id, sti)
        
        message = f"Доброго времени суток{f', {first_name}'}!\n\nЯ - {bot_name}, биржевой бот, благодаря которому Вы можете узнать котировки акций и курс валют Центробанка России.\n\nНа данный момент доступны только акции Московской биржи. Это означает, что бот не может получить котировки акций \"Apple\", \"Google\" или \"Amazon\".\n\nТакже Вы можете получить основные курсы валют ЦБ РФ к рублю, введя команду \"/getrates\", или выбрав её в меню команд. Если Вы хотите получить курс на какую-нибудь конкретную дату, то введите \"/getrates нужная дата\"\nВот пара примеров:\n/getrates 24.02.2022\n/getrates 20.8.2020.\n\nЧтобы получить доступ к цене непосредственно акции, просто отправьте её <a href=\"https://ru.wikipedia.org/wiki/%D0%A2%D0%B8%D0%BA%D0%B5%D1%80\">тикер</a> в любом регистре. Например, <b>\"YNDX\"</b> или <b>\"GaZp\"</b>.\n\nЕщё Вы можете добавлять акции в избранное, для этого просто отправьте тикер акции, а затем, на появившейся клавиатуре выберите \"Добавить в избранное [тикер акции]\".\n\nЗатем, когда Вы захотите увидеть стоимость избранных акций, введите \n\"/getfavourite\". Аналогично можно удалить акцию из списка. Если Вы хотите мгновенно удалить все акции, просто введите команду \n\"/clearfavourite\" и список будет полностью очищен.\n\nПриятного пользования!"
        
        context.bot.send_message(chat_id, message, parse_mode="html", disable_web_page_preview=True)
        
        self.logger.info(f"{full_name} selected start command")

    def handle_get_favourite(self, update, context) -> None:
        """Handles "/getfavourite" command
        
        """
        chat_id = update.effective_chat.id
        full_name = update.effective_chat.full_name
        
        message = "Стоимость избранных акций:\n"
        log_message = f"{full_name} required the favourite shares list"
        
        favourite_shares = UserFavouriteShares(chat_id).get_favourite_shares()
        
        if not favourite_shares:
            message = "У вас пока нет избранных акций😅\nПопробуйте ввести ticker акции, например \"YNDX\"."
        
        for ticker in favourite_shares:
            share = MSMShare(ticker)
            message += f"{ticker} ({share.get_share_name()}): <b>{share.get_share_price()}</b>₽\n"
            
        self.logger.info(log_message)
        
        context.bot.send_message(chat_id, message, parse_mode="html")
                        
    def handle_clear_favourite(self, update, context) -> None:
        """Handles "/clearfavourite" command

        """
        chat_id = update.effective_chat.id
        full_name = update.effective_chat.full_name
        
        log_message = f"{full_name} cleard favourite list"
        
        UserFavouriteShares(chat_id).clear_favourite_shares()
        
        self.logger.info(log_message)
        
            
        context.bot.send_message(chat_id, f"Список избранных акций был очищен.")

    def handle_get_rates(self, update, context) -> None:
        """Handles "/getrates" command

        """
        chat_id = update.effective_chat.id
        full_name = update.effective_chat.full_name 
        
        args = context.args    
        
        NEEDED_RATES = config.VALUTES
                
        if not args:
            date = Date().get_next_day_date()
            
            CB_exchange_rates = CBRates((date.day, date.month, date.year))
            
            previous_CB_exchange_rates = CB_exchange_rates.get_previous_exchange_rates()

            message = "🏦\nКурсы ЦБ валют к рублю:\n"
            
            current_data = CB_exchange_rates.data
            previous_data = previous_CB_exchange_rates.data
            
            for key in NEEDED_RATES:
                if current_data[key]['price'] > previous_data[key]['price']:
                    sign = '⏫'
                elif current_data[key]['price'] < previous_data[key]['price']:
                    sign = '⏬'
                else:
                    sign = ''
                    
                message += f"{current_data[key]['nominal']} {current_data[key]['name'][0].lower() + current_data[key]['name'][1:]}:\n<b>{current_data[key]['price']}₽</b>{sign}\n"
                
            log_message = f"{full_name} required CB rates"
            
            return       
        
        try:
            
            date = args[0].split('.')
            
            rates = CBRates(date=(date[0], date[1], date[2])).data
            
            date = '.'.join(date)
            
            message = f"🏦\nКурс ЦБ валют к рублю на {date}:\n"
            for key in NEEDED_RATES:
                try:
                    message += f"{rates[key]['nominal']} {rates[key]['name'][0].lower() + rates[key]['name'][1:]}:\n<b>{rates[key]['price']}₽</b>\n"
                except KeyError:
                    continue
                
            log_message = f"{full_name} required CBRates with next date: {date}"
        
        except (ValueError, IndexError):
            message = "Похоже Вы ввели непрвильную дату с командой /getrates.\n\nКоманда должна иметь следующий вид:\n/getrates день.месяц.год.\n\nПримеры корректного ввода:\n/getrates 24.02.2022\n/getrates 20.8.2020"
            log_message = f"{full_name} tried to require CBRates, but the date was incorrect. Input: {date}"
                        
        self.logger.info(log_message)
        context.bot.send_message(chat_id, message, parse_mode="html")
                
    def handle_message(self, update, context) -> None:
        """Handles any text message

        """
        chat_id = update.effective_chat.id
        full_name = update.effective_chat.full_name 
        text = update.message.text
        
        reply_keyboard = [[]]
            
        if "Добавить в избранное:" in text:
            ticker = f"{text[-4]}{text[-3]}{text[-2]}{text[-1]}"
            userFavouriteShares = UserFavouriteShares(chat_id)
            
            if not ticker in userFavouriteShares.get_favourite_shares():
                userFavouriteShares.add_favourite_share(ticker)
                message = f"Акция \"{ticker}\" была добавлена в избранное.\nВведите команду \"/getfavourite\", чтобы увидеть стоимость избранных акций."
                log_message = f"{full_name} added {ticker} share to the favourite list"

                return 
            
            message = f"Акция \"{ticker}\" уже в Вашем списке избранных акций🤷‍♂️"
            log_message = f"{full_name} tried to add {ticker} to the favourite list, but the share is already there"
            
            return 
            
        if "Удалить из избранного:" in text:
            #Here we connect to the DataBase and remove the share from the user's favourite list
            ticker = f"{text[-4]}{text[-3]}{text[-2]}{text[-1]}"
            userFavouriteShares = UserFavouriteShares(chat_id)
            
            if ticker in userFavouriteShares.get_favourite_shares():  
                UserFavouriteShares(chat_id).remove_from_favourite_shares(ticker)
                message = f"Акция \"{ticker}\" была удалена из избранного.\nВведите команду \"/getfavourite\", чтобы увидеть стоимость избранных акций."
                log_message = f"{full_name} removed {ticker} share from the favourite list"

                return 
                
            message = f"Акции \"{ticker}\ и так нет в Вашем списке избранных акций🤷‍♂️"
            log_message = f"{full_name} tried to remove {ticker} share from the favourite list, but it was alredy not there"
            
            return
                
        
        try:
            #Here we a Moscow Stock Market share and get its price.
            #If the share is in the user's favourite list, we change it either "Add to favourite shares list" or "Remove from favourite shares list"
            share = MSMShare(text)
            price = share.get_share_price()
            share_name = share.get_share_name()
                
            log_message = f"{full_name} required {text} share, its price is {price} RUB"
            message = f"По данным Московской биржи, стоимость акций {share_name} составляет <b>{price}</b>₽."
                
            reply_keyboard = [[KeyboardButton(f"Добавить в избранное: {text.upper()}")]] if not text.upper() in UserFavouriteShares(chat_id).get_favourite_shares() else [[KeyboardButton(f"Удалить из избранного: {text.upper()}")]]
        
        except ValueError:
            message = "Упс... Похоже такой акции нет..."
            log_message = f"{full_name} required non-existent share. Entered value: {text}"
            
        self.logger.info(log_message)
        
        context.bot.send_message(chat_id, message, parse_mode="html", reply_markup=ReplyKeyboardMarkup(keyboard=(reply_keyboard or ""), one_time_keyboard=True, resize_keyboard=True))

    def handle_sticker(self, update, context) -> None:
        """Handles any sticker

        """
        chat_id = update.effective_chat.id
        first_name = update.effective_chat.first_name
        last_name = update.effective_chat.last_name or ""
        
        log_message = f"{first_name} {last_name} sent a sticker"
        
        self.logger.info(log_message)
        
        context.bot.send_message(chat_id, 'Стикер? Ладно.')