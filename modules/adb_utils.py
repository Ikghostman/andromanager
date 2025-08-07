#! /bin/python3 

''' Adb daemom management '''

from modules.banners import main_banner as banner
from subprocess import getoutput as get_status
from colorama import Fore
from modules.menus import adb_utils_menu
from modules.utils import clear, Quit, back, options_matcher
from click import echo, style, prompt
import os


def is_adb_up():

    status=get_status(f"nmap localhost -p 5037 --system-dns|grep -i open|cut -d ' ' -f 2")
    if str(status)=='open':
        echo(style("[✔️ ] ADB daemon running ...",fg='green'))
        return True
    else:
        echo(style("[❌] ADB server is down !",fg='bright_yellow'))
        return False
def start_adb():
    try:
        status=get_status(f"adb start-server")
        if len(status)==0:
            echo(style("[✔️] ADB server already up ...",fg='bright_green'))
        elif 'start' in status:
                echo(style("[✔️] ADB daemom started successfully ...",fg='bright_white'))
                return True
        else:
            echo(style("[❗] Sorry, Unknown ERROR caught !, returning ...",blink=True,fg='red'))
            return False
    except Exception as e:
        print(f"{Fore.RED}[❗] ERROR: {e}{Fore.RESET}")
        return False
    except KeyboardInterrupt:
        Quit()
def stop_adb():
    try:
        status=get_status(
                f"adb kill-server"
                )
        if status=='':
            echo(style("[✔️] ADB daemon stoped successfully ...",fg='bright_yellow'))
        else:
            if 'cannot connect' in status:
                echo(style(" [!] ADB daemon is not running...Already stoped ",fg='red'))
                return True
    except Exception as e:
        print(f"{Fore.RED}ERROR: {e}{Fore.RESET}")
    except KeyboardInterrupt:
        Quit()

def restart_adb():
    try:
        status=get_status(f"adb kill-server&&adb start-server")
        if len(status)==0:
            echo(style("[!] Unkown ERROR  ...",fg='red'))
        elif 'start' in status:
                echo(style("[✔️] ADB daemom restarted successfully ...",fg='bright_magenta'))
                return True
        else:
            echo(style("[❗] Sorry, Unknown ERROR caught !, returning ...",blink=True,fg='red'))
            return False
    except Exception as e:
        print(f"{Fore.RED}[❗] ERROR: {e}{Fore.RESET}")
        return False
    except KeyboardInterrupt:
        Quit()
def adb_options():
    def clean():
        clear()
    try:
        adb_utils_menu()
        option=prompt("[Choose an option [int]>]: ")
        options_list={
                "1":  is_adb_up,
                "2":  start_adb,
                "3":  stop_adb,
                "4":  restart_adb,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !='0':
            adb_options()
        
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET}{Fore.YELLOW}{e}")
    except KeyboardInterrupt:
        Quit()
