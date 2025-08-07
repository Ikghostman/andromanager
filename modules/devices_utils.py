#! /bin/python3 

''' Devices  Utilities'''

import sys
from modules.utils import back, Quit, clear
from modules.menus import devices_utils_menu, network_scan_menu
from subprocess import getoutput as get_data
from modules.banners import main_banner as banner
from modules.build_table import builder as build
from modules.utils import back, clear, Quit, options_matcher, is_device_found
from colorama import Fore
from click import echo, style, prompt
from modules import adb_utils
from rich.table import Table
from rich.console import Console
import nmap
import os
import sys
import socket

def connect():
    echo(style("Require Android phones IP Address [Example : 192.168.1.23]",fg='bright_yellow'))
    ip = input("[Enter IP Address>]: ")
    if ip=="":
        echo(style("No IP Address provided !",blink=True,fg='red'))
        return False
    if ip.count(".") != 3:
        echo(style("[*] Invalied IP Address Provided !",fg='red'))
        return False
    else:
        echo(style("Enter target device Debug Bridge Port or press enter for default",fg='bright_yellow'))
        port=prompt("[Enter port [int]>] the default is: ",default='5555')

        # Restart ADB on new connection.
        try:
            if adb_utils.is_adb_up():
                adb_utils.restart_adb()
                if os.system(f"adb connect {ip}:{port} > /dev/null")==True:
                    print(f"{Fore.GREEN}[i] Operation status:{Fore.RESET} {Fore.LIGHTWHITE_EX}{ip}{Fore.RESET} {Fore.GREEN}Connected successfully{Fore.RESET}")
                    return True
                else:
                    print(f"{Fore.GREEN}[i] Operation status:{Fore.RESET} {Fore.LIGHTYELLOW_EX}{ip}{Fore.RESET} {Fore.RED}Connection Failed.{Fore.RESET}")
                    return False
            else:
                adb_utils.start_adb()
                if os.system(f"adb connect {ip}:{port} > /dev/null")==True:
                    print(f"{Fore.GREEN}[i] Operation status:{Fore.RESET} {Fore.LIGHTWHITE_EX}{ip}{Fore.RESET} {Fore.GREEN}Connected successfully{Fore.RESET}")
                    return True
                else:
                    print(f"{Fore.GREEN}[i] Operation status:{Fore.RESET} {Fore.LIGHTYELLOW_EX}{ip}{Fore.RESET} {Fore.RED}Connection Failed.{Fore.RESET}")
                    return False
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}{Fore.RESET}")
            return False
        except KeyboardInterrupt:
            return False
    return True

def list_devices():
    devices=get_data(f"adb devices -l")
    if adb_utils.is_adb_up():
        devices=get_data(f"adb devices -l|wc -l")
        column={
                "Connected Devices": "gold3",
                "List of Attached Devices": "bright_white",
                }
        rows= {}
        if int(devices)==2:
            rows["Devices"]="No Device found on ADB"
            build(column,rows,style="bright_cyan",end_s=False)
            return False
        else:
            devs=get_data(f"adb devices -l|sed s/'List of devices attached'//g|sed s/'  '/''/g").strip()
            rows['Devices']=devs
            build(column,rows,style='bright_cyan',end_s=False)
            return True
    else:
        adb_utils.start_adb()
        return list_devices()
    return True

def disconnect():
    if is_device_found():
        if os.system("adb disconnect > /dev/null")==0:
            echo(style("All connected devices are disconnected !.",fg='bright_green'))
            return True
        else:
            echo(style("[x] Fata Error: unknown !.",fg='bright_red'))
            return False
    else:
        return False

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return False

def select_device():
    try:
        if list_devices():
            if 'usb' in get_data(f"adb devices -l|sed /'List of devices attached'//g|sed s/'  '/''/g").strip():
                echo(style("Require target device serial No. Manyally Enter please",fg='bright_yellow'))
                device=input("[Enter target device Serial No>]: ")
                if device=="":
                    banner()
                    echo(style("No serial no specified !",fg='red'))
                    return False
                try:
                    serial_nos=get_data(f"adb devices -l|sed s/'List of devices attached'//g|sed s/'  '/''/g|cut -d ' ' -f 1").strip().split('\n')
                    for serial in serial_nos:
                        if str(serial)==str(device):
                            print(f"{Fore.YELLOW}[*] Restarting adb in one device mode:{Fore.RESET} {Fore.RED}{device} ...{Fore.RESET}")
                            if os.system(
                                    f"adb start-server --one-device {device}>/dev/null"
                                    )==0:
                                print(f"{Fore.GREEN}[i] Selected device:{Fore.RESET} {Fore.RED}{device}{Fore.RESET} {Fore.GREEN}connected successfully{Fore.RESET}")
                                return True
                            else:
                                echo(style("[i] Device connection failed !. An ERROR Occured",blink=True,fg='bright_red'))
                                return False
                        else:
                            echo(style("[*] No device match the specified serial no !",fg='red'))
                            return False
                except Exception as e:
                    print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                    return False
            else:
                echo(style("No device detected over USB !",fg='red'))
                return False
        else:
            echo(style("[i] No available device over ADB",blink=True,fg='red'))
            return False
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET}: {Fore.YELLOW}{e}")
        return False
    return True

