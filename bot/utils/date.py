from datetime import date as dt

class Date:
    
    last_days_of_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    def __init__(self, day=dt.today().day, month=dt.today().month, year=dt.today().year):
        self.year = year
        
        if (month < 1 or month > 12):
            raise ValueError("Month must be in range from 1 to 12")
        self.month = month
        
        if (not self.__is_day_of_month_valid(day, month, year)):
            raise ValueError("No such day in this month")
        self.day = day
    
    def get_current_day():
        return dt.today().day
    
    def get_current_month():
        return dt.today().month
    
    def get_current_year():
        return dt.today().year
    
    def __is_day_of_month_valid(self, day, month, year) -> bool:
        """
        Checks if month contains day.
        
        Args:
            day (int): day to check
            month (int): month for checking
            year (int): year that contains "month"

        Returns:
            bool: returns True if month contains day. Else returns False. 
        """
        
        if day < 1 or day > self.last_days_of_months[month - 1]:
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
        day = self.day
        month = self.month
        year = self.year
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
        day = self.day
        month = self.month
        year = self.year
        
        day -= 1
        
        if day == 0:
            if month == 3 and year % 4 == 0:
                return Date(29, 2, year)

            month -= 1
            
            if month == 0:
                year -= 1
                month = 12
            
                
            day = self.last_days_of_months[month - 1]
        
        return Date(day, month, year)
    
    def get_next_day_date(self):
        """Returns next date as Date instance object

        Returns:
            date: a Date instance object
        """
        day = self.day
        month = self.month
        year = self.year
        
        day += 1
        
        if day > self.last_days_of_months[month - 1]:
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
        
        return Date(day, month, year)         
