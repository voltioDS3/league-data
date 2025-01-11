import requests
import time
class AccountV1:
    def __init__(self, api_key, base_url, max_retries):
        self.api_key = api_key
        self.base_url = base_url
        self.max_retries = max_retries
        
    def request_handler(self, url, header,params = None):
        tries = 0
        
        while tries < self.max_retries:
            try:
                response = requests.get(url, params=params, headers=header )
                response.raise_for_status() 
                tries += 1
                if response.status_code == 429:
                    time.sleep(90)
                    continue
                else:
                    return response.json()
                
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                continue
                return None
            
            except requests.exceptions.ConnectionError:
                print("Error connecting to the API.")
                continue
                return None
            
            except requests.exceptions.Timeout:
                print("The request timed out.")
                continue
                return None
            
            except requests.exceptions.RequestException as err:
                print(f"An error occurred: {err}")
                continue
                return None
        
        return None
    """
    Returns the puuid, gameName and tagLine of the user just with the puuid 
    """
    def account_by_puuid(self, puuid, region):
        request_url = f"https://{region}.api.riotgames.com/{self.base_url}accounts/by-puuid/{puuid}"
        header ={
            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header=header)
    
    """
    Returns the puuid, ganeName and tagLine of the user just with the gameName and tagLine
    """
    def account_by_riot_id(self, tagLine, gameName, region):
        request_url = f"https://{region}.api.riotgames.com/{self.base_url}accounts/by-riot-id/{gameName}/{tagLine}"
        header = {
            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header = header)
        
