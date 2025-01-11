from viegoAPI import ViegoAPI
with open("api_key.txt", "r") as f:
    api_key = f.readline()

viego = ViegoAPI(api_key)