def enable_remote_connect():
    try:
        if is_device_found():
            if os.system(
                    f"adb tcpip 5555 > /dev/null"
                    )==0:
                echo(style("[*]Device TCP connection switched on",fg='bright_green'))
                return True
            else:
                echo(style("[!] Failed to switch on device TCP connetion.",fg='red'))
                return False
        else:
            return False
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
        return False
    return True

def scan_network():
    try:
        echo(style("[*] Scanning network for connected devices...",fg='bright_green'))
        if get_ip_address():
            ip=get_ip_address()
            ip += '/24'
            scanner = nmap.PortScanner()
            scanner.scan(hosts=ip, arguments="-sn")
            devices={}
            vendor_found={}
            vendor_not_found={}
            vendor_found_hosts=[]
            vendor_not_found_hosts=[]
            all_hosts=[]
            columns={
                    "Hosts IP Adress": "bright_white",
                    "Hosts Vendors Informations": "bright_yellow",
                    }
            for host in scanner.all_hosts():
                if scanner[host]["status"]["state"] == "up":
                    if len(scanner[host]['vendor']) !=0:
                        devices[host]=str(scanner[host]['vendor']).strip("{}")
                        vendor_found[host]=str(scanner[host]['vendor']).strip("{}")
                    else:
                        devices[host]="Missing Vendor Information"
                        vendor_not_found[host]="Missing Vendor Information"
            for key, value in devices.items():
                all_hosts.append(key)
            for key, value in vendor_found.items():
                vendor_found_hosts.append(key)
            for key, value in vendor_not_found.items():
                vendor_not_found_hosts.append(key)
            s_columns={
                    "Hosts with Vendor Infos": "bright_white",
                    "Hosts  without Vendor Info": "yellow",
                    "All Discovered Hosts": "bright_red",
                    }
            s_rows={
                    f"{str(len(vendor_found_hosts))}": f"{str(len(vendor_not_found_hosts))}",
                    }
            def scan_result():
                build(s_columns,s_rows,style='bright_cyan',end_s=False,sr=f"{str(len(all_hosts))}")
                private_ip_cmd="ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1 -d'/'"
                public_ip=get_data(f"shodan myip")
                private_ip=get_data(f"{private_ip_cmd}")
                print(f"{Fore.LIGHTGREEN_EX}[*] Your Private IP:{Fore.RESET} {Fore.LIGHTWHITE_EX}{private_ip}{Fore.RESET}")
                print(f"{Fore.LIGHTGREEN_EX}[*] Your Public IP:{Fore.RESET} {Fore.LIGHTWHITE_EX}{public_ip}{Fore.RESET}")
            def print_vendor_found():
                build(columns,vendor_found,style='bright_cyan',end_s=False)
                return scan_result_options()
            def print_vendor_not_found():
                build(columns,vendor_not_found,style='bright_cyan',error='Missing Vendor Information',end_s=False)
                return scan_result_options()
            def print_all():
                build(columns,devices,style='bright_cyan',end_s=False)
                return scan_result_options()
            def clean():
                clear()
            def scan_result_options():
                try:
                    network_scan_menu()
                    scan_result()
                    option=input("[Choose an option>]: ")
                    options_list={
                            "1":  print_vendor_found,
                            "2":  print_vendor_not_found,
                            "3":  print_all,
                            "4":  scan_network,
                            "00": back,
                            "99": clean,
                            "0":  Quit,
                            }
                    options_matcher(option,options_list)
                except Exception as e:
                    print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                    return False
            scan_result_options()
        else:
            echo(style("[!] Internet Access ERROR: The Network is unrecheable...", fg='bright_red'))
            return False
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
        return False

def devices_utils_options():
    def clean():
        clear()
    try:
        devices_utils_menu()
        option=input("[Choose an option [int]>]: ")
        options_list= {
                "1":  list_devices,
                "2":  connect,
                "3":  scan_network,
                "4":  disconnect,
                "5":  select_device,
                "6":  enable_remote_connect,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !='0':
            devices_utils_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
