"""
MIT License

Copyright (c) 2024 Aayush Srivastava

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import colorama
import time
import requests
from . import __version__
from os import system

colorama.init(autoreset=True)
colorama.just_fix_windows_console()



class _btInternal:
    def error(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'ERROR    :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Bot :", end=' ')
        print(colorama.Style.BRIGHT+msg)

    def warn(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'WARNING  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Bot :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def success(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + f'SUCCESS  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Bot :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def status(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + f'INFO     :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Bot :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def fatal(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'FATAL    :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.RED + "esycord.Bot :", end=' ')
        print(colorama.Style.BRIGHT+msg)

class _dataInternal:
    def error(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'ERROR    :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Data :", end=' ')
        print(colorama.Style.BRIGHT+msg)

    def warn(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'WARNING  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Data :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def success(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + f'SUCCESS  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Data :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def status(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + f'INFO     :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Data :", end=' ')
        print(colorama.Style.BRIGHT+msg)


class _wbInternal:
    def error(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'ERROR    :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Webhook :", end=' ')
        print(colorama.Style.BRIGHT+msg)

    def warn(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'WARNING  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Webhook :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def success(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + f'SUCCESS  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Webhook :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def status(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + f'INFO     :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Webhook :", end=' ')
        print(colorama.Style.BRIGHT+msg)

class _vcInternal:
    def error(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'ERROR    :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Voice :", end=' ')
        print(colorama.Style.BRIGHT+msg)

    def warn(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'WARNING  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Voice :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def success(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + f'SUCCESS  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Voice :", end=' ')
        print(colorama.Style.BRIGHT+msg)
    def status(msg):
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + f'INFO     :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Voice :", end=' ')
        print(colorama.Style.BRIGHT+msg)

def update_checker():
    try:
        josn=requests.get('https://pypi.org/pypi/esycord/json').json()
        if josn["releases"].popitem()[0]!=__version__:
            print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + f'INFO     :', end='     ' )
            print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord :", end=' ')
            print(colorama.Style.BRIGHT+"A new distribution of esycord is available!")
            print(f'Current Version : {__version__}. Latest Release : {josn["releases"].popitem()[0]}', end=' ')
            
            while True:
                x=input(colorama.Style.BRIGHT+"Update? (y/n): ").lower().strip()
                if x in ['y', 'n']:break
                else:print("Please select a valid choice!")
            
            if x=='y':
                system("python3 -m pip install -U esycord")
                print("Update Successfully installed. Rerun your script now.")
            elif x=='n':pass
    except:
        print(colorama.Style.DIM + colorama.Fore.LIGHTBLACK_EX+ time.strftime("%Y-%m-%d %H:%m:%S"), end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'WARNING  :', end='     ' )
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord :    ", end=' ')
        print(colorama.Style.BRIGHT+"Version Check failed. Continuing...")
