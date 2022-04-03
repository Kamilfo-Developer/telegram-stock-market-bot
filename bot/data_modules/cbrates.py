from xml.dom import minidom
from bot.utils.date import Date
import bot.config as config
import pymongo
import requests
import json

class CBRates:
    
    def __init__(self, day=Date.get_current_day(), 
                 month=Date.get_current_month(), 
                 year=Date.get_current_year()) -> None:
        
        self.__date = Date(day, month, year).get_next_day_date()
        self.__data = self.__get_CB_exchange_rates()
        
    
    @property
    def date(self):
        return self.__date
    
    @date.setter
    def date(self, value):
        raise AttributeError("date property is not allowed to be changed.")
    
    @property
    def data(self):
        return self.__data
    
    @date.setter
    def date(self, value):
        raise AttributeError("data property is not allowed to be changed.")

    def __require_CB_exchange_rates(self, date: Date):
        req = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.get_formated_date()}")
        #https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off
        
        if (req.status_code != 200): 
            return req.status_code
        
        parsed = minidom.parseString(req.text)
        
        items = parsed.getElementsByTagName("Valute")

        result = dict()
        
        result["date"] = "-".join(parsed.getElementsByTagName("ValCurs")[0].getAttribute("Date").split('.'))
        
        for valute in items:
            current_valute = valute.childNodes[1].firstChild.nodeValue
            
            result[valute.childNodes[1].firstChild.nodeValue] = {}
            
            result[current_valute]["price"] = float(valute.childNodes[4].firstChild.nodeValue.replace(",", "."))
            result[current_valute]["name"] = valute.childNodes[3].firstChild.nodeValue
            result[current_valute]["nominal"] = valute.childNodes[2].firstChild.nodeValue
        
        return result
    
    def __get_CB_exchange_rates(self):
        date = self.__date
        
        DB_client = pymongo.MongoClient("mongodb://localhost:27017")

        DB = DB_client["cache"]

        cache = DB["CB_cache"]

        if config.USE_CACHE:
            
            formated_date = date.get_formated_date()

            cache_data = cache.find_one({"date": formated_date})
            
            if not cache_data:
                data = self.__require_CB_exchange_rates(date)
                
                day, month, year = data["date"].split("-")

                
                if Date(int(day), int(month), int(year)).get_formated_date() != date.get_previous_day_date().get_formated_date():
                    json_data = json.dumps(data)
                    
                    cache.insert_one({"date": formated_date, "data": json_data})
                    
                return data
            
            return json.loads(cache_data["data"])
        
        return self.__require_CB_exchange_rates(date)
        
    def get_previous_exchange_rates(self):
        date = self.__date
        current_exchange_rates = self.__data
        
        prev_date = date.get_previous_day_date()
        previous_exchange_rates = CBRates(prev_date.day, prev_date.month, prev_date.year)
        
        while previous_exchange_rates.data == current_exchange_rates:
            previous_exchange_rates = CBRates(prev_date.day, prev_date.month, prev_date.year)
            prev_date = prev_date.get_previous_day_date()
    
        return previous_exchange_rates