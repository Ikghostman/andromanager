#! /bin/python3

from modules.menus import main_menu
from modules.banners import main_banner as banner
from modules.adb_utils import adb_options
from modules.utils import Quit, clear, options_matcher
from modules.basic_infos import device_infos_options
from modules.devices_utils import devices_utils_options
from modules.device_access import device_access_options
from modules.power_manager import power_manager_options
from modules.frpbypass import FRP_options
import sys
import os
from click import echo, style
from colorama import Fore
import time

def main_options():
    
    def clean():
        clear()
        return main_options()
    
    try:
        banner()
        main_menu()
        echo(style("[Choose an option>]--⤵️",fg='bright_cyan'))
        option=input(f"[int>]: ")
        options_list= {
                "1":  adb_options,
                "2":  devices_utils_options,
                "3":  device_infos_options,
                "4":  device_access_options,
                "5":  FRP_options,
                "6":  power_manager_options,
                "99": clean,
                "0":  Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            main_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET}{Fore.YELLOW}{e}")
    except KeyboardInterrupt:
        Quit()

if __name__== "__main__":
    main_options()
