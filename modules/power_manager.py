#! /bin/python3

import os
from modules.menus import power_manager_menu
from modules.utils import is_device_found, back, Quit, clear, options_matcher
from colorama import Fore
from click import echo, style, prompt

class PowerManager:

    '''Android device reboot class. Used to reboot device into a speified mode (fastboot, recovery, bootloader).'''

    def reboot():
        try:
            if is_device_found():
                echo(style("[WARRNING] Restatring Will disconnect devices",fg='red',blink=True))
                choice=input(f"{Fore.RED}[Do you want to continue (y/n)>] {Fore.RESET}")
                if choice.upper()=='Y' or choice.lower()=='y':
                    echo(style("[i] Restartind device ...",fg='green'))
                    if os.system(
                            f"adb reboot>/dev/null"
                            )==0:
                        echo(style("[*] Restart operation finished successfully.",fg='bright_yellow'))
                        return True
                    else:
                        echo(style("[i] An occured occured while restarting device !",fg='red'))
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        return True
    
    def reboot_recovery():
        try:
            if is_device_found():
                echo(style("[WARRNING] Deivce will disconnect and reboot into recovery mode",fg='red',blink=True))
                choice=input(f"{Fore.RED}[Do you want to continue (y/n)>] {Fore.RESET}")
                if choice.upper()=='Y' or choice.lower()=='y':
                    echo(style("[i] Triggerd device recovery mode reboot ...",fg='green'))
                    if os.system(
                            f"adb reboot>/dev/null"
                            )==0:
                        echo(style("[*] Recovery reboot operation finished successfully.",fg='bright_yellow'))
                        return True
                    else:
                        echo(style("[i] An occured occured while rebooting device into recovery mode !",fg='red'))
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        return True
    
    def reboot_fastboot():
        try:
            if is_device_found():
                echo(style("[WARRNING] Device Will disconnect and reboot into fastboot mode",fg='red',blink=True))
                choice=input(f"{Fore.RED}[Do you want to continue (y/n)>] {Fore.RESET}")
                if choice.upper()=='Y' or choice.lower()=='y':
                    echo(style("[i] Triggered device fastboot mode reboot ...",fg='green'))
                    if os.system(
                            f"adb reboot>/dev/null"
                            )==0:
                        echo(style("[*] Fastboot reboot operation finished successfully.",fg='bright_yellow'))
                        return True
                    else:
                        echo(style("[i] An occured occured while rebooting device into fastboot mode !",fg='red'))
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        return True
    
    def reboot_bootloader():
        try:
            if is_device_found():
                echo(style("[WARRNING] Device Will disconnect and reboot to booloader",fg='red',blink=True))
                choice=input(f"{Fore.RED}[Do you want to continue (y/n)>] {Fore.RESET}")
                if choice.upper()=='Y' or choice.lower()=='y':
                    echo(style("[i] Triggered device bootloader reboot ...",fg='green'))
                    if os.system(
                            f"adb reboot>/dev/null"
                            )==0:
                        echo(style("[*] bootloader reboot operation finished successfully.",fg='bright_yellow'))
                        return True
                    else:
                        echo(style("[i] An occured occured while rebooting device into bootloader !",fg='red'))
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        return True

def power_manager_options():
    def clean():
        clear()
    try:
        power_manager_menu()
        option=prompt("[Choose an option [int]>] ")
        options_list={
                "1": PowerManager.reboot,
                "2": PowerManager.reboot_recovery,
                "3": PowerManager.reboot_fastboot,
                "4": PowerManager.reboot_bootloader,
                "99": clean,
                "0": back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !='0':
            power_manager_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
