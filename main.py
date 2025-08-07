#! /bin/python3
from modules.banners import main_banner as banner
from colorama import Fore
from modules import andromanager
from modules.utils import Quit
from setup_check import check_required_tools
import sys

def run_tool():
    try:
        banner()
        if check_required_tools(sleeper=False,output_style=2):
            return andromanager.main_options()
        else:
            print(f"\n")
            print(f"{Fore.RED}[*] Please run{Fore.RESET} {Fore.GREEN}python3 setup_check.py{Fore.RESET} {Fore.RED}for tool setup guide{Fore.RESET}")
            sys.exit()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET}{Fore.YELLOW}{e}")
        sys.exit()
    except KeyboardInterrupt:
        Quit()
if __name__=="__main__":
    run_tool()
