import json
import sqlite3 as sql
from collections import defaultdict
id_to_all = defaultdict(lambda: defaultdict(str))
with sql.connect("website.cdb") as connection:
    for language in ["en-US","ja-JP","zh-CN","zh-TW","ko-KR"]:
        cards= json.load(open("C:\\Users\\10601\\Documents\\GitHub\\mdt\\database\\ygopro_db\\"+language+".json",encoding='UTF-8'))
        print(len(cards))
        for card in cards:
            id_to_all[str(card["id"])][language+"_name"] = card["name"]
            id_to_all[str(card["id"])][language+"_desc"] = card["desc"]
            id_to_all[str(card["id"])]["rarity"] = None
            id_to_all[str(card["id"])]["deck_used"] = None
    cur = connection.cursor()
    sqlReq = "SELECT * FROM card_info"
    cur.execute(sqlReq)
    info = cur.fetchall()
    cnt = 0
    for i, (id, name, card_info, deck_info) in enumerate(info):
        card_info = json.loads(card_info)[0]
        # deck_info = json.loads(deck_info)
        # if type(deck_info) is dict:
        #     if not deck_info["deckTypesInfo"]:
        #         continue
        # else:
        #     cnt+=1
        #     print(deck_info)
        #     continue
        # print(deck_info["deckTypesInfo"])
        # exit()
        if id in id_to_all.keys():
            id_to_all[id]["deck_used"] =  card_info['deckTypes']
            if "rarity" in card_info.keys():
                id_to_all[id]["rarity"] = card_info['rarity']

json.dump(id_to_all,open("data.json","w"))

    #                 deck_type.add(deck)
    # deck_type = set()
    # with open('deck_type.txt','w') as w:
    #     for i,(id,name,card_info,deck_info) in enumerate(info):
    #         try:
    #             card_info = json.loads(card_info)[0]
    #             test = card_info['deckTypes']
    #         except:
    #             print(id,name)
    #             continue
    #         if card_info['deckTypes']:
    #             for deck in card_info['deckTypes']:
    #                 deck_type.add(deck)
    #     for deck in list(deck_type):
    #         w.write(deck+'\n')
