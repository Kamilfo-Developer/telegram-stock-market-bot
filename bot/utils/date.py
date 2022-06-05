from datetime import date as dt

class Date:
    LAST_DAYS_OF_MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    def __init__(self, day: int | str = dt.today().day, month: int | str = dt.today().month, year: int | str = dt.today().year) -> None:
        
        try:
            day = int(day)
            
        except ValueError:
            raise ValueError("Incorrect day passed. Make sure it can be parsed to the integer type.")
        
        try:
            month = int(month)
        
        except ValueError:
            raise ValueError("Incorrect month passed. Make sure it can be parsed to the integer type.")
        
        try:
            year = int(year)
        
        except ValueError:
            raise ValueError("Incorrect year passed. Make sure it can be parsed to the integer type.")
        
        self.__year = year
        
        if (month < 1 or month > 12):
            raise ValueError("Month must be in range from 1 to 12")
        self.__month = month
        
        if (not Date.is_day_of_month_valid(day, month, year)):
            raise ValueError("No such day in this month")
        self.__day = day
    
    def __str__(self) -> str:
        return self.get_formated_date()
    
    @property
    def day(self):
        return self.__day
    
    @day.setter
    def day(self, value):
        raise AttributeError("The day property is not supposed to be changed")

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, value):
        raise AttributeError("The year property is not supposed to be changed")
    
    @property
    def year(self):
        return self.__year
    
    @year.setter
    def year(self, value):
        raise AttributeError("The day property is not supposed to be changed")    
    
    def get_current_day(self=None) -> int:
        return dt.today().day
    
    def get_current_month(self=None) -> int:
        return dt.today().month
    
    def get_current_year(self=None) -> int:
        return dt.today().year
    
    def is_day_of_month_valid(day, month, year) -> bool:
        """
        Checks if month contains day.
        
        Args:
            day (int): day to check
            month (int): month to check
            year (int): year

        Returns:
            bool: returns True if month contains day. Else returns False. 
        """
        
        if day < 1 or day > Date.LAST_DAYS_OF_MONTHS[month - 1]:
            #if the year is leap
            if month == 2 and year % 4 == 0:
                if day <= 29:
                    return True

                return False
        
        return True
    
    def get_formated_date(self, separator="-", reversed=False) -> str:
        """Returns date string in format "day-month-year" if no separator given, else returns "day{separator}month{separator}year".
        If reversed = True return string in format "year{separator}month{separator}day"
        

        Args:
            separator (str, optional): the string will separate the numbers. Defaults to "-".
            reversed (bool, optional): if needed a reversed date string, set this argument to True. Defaults to False.

        Returns:
            str: formated date string
        """
        
        day = self.__day
        month = self.__month
        year = self.__year
        
        if day < 10:
            day = f"0{day}"
        if month < 10:
            month = f"0{month}"
        
        return f"{day}{separator}{month}{separator}{year}" if not reversed else f"{year}{separator}{month}{separator}{day}" 
    
    def get_previous_day_date(self):
        """Returns previous date as Date instance object

        Returns:
            date: a Date instance object
        """
        
        day = self.__day - 1
        month = self.__month
        year = self.__year

        
        if day == 0:
            if month == 3 and year % 4 == 0:
                return Date(29, 2, year)

            month -= 1
            
            if month == 0:
                year -= 1
                month = 12
            
                
            day = self.LAST_DAYS_OF_MONTHS[month - 1]
        
        return Date(day, month, year)
    
    def get_next_day_date(self):
        """Returns next date as Date instance object

        Returns:
            date: a Date instance object
        """
        
        day = self.__day
        month = self.__month
        year = self.__year
        
        day += 1
        
        if day > self.LAST_DAYS_OF_MONTHS[month - 1]:
            if year % 4 == 0 and month == 2 and day == 29:
                return Date(29, month, year)
            elif year % 4 == 0 and month == 2 and day == 30:
                return Date(1, month + 1, year)
            else:
                day = 1
                month += 1
                if month == 13:
                    year += 1
                    month = 1
        
        return Date(day=day, month=month, year=year)         
