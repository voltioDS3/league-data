
from .matchv5 import MatchV5
from .accountv1 import AccountV1
from .leaguev4 import LeagueV4
class ViegoAPI:
    def __init__(self, api_key, max_retries):
        self.api_key = api_key
        self.matchv5 = MatchV5(api_key, "lol/match/v5/matches/", max_retries=max_retries)
        self.accountv1 = AccountV1(api_key= self.api_key, base_url="riot/account/v1/", max_retries=max_retries)
        self.leaguev4 = LeagueV4(api_key=self.api_key, base_url="lol/league/v4/", max_retries=max_retries)
        
        