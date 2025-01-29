import pandas as pd
import numpy as np
import json
import os
from viegoAPI import ViegoAPI
import sys

region = sys.argv[1].lower() #TEST , SHOULD CHANGE DEPENDING OF THE REGION YOU WANT TO CONSULT
    
root_folder = f"./{region.lower()}-ids/"

output_file = f"{region}-ids.csv"
progress_file = f"{region}-ids-progress.json"
    
def processIdData(id_data):
    if len(id_data) == 0:
        return  pd.DataFrame()
    header_columns = ["leagueId", "summonerId", "tier", "rank"]
    df = pd.DataFrame(columns=header_columns)
    for i in range(len(id_data)):
        col = {"leagueId":id_data[i]["leagueId"],"summonerId":id_data[i]["summonerId"],"tier": id_data[i]["tier"],"rank":id_data[i]["rank"] }
        df.loc[i] = col

    return df

def processIdDataTop(id_data):
    tier = id_data["tier"]
    rank = "I"
    entries = id_data["entries"]
    header_columns = ["leagueId", "summonerId", "tier", "rank"]
    df = pd.DataFrame(columns=header_columns)
    
    for i in range(len(id_data["entries"])):
        col = {"leagueId": pd.NA, "summonerId":entries[i]["summonerId"], "tier":tier, "rank":rank}
        df.loc[i] = col
        
    return df

def writeJson(data):
    with open(root_folder + progress_file,"w") as f:
        json.dump(data,f)
        
    
if __name__ == "__main__":
    ### FILE OPENING AND SETUP ###
    with open("./api_key.txt", "r") as f:
        api_key = f.readlines()[0]
        
    viego = ViegoAPI(api_key,3)
    queue = "RANKED_SOLO_5x5"
    tiers = ["EMERALD", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
    divisions = ["IV", "III", "II", "I"]
    
    header_columns = ["leagueId", "summonerId", "tier", "rank"]
    output_csv = pd.DataFrame(columns=header_columns)

    progress_json = {
        "tier_index": tiers[0],
        "division_index": divisions[0],
        "page": 1
    }
    if not os.path.exists(root_folder):
        os.mkdir(root_folder)
        
    if os.path.isfile(root_folder + output_file):
        output_csv = pd.read_csv(root_folder + output_file)

    if os.path.isfile(root_folder + progress_file):
        with open(root_folder + progress_file, "r") as f:
            progress_json = json.load(f)

    last_tier = progress_json["tier_index"]
    last_division = progress_json["division_index"]
    last_page = progress_json["page"]

    tiers = tiers[tiers.index(last_tier):]
    divisions = divisions[divisions.index(last_division):]
    page = last_page
    end_of_page = False
    # viego.leaguev4.debug = True
    for tier in tiers:
        progress_json["tier_index"] = tier
        writeJson(progress_json)
        if tier == "MASTER":
            master =    processIdDataTop(viego.leaguev4.master_leagues_by_queue(queue, region))
            output_csv = pd.concat([output_csv, master])
            
            output_csv.to_csv(root_folder + output_file, encoding='utf-8', index=False)
        if tier == "GRANDMASTER":
            grand_master = processIdDataTop(viego.leaguev4.grandmaster_leagues_by_queue(queue, region))
            output_csv = pd.concat([output_csv, grand_master])
            
            output_csv.to_csv(root_folder + output_file, encoding='utf-8', index=False)
        if tier == "CHALLENGER":
            challenger = processIdDataTop(viego.leaguev4.challenger_league_by_queue(queue, region))
            
            output_csv = pd.concat([output_csv, challenger])
            
            output_csv.to_csv(root_folder + output_file, encoding='utf-8', index=False)
            
        if tier == "DIAMOND" or tier == "EMERALD":
            for division in divisions:
                progress_json["division_index"] = division
                writeJson(progress_json)
                while not end_of_page:
                    progress_json["page"] = page
                    writeJson(progress_json)
                    data = viego.leaguev4.all_entries(queue,tier,division,region,page)
                    if data != False:
                        
                        # process data
                        extracted_df = processIdData(data)
                        if extracted_df.empty:
                            print(f"[I] in page {page} there was no players")
                            end_of_page = True
                        else:  
                            output_csv = pd.concat([output_csv,extracted_df])
                            output_csv.to_csv(root_folder + output_file, encoding='utf-8', index=False)
                        
                    else: pass  
                    page += 1
                    
                page = 1
                end_of_page = False
            page = 1
            end_of_page = False
            divisions = ["IV", "III", "II", "I"]
        
        
        