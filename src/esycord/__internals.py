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
colorama.init(autoreset=True)
colorama.just_fix_windows_console()




class _btInternal:
    def error(msg):
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Bot :", end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'[ERROR]:  ', end=' ' )
        print(msg)

    def warn(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.BLUE+"esycord.Bot :", end=' ')
        print( colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'[WARNING]: ', end=' ' )
        print(msg)

    def success(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Bot :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.GREEN + f'[SUCCESS]:  ', end=' ' )
        print(msg)
    def status(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.BLUE + "esycord.Bot :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.CYAN + f'[STATUS]: ', end=' ' )
        print(msg)

class _dataInternal:
    def error(msg):
        print(colorama.Style.BRIGHT + colorama.Fore.WHITE + "esycord.Data :", end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'[ERROR]:  ', end=' ' )
        print(msg)

    def warn(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.WHITE+"esycord.Data :", end=' ')
        print( colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'[WARNING]: ', end=' ' )
        print(msg)

    def success(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.WHITE + "esycord.Data :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.GREEN + f'[SUCCESS]:  ', end=' ' )
        print(msg)
    def status(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.WHITE + "esycord.Data :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.CYAN + f'[STATUS]: ', end=' ' )
        print(msg)

class _wbInternal:
    def error(msg):
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + "esycord.Webhook :", end=' ')
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f'[ERROR]:  ', end=' ' )
        print(msg)

    def warn(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.YELLOW+"esycord.Webhook :", end=' ')
        print( colorama.Style.BRIGHT + colorama.Fore.YELLOW + f'[WARNING]: ', end=' ' )
        print(msg)

    def success(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.YELLOW + "esycord.Webhook :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.GREEN + f'[SUCCESS]:  ', end=' ' )
        print(msg)
    def status(msg):
        print( colorama.Style.BRIGHT + colorama.Fore.YELLOW + "esycord.Webhook :", end=' ' )
        print( colorama.Style.BRIGHT + colorama.Fore.CYAN + f'[STATUS]: ', end=' ' )
        print(msg)
