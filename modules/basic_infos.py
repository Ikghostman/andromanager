#!/bin/python3
''' 
    This function tries to gather some basic informations about android devices via ADB
    '''
from modules.menus import device_infos_menu
from modules.utils import back, clear, Quit, options_matcher
from colorama import Fore
from modules.build_table import builder as build
from modules.adb_cmds import basic_infos_cmds
from subprocess import getoutput as get_data
from modules.banners import main_banner as banner
from click import echo, style, prompt
import sys
import os

def device_infos(): # Device information Ghather function 
    
    cmd=basic_infos_cmds
    
    model=get_data(f"{cmd[1]}.model")
    manufacturer=get_data(f"{cmd[1]}.manufacturer")
    chipset=get_data(f"{cmd[1]}.board")
    android=get_data(f"{cmd[2]}.version.release")
    security_patch=get_data(f"{cmd[2]}.version.security_patch")
    device=get_data(f"{cmd[1]}.vendor.device")
    sim=get_data(f"{cmd[5]}")
    encryptage=get_data(f"{cmd[3]}.state")
    build_date=get_data(f"{cmd[2]}.date")
    sdk_version=get_data(f"{cmd[2]}.version.sdk")
    wifi_interface=get_data(f"{cmd[4]}")
    battery=get_data(f"{cmd[6]}")
    device_name=get_data(f"{cmd[7]}.name")
    
    columns={
            'Device Properties': 'red',
            'Informations': 'bright_green',
            }
    rows={
            'Model': model,
            'Manufactuerer': manufacturer,
            'Chipset': chipset,
            'Android': android,
            'Security Patch': security_patch,
            'Device': device,
            'Device Name': device_name,
            'Sim': sim,
            'Encryption Type': encryptage,
            'Build Date': build_date,
            'SDK Version': sdk_version,
            'WI-FI Interface': wifi_interface,
            }
    battery_column= {
            "Device Battery": 'bright_white',
            "Informations": 'bright_yellow',
            }
    battery_rows= {
            "Battery": battery,
            }
    try:
        check=get_data(f"adb devices -l|grep -i 'device:'")
        if "device" not in check:
            banner()
            echo(style("No Device detected on ADB  📵",blink=True,fg='red'))
            return False
        else:
            banner()
            build(columns,rows,style='yellow',end_s=False)
            build(battery_column,battery_rows,style='yellow',end_s=False)
    except Exception as e:
        banner()
        print(f"{Fore.RED}Error Occured{Fore.RESET}: {Fore.YELLOW}{e}{Fore.RESET}")
        return False
        
def device_infos_options():
    def clean():
        clear()
    try:
        device_infos_menu()
        option=prompt("[Choose an option [int]>] ")
        options_list={
                "1":  device_infos,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !='0':
            device_infos_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET}{Fore.YELLOW}{e}")
