from urllib.error import HTTPError
from xml.dom import minidom
from bot.utils.date import Date
import bot.config as config
import pymongo
import requests
import json
import time 

class CBRates:
    
    def __init__(self, date: tuple = (Date.get_current_day(), 
                 Date.get_current_month(), 
                 Date.get_current_year())) -> None:
        try:
            self.__date = Date(date[0], date[1], date[2])
        except (ValueError, IndexError):
            raise ValueError("Incorrect date passed. Make sure it is a tuple of next format (day, month, year) and day, month and year can be parsed to the integer type.")
        
        self.__data = self.__get_CB_exchange_rates()
            
    @property
    def date(self):
        return self.__date
    
    @date.setter
    def date(self, value):
        raise AttributeError("\"date\" property is not allowed to be changed.")
    
    @property
    def data(self):
        return self.__data
    
    @date.setter
    def date(self, value):
        raise AttributeError("\"data\" property is not allowed to be changed.")

    def __require_CB_exchange_rates(self, date: Date) -> dict:
        req = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.get_formated_date()}")
        #https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off
        
        if (str(req.status_code)[0] == "5"): 
            raise HTTPError(f"Server of Central Bank of Russia is not available at the moment. Status code: {req.status_code}")
        
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
    
    def __get_CB_exchange_rates(self) -> dict:
        """Gets CB exchange rates.
        If cache used the method returns data either from the cache database or from the official CB API if more than CACHE_INTERVAL in seconds passed since the last try  

        Returns:
            dict: the CB rates data
        """
        date = self.__date
        
        if config.USE_CACHE:
            DB_client = pymongo.MongoClient("mongodb://localhost:27017")

            DB = DB_client["cache"]

            cache = DB["CB_cache"]        
            
            formated_date = date.get_formated_date()
            
            cache_data = cache.find_one({"date": formated_date})

            if not cache_data or time.time() - cache_data["timestamp_of_insertion"] > config.CACHE_INTERVAL:

                data = self.__require_CB_exchange_rates(date)
                
                json_data = json.dumps(data)
                    
                cache.delete_one({"date": formated_date})
                cache.insert_one({"date": formated_date, "data": json_data, "timestamp_of_insertion": time.time()})
                    
                return data
                      
            return json.loads(cache_data["data"])
        
        return self.__require_CB_exchange_rates(date)
        
    def get_previous_exchange_rates(self):
        """Returns the previous exchange rates  

        Returns:
            CBRates: instance of CBRates class that contains previous exchange rates data
        """
        
        date = self.__date
        current_exchange_rates = self.__data
        
        prev_date = date.get_previous_day_date()
        previous_exchange_rates = CBRates(date=(prev_date.day, prev_date.month, prev_date.year))
        
        #Here we check either previous day rates are equal to the current
        while previous_exchange_rates.data == current_exchange_rates:
            prev_date = prev_date.get_previous_day_date()
            previous_exchange_rates = CBRates(date=(prev_date.day, prev_date.month, prev_date.year))
            
        return previous_exchange_rates