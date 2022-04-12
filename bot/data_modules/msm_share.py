from urllib.error import HTTPError
import requests
import json

class MSMShare:
    
    def __init__(self, mcx) -> None:
        self.__data = self.__get_share_data(mcx)
        if not self.__check_if_share_exists():
            raise ValueError("No share with such name.")

    def __get_share_data(self, mcx) -> dict:    
        """
        Access moex.com and gets json then returns dict with share data if the request was successful,
        else raises an HTTPError.

        Args:
            name (str): name of a share. Defaults to None.

        Returns:
            dict: returns dict with share data from moex.com or HTTP status code.
        """
        
        req = requests.get(url=f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{mcx}.json?iss.meta=off")
    
        if (str(req.status_code)[0] == "5"): 
            raise HTTPError(f"Server of MOEX is not available at the moment. Status code: {req.status_code}")
        
        parsed = json.loads(req.text)
    
        return parsed
    
    def __check_if_share_exists(self):
        return len(self.__data["securities"]["data"]) != 0
    
    def get_share_price(self) -> int:
        """Returns the price of the share from TQBR

        Returns:
            int: price of the share
        """
        
        for data_arr in self.__data["marketdata"]["data"]:
            if data_arr[1] == "TQBR":
                return int(data_arr[12] or data_arr[24])
            
        if len(self.__data["securities"]["data"]) == 0:
            return 0
        
        return int(self.__data["marketdata"]["data"][1][12])

    def get_share_name(self) -> str:
        """Returns name of the share

        Returns:
            str: name of the share
        """
        
        return self.__data["securities"]["data"][0][2]
