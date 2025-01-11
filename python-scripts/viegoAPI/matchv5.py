import requests
import time
class MatchV5:
    
    def __init__(self, api_key,base_url, max_retries):
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
    Query parameters
    startTime (long): Epoch timestamp in SECONDS. the start of this is june 16th 2021
    endTime (long): Epoch timestamp in SECONDS 
    queue (int): each queue has a number assosiated, which you can find here https://static.developer.riotgames.com/docs/lol/queues.json
    type (string): filter by match type, which can be found here https://static.developer.riotgames.com/docs/lol/gameTypes.json
    start (int): from which index do you want to start selectiing the matchlist, default 0
    count (int): number of matches requested, from 0 to 100, default 20
    region (string): region

    """
    def matches_by_puuid(self,puuid, region,  queue=None, type=None, startTime=None, endTime=None, start=0, count=20):
        request_url = f"https://{region}.api.riotgames.com/{self.base_url}by-puuid/{puuid}/ids"
        params ={
            "queue": queue,
            "type": type,
            "startTime": startTime,
            "endTime": endTime,
            "start": start,
            "count": count
        }
        header ={
            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url,header, params)
    
    """
    returns all the match info with said id
    """
    def match_by_id(self, matchId, region):
        request_url = f"https://{region}.api.riotgames.com/{self.base_url}{matchId}"
        header ={
            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header)
    
    """
    returns the timeline of a match with said id
    """
    def match_timeline_by_id(self,matchId, region):
        request_url = f"https://{region}.api.riotgames.com/{self.base_url}{matchId}/timeline"
        header ={
            "X-Riot-Token": self.api_key
        }
        return self.request_handler(request_url, header)

    


