from xml.dom import minidom
from bot.utils.date import Date
from datetime import date as dt
import requests

class CBRates:
    
    def __init__(self, day=Date.get_current_day(), 
                 month=Date.get_current_month(), 
                 year=Date.get_current_year()) -> None:
        
        self.date = Date(day, month, year)
        self.data = self.__get_CB_exchange_rates()

    def __get_CB_exchange_rates(self):
        date = self.date
        
        if (dt.today().day == date.day and date.month == dt.today().month and date.year == dt.today().year):
            req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
        else: 
            req = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.get_formated_date()}")
        #https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off
        
        if (req.status_code != 200): 
            return req.status_code
        
        parsed = minidom.parseString(req.text)
        
        items = parsed.getElementsByTagName("Valute")

        result = dict()
        
        for valute in items:
            current_valute = valute.childNodes[1].firstChild.nodeValue
            
            result[valute.childNodes[1].firstChild.nodeValue] = {}
            
            result[current_valute]["price"] = float(valute.childNodes[4].firstChild.nodeValue.replace(",", "."))
            result[current_valute]["name"] = valute.childNodes[3].firstChild.nodeValue
            result[current_valute]["nominal"] = valute.childNodes[2].firstChild.nodeValue
        
        return result
    
    def get_previous_exchange_rates(self):
        date = self.date
        current_exchange_rates = self.data
        
        prev_date = date.get_previous_day_date()
        previous_exchange_rates = CBRates(prev_date.day, prev_date.month, prev_date.year)
        
        
        while previous_exchange_rates.data == current_exchange_rates:
            previous_exchange_rates = CBRates(prev_date.day, prev_date.month, prev_date.year)
            prev_date = prev_date.get_previous_day_date()
    
        return previous_exchange_rates

print(CBRates().data['USD']['price'])