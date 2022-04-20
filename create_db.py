import collections
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
            id_to_all[str(card["id"])]["deck_types_info"] = None
    cur = connection.cursor()
    sqlReq = "SELECT * FROM card_info"
    cur.execute(sqlReq)
    info = cur.fetchall()
    # cnt = 0
    # w =  open('error.txt','w')
    # for i, (id, name, card_info, deck_info) in enumerate(info):
    #     try:
    #         card_info = json.loads(card_info)[0]
    #         test = card_info['deckTypes']
    #     except:
    #         print(id,name,card_info,deck_info)
    #         w.write(id+' '+name+'\n')
    #         continue
    #     deck_info = json.loads(deck_info)
    #     if type(deck_info) is dict:
    #         if not deck_info["deckTypesInfo"]:
    #             continue
    #     else:
    #         w.write(id + ' ' + name+ '\n')
    #         cnt+=1
    #         continue
    # print(cnt)
    for i, (id, name, card_info, deck_info) in enumerate(info):
        card_info = json.loads(card_info)[0]
        if json.loads(deck_info)['deckTypesInfo']:
            deck_info_dic = collections.defaultdict(list)
            for dic in json.loads(deck_info)['deckTypesInfo']:
                for percent in dic['cardCountPercentages']:
                    deck_info_dic[dic['name']].append(str(percent['percentage'])+"%")
                deck_info_dic[dic['name']].append(str(dic['avgCopies']))
        else:
            deck_info_dic = None
        if id in id_to_all.keys():
            id_to_all[id]["deck_used"] =  card_info['deckTypes']
            id_to_all[id]["deck_types_info"] =  deck_info_dic
            if "rarity" in card_info.keys():
                id_to_all[id]["rarity"] = card_info['rarity']

json.dump(id_to_all,open("data.json","w"))

    # deck_type = set()
    # max_length = 0
    # with open('deck_type.txt','w') as w:
    #     for i,(id,name,card_info,deck_info) in enumerate(info):
    #         try:
    #             card_info = json.loads(card_info)[0]
    #             test = card_info['deckTypes']
    #         except:
    #             print(id,name,card_info)
    #             continue
    #         if card_info['deckTypes']:
    #             for deck in card_info['deckTypes']:
    #                 max_length = max(max_length,len(deck))
    #                 deck_type.add(deck)
    #     for deck in list(deck_type):
    #         w.write(deck+'\n')
    # print(max_length)