import os
import requests
import json
import pandas

from codeparts.data import Constants

sess = requests.Session()


class checkers():
    def __init__(self) -> None:
        path = os.getcwd()
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))

    def skins_en(self, account) -> None:
        # riot api counts latam and br as NA so u have to do this shit
        region = account.region
        if region.lower() == 'latam' or region.lower() == 'br':
            region = 'na'
        try:
            headers = {
                "X-Riot-Entitlements-JWT": account.entt,
                "Authorization": f"Bearer {account.token}"
            }

            # get skins using api
            r = sess.get(
                f"https://pd.{region}.a.pvp.net/store/v1/entitlements/{account.puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433", headers=headers)
            # input(r.text)
            Skins = r.json()["Entitlements"]
            # file with skins' names
            with open(f'{self.parentpath}\\src\\assets\\skins.json', 'r', encoding='utf-8') as f:
                response = json.load(f)

            # there could be a list but im 1 iq
            skinlist = []
            skinids = []
            for skin in Skins:
                # find skin's name by it's id
                try:
                    skinid = skin['ItemID']
                    for i in response['data']:
                        if skinid in str(i):
                            if i['displayName'] in skinlist:
                                break
                            skinlist.append(i['displayName'])
                            skinids.append(skinid.strip())
                            break

                except Exception as e:
                    #input(e)
                    pass

            #input(skinlist)
            account.skins = skinlist
            account.uuids = skinids
        except Exception as e:
            input(e)
            account.skins = ['N/A']

    def balance(self, account) -> None:
        region = account.region
        if region.lower() == 'latam' or region.lower() == 'br':
            region = 'na'
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {account.token}",
                   "X-Riot-Entitlements-JWT": account.entt,
                   }
        try:
            r = requests.get(
                f"https://pd.{region}.a.pvp.net/store/v1/wallet/{account.puuid}", headers=headers)
            # input(r.text)

            vp = int(r.json()["Balances"]
                     ["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"])
            rp = int(r.json()["Balances"]
                     ["e59aa87c-4cbf-517a-5983-6e81511be9b7"])
        except:
            vp = 'N/A'
            rp = 'N/A'
        account.vp = vp
        account.rp = rp

    def ranked(self, account) -> None:
        region = account.region
        if region.lower() == 'latam' or region.lower() == 'br':
            region = 'na'
        try:

            if account.entt == False:
                return False
            RankIDtoRank = {"0": "Unranked", "1": "", "2": "", "3": "Iron 1", "4": "Iron 2", "5": "Iron 3",
                            "6": "Bronze 1", "7": "Bronze 2", "8": "Bronze 3", "9": "Silver 1", "10": "Silver 2", "11": "Silver 3", "12": "Gold 1",
                            "13": "Gold 2", "14": "Gold 3", "15": "Platinum 1", "16": "Platinum 2", "17": "Platinum 3", "18": "Diamond 1", "19": "Diamond 2", "20": "Diamond 3", "21": "Ascendant 1", "22": "Ascendant 2", "23": "Ascendant 3", "24": "Immortal 1", "25": "Immortal 2", "26": "Immortal 3", "27": "Radiant"}
            headers = {"Content-Type": "application/json",
                       "Authorization": f"Bearer {account.token}",
                       "X-Riot-Entitlements-JWT": account.entt,
                       "X-Riot-ClientVersion": "release-05.12-shipping-21-808353",
                       "X-Riot-ClientPlatform": Constants.CLIENTPLATFORM}
            ranked = sess.get(
                f"https://pd.{region}.a.pvp.net/mmr/v1/players/{account.puuid}/competitiveupdates", headers=headers)
            if '","Matches":[]}' in ranked.text:
                rank = "unranked"
            else:
                # input(ranked.json())
                rankid = str(ranked.json()['Matches'][0]['TierAfterUpdate'])
                account.lastplayed = pandas.to_datetime(ranked.json()['Matches'][0]['MatchStartTime'], unit='ms')
                rank = RankIDtoRank[rankid]
            account.rank = rank
        except Exception as e:
            # input(e)
            account.rank = 'err'

    def lastplayed(self, account):
        region = account.region
        if region.lower() == 'latam' or region.lower() == 'br':
            region = 'na'
        try:
            headers = {"Content-Type": "application/json",
                       "Authorization": f"Bearer {account.token}",
                       "X-Riot-Entitlements-JWT": account.entt,
                       "X-Riot-ClientVersion": "release-05.12-shipping-21-808353",
                       "X-Riot-ClientPlatform": Constants.CLIENTPLATFORM
                       }
            r = requests.get(
                f"https://pd.{region}.a.pvp.net/match-history/v1/history/{account.puuid}?startIndex=0&endIndex=10", headers=headers)
            data = r.json()
            # input(data)
            data2 = data["History"]
            if data2 == []:
                if account.lastplayed is None:
                    account.lastplayed = 'long time ago'
                return
            #print(data2)
            data3 = data2[0]['GameStartTime']
            unix_time1 = data3
            unix_time1 = int(unix_time1)
            result_s2 = pandas.to_datetime(unix_time1, unit='ms')
            time = str(result_s2)
        except Exception as e:
            #print(e)
            time = "N/A"
        account.lastplayed = time

    def skinprice(self, skin: str):
        try:
            price = Constants.skinprice[skin]
        except:
            price = 0
        return price
