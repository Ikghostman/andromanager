#! /bin/python3

from modules import andromanager
from modules.build_table import builder as build
from modules import adb_utils
from subprocess import getoutput as get_data
from colorama import Fore
import os
import sys
import socket
import time
from modules.banners import main_banner as banner
from click import echo, style

def clear():
    banner()

back=lambda:andromanager.main_options()

def Quit():
    echo(style("[*] Thanks for using the Tool !, Exiting...",blink=True,fg='red'))
    sys.exit()

def options_matcher(option : str ,options_list : dict ):
    
    '''Use carefully..If there is a return function after the choosed option,
    a little effort is required to avoid the loop of this function. 
    Check its usage in device_access.py for better usage.. 
    '''
    if option=="":
        echo(style("[*] No option selected !",fg='red'))
        time.sleep(0.5)
        banner()
        return
    else:
        match option:
            case opt:
                if option not in options_list:
                    echo(style("[*] Invalid option !",fg='red'))
                    time.sleep(0.5)
                    banner()
                    return
                else:
                    for key, value in options_list.items():
                        if key==opt:
                            banner()
                            value()

def open_file(filename):
    opener='xdg-open'
    return os.system(f"{opener} {filename}")

def is_device_found():
    try:
        if adb_utils.is_adb_up():
            devices=get_data(f"adb devices -l|wc -l")
            columns={
                    "Connected Devices": "gold3",
                    "List of attached devices": "bright_white",
                    }
            rows={
                    "Devices": devices,
                    }
            if int(devices)==2:
                rows['Devices']="No device found over ADB"
                build(columns,rows,style="bright_cyan",end_s=False)
                echo(style("[i] No available device over ADB",blink=True,fg='red'))
                return False
            else:
                devs=get_data(f"adb devices -l|sed s/'List of devices attached'//g|sed s/'  '/''/g")
                rows["Devices"]=devs
                build(columns,rows,style='bright_cyan',end_s=True)
                return True
        else:
            adb_utils.start_adb()
            return is_device_found()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
        return False
    return True

def andro_frp_hint():
    column={
            "HINT FOR ENABLING ADB IF DEVICE IS COMPATIBLE": "bright_cyan",
            }
    row={
            "A Little bit hack is required for enabling ADB.\nSo, if you find a way to open chrome on the FRP\nLocked device then, go and search for 'frp bypass vmrom'.\nOnce on the site, check the 'enable adb option.\nIt would link to the dialer. Dial *#85# and, If\nthe code work,connect the USB Cable then, check the ABD\nprompt on target device screen and all is done.": "",
            }
    build(column,row,style='bright_yellow',end_s=False)

def sam_frp_hint():
    column={
            "SPECIAL NOTE ABOUT USING THIS FEATURE OF ANDROID MANAGE TOOL": "bright_cyan",
            }
    row={
            "The SAMSUNG FRP Bypass feature may detect your device but ends up with failure\nto enable ADB, try editing the code in 'frputils' if you have some custom AT\nCommands or other alternative required info for Samsung ADB Enable in the code.\nAny Contribution for powering the tool is welcome.Be awarned that not all devices\nthat are supported.The tool is made from scratch by using other codes found on \ngithub and other sources.Github link in Tool's banner for reporting issues.": "",
            }
    build(column,row,style='bright_yellow',end_s=False)
