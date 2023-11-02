import os
import traceback
from collections import OrderedDict
from re import compile
import ssl
from typing import Any
from tkinter import *

import pandas
import requests
from requests.adapters import HTTPAdapter

from codeparts import systems
from codeparts.data import Constants
from codeparts.systems import Account

syst = systems.system()


class SSLAdapter(HTTPAdapter):
	def init_poolmanager(self, *a: Any, **k: Any) -> None:
		c = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
		c.set_ciphers(':'.join(Constants.CIPHERS))
		k['ssl_context'] = c
		return super(SSLAdapter, self).init_poolmanager(*a, **k)


class auth():
    def __init__(self) -> None:
        path = os.getcwd()
        self.useragent = Constants.RIOTCLIENT
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))

    def auth(self, logpass: str = None, username=None, password=None, proxy=None) -> Account:
        account = Account()
        try:
            account.logpass = logpass
            headers = OrderedDict({
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "application/json, text/plain, */*",
                'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)'
            })
            session = requests.Session()
            session.headers = headers
            session.mount('https://', SSLAdapter())
            if username is None:
                username = logpass.split(':')[0].strip()
                password = logpass.split(':')[1].strip()

            data = {"acr_values": "urn:riot:bronze",
                    "claims": "",
                    "client_id": "riot-client",
                    "nonce": "oYnVwCSrlS5IHKh7iI16oQ",
                    "redirect_uri": "http://localhost/redirect",
                    "response_type": "token id_token",
                    "scope": "openid link ban lol_region"
                }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)'
            }
            try:
                r = session.post(Constants.AUTH_URL,
                                json=data, headers=headers, proxies=proxy, timeout=20)
                data = {
                   'type': 'auth',
                   'username': username,
                   'password': password
                }
                r2 = session.put(Constants.AUTH_URL,json=data,headers=headers,proxies=proxy,timeout=20)
                #input(r2.text)
                #print(session.get('https://api64.ipify.org?format=json',proxies=proxy).text)
            except Exception as e:
                #input(e)
                account.code = 6
                return account
            try:
                data = r2.json()
            except:
                account.code = 6
                return account
            if "access_token" in r2.text:
                pattern = compile(
                    'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
                data = pattern.findall(
                    data['response']['parameters']['uri'])[0]
                token = data[0]
                token_id = data[1]

            elif 'invalid_session_id' in r2.text:
                account.code = 6
                return account
            elif "auth_failure" in r2.text:
                account.code = 3
                return account
            elif 'rate_limited' in r2.text:
                account.code = 1
                return account
            elif 'multifactor' in r2.text:
                account.code = 3
                return account
            elif 'cloudflare' in r2.text:
                account.code = 5
                return account
            else:
                account.code = 3
                return account


            headers = {
                'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)',
                'Authorization': f'Bearer {token}',
            }
            try:
                with session.post(Constants.ENTITLEMENT_URL, headers=headers, json={}, proxies=proxy) as r:
                    entitlement = r.json()['entitlements_token']
                r = session.post(Constants.USERINFO_URL,
                                 headers=headers, json={}, proxies=proxy)
            except:
                account.code = 6
                return account
            # print(r.text)
            # input()
            #input(r.text)
            data = r.json()
            # print(data)
            # input()
            gamename = data['acct']['game_name']
            tagline = data['acct']['tag_line']
            registerdate = data['acct']['created_at']
            registerdatepatched = pandas.to_datetime(int(registerdate), unit='ms')
            puuid = data['sub']
            try:
                #input(data)
                data2 = data['ban']
                # input(data2)
                data3 = data2['restrictions']
                #input(data3)
                typebanned = data3[0]['type']
                #input(typebanned)
                # input(typebanned)
                if typebanned == "PERMANENT_BAN" or typebanned == 'PERMA_BAN':
                    # input(True)
                    account.code = 4
                    return account
                elif 'PERMANENT_BAN' in str(data3) or 'PERMA_BAN' in str(data3):
                    # input(True)
                    account.code = 4
                    return account
                elif typebanned == 'TIME_BAN' or typebanned == 'LEGACY_BAN':
                    expire = data3[0]['dat']['expirationMillis']
                    expirepatched = pandas.to_datetime(int(expire), unit='ms')
                    #input(expire)
                    banuntil = expirepatched
                else:
                    banuntil = None
                    pass
            except Exception as e:
                # print(e)
                #input(e)
                banuntil = None
                pass
            try:
                # headers={
                #    'Authorization': f'Bearer {token}',
                #    'Content-Type': 'application/json',
                #    'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)',
                # }

                # r=session.get('https://email-verification.riotgames.com/api/v1/account/status',headers=headers,json={},proxies=sys.getproxy(self.proxlist)).text

                # mailverif=r.split(',"emailVerified":')[1].split('}')[0]

                mailverif = bool(data['email_verified'])

            except Exception as e:
                # input(e)
                mailverif = True
            mailverif = not mailverif #true to false || false to true
            account.token = token
            account.entt = entitlement
            account.puuid = puuid
            account.unverifiedmail = mailverif
            account.banuntil = banuntil
            account.gamename = gamename
            account.tagline = tagline
            account.registerdate = registerdatepatched
            return account
        except Exception as e:
            account.errmsg = str(traceback.format_exc())
            account.code = 2
            return account