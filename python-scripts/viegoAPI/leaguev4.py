import requests
class LeagueV4:
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
    dont know what it returns but ok, queue could be 
    "RANKED_SOLO_5x5"
    RANKED_FLEX_SR
    RANKED_FLEX_TT
    REGION is different to region, this could ne NA1, LA1 LA2 etc
    """
    def challenger_league_by_queue(self, queue, REGION):
        request_url = f"https://{REGION}.api.riotgames.com/{self.base_url}challengerleagues/by-queue/{queue}"
        header = {

            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header)

    """
    gets the entries of the specific summoner
    """
    def entries_by_summonerId(self, summonerId, REGION):
        request_url = f"https://{REGION}.api.riotgames.com/{self.base_url}entries/by-summoner/{summonerId}"
        header = {

          "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header)
    
    """
    get all the entries of the specific queu tier, division and region you specify
    PATH PARAMETERS
        - queue(string): RANKED_SOLO_5x5, RANKED_FLEX_SR, RANKED_FLEX_TT
        - tier(string): DIAMOND, EMERALD, PLATINUM, GOLD, SILVER, BRONZE, IRON
        - division(string): I, II, III, IV
        - REGION(string): is different to region, this could ne NA1, LA1 LA2 etc
    QUERY PARAMTERS
        - page(int): default to 1, just which page of data you see, page 1 has the best, page 2 the seconds best and so forth
    """
    def all_entries(self, queue, tier, division, REGION, page = 1):
        request_url = f"https://{REGION.lower()}.api.riotgames.com/{self.base_url}entries/{queue}/{tier}/{division}"
        header = {
          "X-Riot-Token": self.api_key
        }
        params = {
            "page": page
        }
        return self.request_handler(request_url, header, params)
    
    """
    dont know what it returns but ok
    PATH PARAMETERS
        - queue(string): RANKED_SOLO_5x5, RANKED_FLEX_SR, RANKED_FLEX_TT
        - REGION(string): is different to region, this could ne NA1, LA1 LA2 etc
    """
    def grandmaster_leagues_by_queue(self, queue, REGION):
        request_url = f"https://{REGION.lower()}.api.riotgames.com/{self.base_url}grandmasterleagues/by-queue/{queue}"
        header = {

            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header)
    
    """
    dont know what it returns but ok
    PATH PARAMETERS
        - leagueId(string): leagueId
        - REGION(string): is different to region, this could ne NA1, LA1 LA2 etc
    """
    def league_by_leagueId(self, leagueId, REGION):
        request_url = f"https://{REGION.lower()}.api.riotgames.com/{self.base_url}leagues/{leagueId}"
        header = {

            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header)
    
    """
    dont know what it returns but ok
    PATH PARAMETERS
        - queue(string): RANKED_SOLO_5x5, RANKED_FLEX_SR, RANKED_FLEX_TT
        - REGION(string): is different to region, this could ne NA1, LA1 LA2 etc
    """
    def master_leagues_by_queue(self, queue, REGION):
        request_url = f"https://{REGION.lower()}.api.riotgames.com/{self.base_url}masterleagues/by-queue/{queue}"
        header = {

            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header)

    
