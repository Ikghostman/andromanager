#! /bin/python3

from modules.banners import main_banner as banner
from modules.menus import frp_menu
from click import echo, style, prompt
from modules.adb_utils import is_adb_up, start_adb
from modules.basic_infos import device_infos
from modules.utils import clear, back, Quit, options_matcher, is_device_found, andro_frp_hint, sam_frp_hint
from colorama import Fore
from modules.frputils import AdbUtils, ATUtils, SamsungFRPBypass
import sys

def AdbEnabledFrpBypass():
    try:
        andro_frp_hint()
        echo(style("Press ENTER to continune once you're ready to proceed",fg='bright_yellow',blink=True))
        statust=input()
        banner()
        
        if is_device_found():
            opt=input(f"{Fore.RED}Device Found: {Fore.RESET} {Fore.YELLOW}Are you sure to continue (y/n) ?: {Fore.RESET}")
            if opt.upper()=='Y' or opt.lower()=='y':
                AdbUtils.frp_bypass_method_1() #or AdbUtils.frp_bypass_method_2()
                echo(style("[*] Android device FRP Bypass Operation finished successfully !.",fg='bright_green'))
                return True
            else:
                return False
        else:
            echo(style("[i] Verify cable connection and make sure ADB is Enabled",fg='red'))
            return False
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}{Fore.RESET}")
        return False
    return True

def SamsungFRP():
    try:
        sam_frp_hint()
        echo(style("Press ENTER to continue once you're ready to proceed",fg='bright_yellow',blink=True))
        status=input()
        banner()
        start_adb()
        if SamsungFRPBypass.SamsungToModem():
            print('-' * 60)
            ATUtils.dump_devconinfo()
            print('-' * 65)
            echo(style("Go to emergency and dial *#0*# or *#*#88#*#* then press Press ENTER to continue",fg='bright_magenta'))
            check=input()
            sys.stdout.flush()
            ATUtils.adb_exploit()
            print('\n')
            print('-' * 65)
            if ATUtils.check_exploit_status():
                print(f"{Fore.LIGHTGREEN_EX}[*] Discovered device over ADB{Fore.RESET}")
                time.sleep(0.7)
                banner()
                AdbUtils.frp_bypass_method_1() #or AdbUtils.frp_bypass_method_2()
            else:
                print(f"{Fore.LIGHTRED_EX}[x] Exploits failed to enable adb !{Fore.RESET}")
                return False
        else:
            return False
    except Exception as e:
            print(f"{Fore.RED}ERROR: {Fore.RESET}{Fore.YELLOW}{e}")
            return False
    return True

def FRP_options():
    def clean():
        clear()
    try:
        frp_menu()
        option=prompt("[Choose an option [int]>] ")
        options_list={
                "1":  AdbEnabledFrpBypass,
                "2":  SamsungFRP,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !='0':
            FRP_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
