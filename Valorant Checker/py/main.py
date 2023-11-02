import asyncio
import ctypes
import json
import os
import random
import tkinter
from tkinter import filedialog
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import colorama

import requests
from colorama import Fore, Style

import checker
from codeparts import checkers, systems, validsort
from codeparts.systems import system

check = checkers.checkers()
sys = systems.system()
valid = validsort.validsort()


class program():
    def __init__(self) -> None:
        self.count = 0
        self.checked = 0
        self.version = '3.15.2'
        self.riotlimitinarow = 0
        path = os.getcwd()
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))
        try:
            self.lastver = requests.get(
                'https://api.github.com/repos/lil-jaba/valchecker/releases').json()[0]['tag_name']
        except:
            self.lastver = self.version

    def start(self):
        try:
            print('internet check')
            requests.get('https://github.com')
        except requests.exceptions.ConnectionError:
            print('no internet connection')
            os._exit(0)
        os.system('cls')
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color not in ['BLACK']]
        colored_name = [random.choice(colors) + char for char in f'ValChecker by liljaba1337']
        print(sys.get_spaces_to_center('ValChecker by liljaba1337')+(''.join(colored_name))+colorama.Fore.RESET)
        print(sys.center(f'v{self.version}'))
        print(sys.center(f'{Fore.YELLOW}Thank you for using ValChecker!'))
        print(sys.center(f'{Fore.YELLOW}v3.15.2 is the last version of ValChecker released by liljaba in Python'))
        print(sys.center(f'{Fore.YELLOW}Im currently working on ValChecker4, so I\'ll notify you when it\'s out'))
        print(sys.center(f'{Fore.YELLOW}This version of ValChecker WILL NOT be supported by me anymore'))
        print()
        r = requests.get('https://api.github.com/repos/lil-jaba/valchecker4')
        try:
            r.json()['message']
        except:
            print(sys.center(f'{Fore.GREEN}Good news! ValChecker4 is out!'))
            print(sys.center(f'{Fore.GREEN}Please follow this link to download it:'))
            print(sys.center(f'{Fore.GREEN}https://github.com/LIL-JABA/valchecker4{Fore.WHITE}'))
        if 'devtest' in self.version:
            print(sys.center(f'{Fore.YELLOW}Hi from liljaba'))
        elif 'beta' in self.version:
            print(sys.center(f'{Fore.YELLOW}You have downloaded the BETA version. It can work unstable and contain some bugs.'))
            print(sys.center(f'Follow https://github.com/LIL-JABA/valchecker/releases/latest to download the latest stable release{Fore.RESET}'))
        elif self.lastver != self.version:
            print(sys.center(
                f'\nnext version {self.lastver} is available!'))
            if inquirer.confirm(
                message="{}Would you like to download it now?".format(system.get_spaces_to_center('Would you like to download it now? (Y/n)')), default=True,qmark=''
            ).execute():
                os.system(f'{self.parentpath}/updater.bat')
                os._exit(0)
        menu_choices = [
            Separator(),
            'Start Checker',
            'Single-Line Checker',
            'Edit Settings',
            'Sort Valid',
            'Test Proxy',
            f'Some info for devs',
            Separator(),
            'Exit'
        ]
        print(sys.center('\nhttps://github.com/LIL-JABA/valchecker\n'))
        res = inquirer.select(
            message="Please select an option:",
            choices=menu_choices,
            default=menu_choices[0],
            pointer='>',
            qmark=''
        ).execute()
        if res == menu_choices[1]:
            self.main()
            input('finished checking. press ENTER to exit')
            pr.start()
        elif res == menu_choices[2]:
            slchecker = checker.singlelinechecker()
            slchecker.main()
            pr.start()
        elif res == menu_choices[3]:
            sys.edit_settings()
            pr.start()
        elif res == menu_choices[4]:
            valid.customsort()
            input('done. press ENTER to exit')
            pr.start()
        elif res == menu_choices[5]:
            sys.checkproxy()
            pr.start()
        elif res == menu_choices[6]:
            os.system('cls')
            print(f'''
    valchecker v{self.version} by liljaba1337

    If you have any questions about valchecker's source code, feel free to ask me in discord
    https://discord.gg/RzUjzpVXpE (liljaba1338#7206)

    You can also open pull requests if you have some updates, I will check them all

    Happy coding :)

  [~] - press ENTER to return
            ''')
            input()
            pr.start()
        elif res == menu_choices[8]:
            os._exit(0)

    def get_accounts(self):
        root = tkinter.Tk()
        file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                                      filetype=(("txt", "*.txt"), ("All files", "*.txt")))
        root.destroy()
        os.system('cls')
        if file == None:
            os._exit(0)
        filename = str(file).split("name='")[1].split("'>")[0]
        with open(str(filename), 'r', encoding='UTF-8', errors='replace') as file:
            lines = file.readlines()
            ret = []
            if len(lines) > 100000:
                if inquirer.confirm(
                    message=f"You have more than 100k accounts ({len(lines)}). Do you want to skip the sorting part? (it removes doubles and bad logpasses but can be long)",
                    default=True,
                    qmark='!',
                    amark='!'
                ).execute():
                    self.count = len(lines)
                    return lines
            for logpass in lines:
                logpass = logpass.strip()
                # remove doubles
                if logpass not in ret and ':' in logpass:
                    self.count += 1
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f'ValChecker {self.version} by liljaba1337 | Loading Accounts ({self.count})')
                    ret.append(logpass)
            return ret

    def main(self):
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Settings')
        print('loading settings')
        settings = sys.load_settings()

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Proxies')
        print('loading proxies')
        proxylist = sys.load_proxy()

        if proxylist == None:
            path = os.getcwd()
            file_path = f"{os.path.abspath(os.path.join(path, os.pardir))}\\proxy.txt"

            print(Fore.YELLOW, end='')
            response = input('No Proxies Found, Do you want to scrape proxies? (y/n): ')
            print(Style.RESET_ALL, end='')

            if response.lower() == 'y':
                f = open('system\\settings.json', 'r+')
                data = json.load(f)
                proxyscraper = data['proxyscraper']
                f.close()

                # Scrape proxies
                url = proxyscraper
                proxies = requests.get(url).text.split('\r\n')

                # Save proxies to file
                with open(file_path, 'w') as f:
                    f.write("\n".join(proxies))

                # Print number of proxies saved
                num_proxies = len(proxies)
                print(f'{num_proxies} Proxies saved to "proxy.txt" file.')
                proxylist = sys.load_proxy()
            else:
                print('Running Proxy Less...')

        if inquirer.confirm(
            message="Do you want to continue checking a .vlchkr file instead of loading a new .txt?", default=True
        ).execute():
            root = tkinter.Tk()
            file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                                          filetype=(("vlchkr", "*.vlchkr"), ("All files", "*.vlchkr")))
            root.destroy()
            if file == None:
                filename = 'None'
            else:
                filename = str(file).split("name='")[1].split("'>")[0]
                valkekersource = systems.vlchkrsource(filename)
                accounts=None
        else: 
            valkekersource = None
            ctypes.windll.kernel32.SetConsoleTitleW(
                f'ValChecker {self.version} by liljaba1337 | Loading Accounts')
            print('loading accounts')
            accounts = self.get_accounts()

        print('loading assets')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Assets')
        sys.load_assets()

        print('loading checker')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Checker')
        scheck = checker.simplechecker(settings, proxylist, self.version)
        asyncio.run(scheck.main(accounts, self.count, valkekersource))
        return


pr = program()
if __name__ == '__main__':
    print('starting')
    pr.start()
