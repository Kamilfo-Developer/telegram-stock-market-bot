from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, dispatcher, MessageHandler
from telegram.ext.filters import Filters
from bot.data_modules.msm_share import MSMShare
from bot.data_modules.userfavouriteshares import UserFavouriteShares
from bot.data_modules.cbrates import CBRates
import logging
import bot.config as config

class Bot:
    def __init__(self, token):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        
        self.logger = logging.getLogger()
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        
        #Making handlers
        message_handler = MessageHandler(Filters.text & (~Filters.command), 
                                         self.handle_message)
        
        sticker_handler = MessageHandler(Filters.sticker & (~Filters.command & ~Filters.text), 
                                         self.handle_sticker)
        
        start_handler = CommandHandler("start", self.handle_start)
        get_rates_handler = CommandHandler("getrates", self.handle_get_rates)
        get_favourite_handler = CommandHandler("getfavourite", self.handle_get_favourite)
        clear_favourite = CommandHandler("clearfavourite", self.handle_clear_favourite)
        
        #Setting handlers
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(sticker_handler)
        self.dispatcher.add_handler(get_rates_handler)
        self.dispatcher.add_handler(get_favourite_handler)
        self.dispatcher.add_handler(clear_favourite)
    
    def start(self):
        self.updater.start_polling()
    
    def handle_start(self, update, context):
        chat_id = update.effective_chat.id
        first_name = update.effective_chat.first_name
        last_name = update.effective_chat.last_name or ""
        
        bot_name = context.bot.get_me().first_name
        
        path = config.START_STICKER_PATH
        
        if path: 
            sti = open(path, 'rb')
            context.bot.send_sticker(chat_id, sti)
        
        message = f"Доброго времени суток{f', {first_name}' if first_name else ''}!\nЯ - {bot_name}, биржевой бот, благодаря которому Вы можете узнать котировки акций и курс валют ЦБ РФ.\nНа данный момент доступны только акции Московской биржи. Это означает, что бот не может получить котировки акций \"Apple\", \"Google\" или \"Amazon\".\nТакже Вы можете получить основные курсы валют ЦБ РФ к рублю, введя команду \"/getrates\", или выбрав её в меню команд.\nЧтобы получить доступ к цене непосредственно акции, просто отправьте её MCX в любом регистре. Например, <b>\"YNDX\"</b> или <b>\"GaZp\"</b>.\nЕщё Вы можете добавлять акции в избранное, для этого просто отправьте MCX акции, а затем, на появившейся клавиатуре выберите \"Добавить в избранное [MCX акции]\".\nЗатем, когда Вы захотите увидеть стоимость избранных акций, введите \n\"/getfavourite\". Аналогично можно удалить акцию из списка. Если Вы хотите мгновенно удалить все акции, просто введите команду \n\"/clearfavourite\" и список будет полностью очищен.\nПриятного пользования!"
        
        context.bot.send_message(chat_id, message, parse_mode="html")
        
        self.logger.info(f"Пользователь {first_name} {last_name} выбрал команду start")

    def handle_get_favourite(self, update, context):
        chat_id = update.effective_chat.id
        first_name = update.effective_chat.first_name
        last_name = update.effective_chat.last_name
            
        message = "Стоимость избранных акций:\n"
        log_message = f"{first_name} {last_name or ''} запросил список избранного"
        favourite_shares = UserFavouriteShares(chat_id).get_favourite_shares()
            
        if not favourite_shares:
            message = "У вас пока нет избранных акций😅\nПопробуйте ввести MCX акции, например \"YNDX\"."
        for mcx in favourite_shares:
            share = MSMShare(mcx)
            message += f"{mcx} ({share.get_share_name()}): <b>{share.get_share_price()}</b>₽\n"
            
        self.logger.info(log_message)
        
        context.bot.send_message(chat_id, message, parse_mode="html")
                
            
    def handle_clear_favourite(self, update, context):
        chat_id = update.effective_chat.id
            
        UserFavouriteShares(chat_id).clear_favourite_shares()
            
        context.bot.send_message(chat_id, f"Список избранных акций был очищен.")

    def handle_get_rates(self, update, context):
        chat_id = update.effective_chat.id
        first_name = update.effective_chat.first_name
        last_name = update.effective_chat.last_name
            
        try:
            CB_exchange_rates = CBRates()
            CB_exchange_rates_previous = CB_exchange_rates.get_previous_exchange_rates()
            
            NEEDED_RATES = config.VALUTES
                
            message = "🏦\nКурсы ЦБ валют к рублю:\n"
                
            prices = CB_exchange_rates.data["prices"]
            previous_price = CB_exchange_rates_previous.data["prices"]
                
            names = CB_exchange_rates.data["names"]
            nominal = CB_exchange_rates.data["nominal"]
                
            for key in NEEDED_RATES:
                if prices[key] > previous_price[key]:
                    sign = '⏫'
                elif prices[key] < previous_price[key]:
                    sign = '⏬'
                else:
                    sign = ''
                    
                message += f"{nominal[key]} {names[key][0].lower() + names[key][1:]}:\n<b>{prices[key]}</b>{sign}\n"
                
                
            log_message = f"{first_name} {last_name or ''} запросил курс валют"
        except ConnectionError:
            message = "Извините, что-то пошло не так, попробуйте повторить запрос через несколько секунд."
            log_message = f"{first_name} {last_name or ''} запросил курс валют слишком много раз"
                
        self.logger.info(log_message)
        context.bot.send_message(chat_id, message, parse_mode="html")
                
    def handle_message(self, update, context):
        chat_id = update.effective_chat.id
        first_name = update.effective_chat.first_name
        last_name = update.effective_chat.last_name
        text = update.message.text
        reply_keyboard = [[]]
            
        if "Добавить в избранное:" in text:
            mcx = f"{text[-4]}{text[-3]}{text[-2]}{text[-1]}"
            userFavouriteShares = UserFavouriteShares(chat_id)
            
            if not mcx in userFavouriteShares.get_favourite_shares():
                userFavouriteShares.add_favourite_share(mcx)
                message = f"Акция \"{mcx}\" была добавлена в избранное.\nВведите команду \"/getfavourite\", чтобы увидеть стоимость избранных акций."
                log_message = f"{first_name} {last_name or ''} добавил акцию {mcx} в избранное"
            
            else:
                message = f"Акция \"{mcx}\" уже в Вашем списке избранных акций🤷‍♂️"
                log_message = f"{first_name} {last_name or ''} попытался добавить {mcx} в избранное, но эта акция уже была в списке"
            
        elif "Удалить из избранного:" in text:
            mcx = f"{text[-4]}{text[-3]}{text[-2]}{text[-1]}"
            userFavouriteShares = UserFavouriteShares(chat_id)
            
            if mcx in userFavouriteShares.get_favourite_shares():  
                UserFavouriteShares(chat_id).remove_from_favourite_shares(mcx)
                message = f"Акция \"{mcx}\" была удалена из избранного.\nВведите команду \"/getfavourite\", чтобы увидеть стоимость избранных акций."
                log_message = f"{first_name} {last_name or ''} удалил акцию {mcx} из избранного"
            
            else:
                message = f"Акции \"{mcx}\ и так нет в Вашем списке избранных акций🤷‍♂️"
            
        else:
            try:
                share = MSMShare(text)
                price = share.get_share_price()
                share_name = share.get_share_name()
                    
                log_message = f"{first_name} {last_name or ''} запросил акцию {text}, стоимость которой составляет {price}₽"
                message = f"По данным Московской биржи, стоимость акций {share_name} составляет <b>{price}</b>₽."
                    
                if not text.upper() in UserFavouriteShares(chat_id).get_favourite_shares():
                    reply_keyboard = [    
                        [KeyboardButton(f"Добавить в избранное: {text.upper()}")]
                    ]
            
                else:
                    reply_keyboard = [    
                        [KeyboardButton(f"Удалить из избранного: {text.upper()}")]
                    ]
            
            except ValueError:
                message = "Упс... Похоже такой акции нет..."
                log_message = f"{first_name} {last_name or ''} запросил несуществующую акцию. Ввод: {text}"
                
        self.logger.info(log_message)
        
        context.bot.send_message(chat_id, message, parse_mode="html", reply_markup=ReplyKeyboardMarkup(keyboard=(reply_keyboard or ""), one_time_keyboard=True, resize_keyboard=True))

    def handle_sticker(self, update, context):
        chat_id = update.effective_chat.id
        first_name = update.effective_chat.first_name
        last_name = update.effective_chat.last_name or ""
        
        log_message = f"{first_name} {last_name} прислал стикер"
        
        self.logger.info(log_message)
        
        context.bot.send_message(chat_id, 'Стикер? Ладно.')