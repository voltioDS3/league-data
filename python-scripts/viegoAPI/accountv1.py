import requests
class AccountV1:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
    
    def request_handler(self, url, header,params = None ,):
        try:
            response = requests.get(url, params=params, headers=header )
            response.raise_for_status() 
        
            if response.status_code == 429:
                return -1
            else:
                return response.json()
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

            return None
        
        except requests.exceptions.ConnectionError:
            print("Error connecting to the API.")
            return None
        
        except requests.exceptions.Timeout:
            print("The request timed out.")
            return None
        
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
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
        
