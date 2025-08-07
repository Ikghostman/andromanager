#!/bin/python3

from modules import andromanager
from modules.banners import main_banner as banner
from rich.table import Table
from rich.console import Console
import os
import sys
from subprocess import getoutput as get_data
from colorama import Fore
from click import echo, style, prompt
import time
import platform

def check_required_tools(output_style,sleeper=False):
    operating_sys=platform.system()
    distros=[
            'Linux',
            'Darwin',
            ]
    if  operating_sys not in distros:
        print(f"{Fore.RED}[*] Android Manage Tool is only for linux.{Fore.RESET}{Fore.GREEN}Your OS: {operating_sys}")
        sys.exit()
    else:
        required_tools=[
                'nmap',
                'adb',
                'scrcpy',
                'shodan',
                'xterm',
                ]
        try:
            status={}
            global missings
            missings=[]
            for required in required_tools:
                status[required]=os.system(f"which -s {required}")
            echo(style("[*] Checking required tools ...",fg='bright_yellow'))
            for key, value in status.items():
                if value != 0:
                    if output_style==1:
                        print(f"[*] {Fore.LIGHTWHITE_EX}{key} {Fore.RED}is missing{Fore.RESET}..........{Fore.GREEN}checked for installion setps guide{Fore.RESET}")
                    else:
                        print(f"[*] {Fore.LIGHTWHITE_EX}{key} {Fore.CYAN}..........{Fore.RESET}{Fore.RED}is missing{Fore.RESET}")
                    time.sleep(0.5)
                    missings.append(key)
                    status_code=1
                else:
                    print(f"{Fore.YELLOW}[*]{Fore.RESET} {Fore.LIGHTWHITE_EX}{key}{Fore.RESET}...........{Fore.GREEN}Found{Fore.RESET}")
                    if sleeper==True:
                        time.sleep(0.5)
                        status_code=0
                    else:
                        pass
                        status_code=0
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}{Fore.RESET}")
    if status_code==0:
        return True
    else:
        return False

def check_missings_tools():
    installation_commands={
            "nmap": "sudo apt-get install nmap",
            "adb": "sudo apt-get install adb",
            "scrcpy": "Check the github repo",
            "shodan": "pip3 install shodan",
            'xterm': "sudo apt-get install xterm",
                }
    tools_sites={
            "nmap": "https://nmap.org",
            "adb": "https://developer.android.com/studio/releases/platform-tools",
            "scrcpy": "https://github.com/Genymobile/scrcpy",
            "shodan": "https://github.com/achillean/shodan-python",
            "xterm": "https://invisible-island.net/xterm/xterm.html",
            }
    table,console=Table(),Console()
    try:
        echo(style("[*] Generating missing required tools installations steps guide...",fg='bright_yellow'))
        columns={
                "Missing Tools":"bright_white",
                "Installions commands": "bright_cyan",
                "Sites": "blue"
                }
        for key, value in columns.items():
            table.add_column(key,style=value)
        for tool in missings:
            table.add_row(tool,installation_commands[tool],tools_sites[tool])
        console.print(table)
        echo(style("[*] Install the above missing required tools for better usage of the Tool",fg='yellow'))
        echo(style("....................................................................",fg='bright_white'))
        
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")



def check_dependencies():
    
    global RUN_TOOL_STATUS_1
    
    RUN_TOOL_STATUS_1=False
    
    try:
        echo(style("[*] Checking requirement from requirements.txt ... Please wait",fg='bright_yellow'))
        packages={}
        to_install=[]
        pkg_list=[]
        pkg_data=get_data(f"cat requirements.txt|cut -d '=' -f 1 ").strip().split('\n')
        for pkg in pkg_data:
            pkg_list.append(pkg)
        for pkg in pkg_list:
            packages[pkg]=get_data(f"pip3 show {pkg}|grep 'Name'|cut -d ':' -f 2").strip()
        r=open('requirements.txt',encoding='utf-8').readlines()
        for line in r:
            for key, value in packages.items():
                if key != value:
                    if str(key) in line:  # for requirement version print purpose
                        print(f"[*]{Fore.RED} Missing requirement......{Fore.RESET} {Fore.MAGENTA}{line.strip()}{Fore.RESET}")
                        time.sleep(0.5)
                        to_install.append(key)
                else:
                    if str(key) in line:
                        print(f"{Fore.GREEN}[*] Requirement{Fore.RESET} {Fore.LIGHTWHITE_EX}{line.strip()}{Fore.RESET} {Fore.GREEN}already satisfied.{Fore.RESET}")
                        time.sleep(0.5)
        if len(to_install)!=0:
            print(f"{Fore.YELLOW}[*] Run{Fore.RESET} {Fore.GREEN}pip3 -m install -r requirements.tx{Fore.RESET} {Fore.YELLOW}to install missing requirements{Fore.RESET}")
        else:
            echo(style("[*] All requirements already satisfied.",fg='bright_green'))
            RUN_TOOL_STATUS_1=True
    except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            sys.exit()


def main():
    
    RUN_TOOL_STATUS_2=False
    
    try:
        banner()
        echo(style("[*] Initalizing Android Manage Tool requirements check up ...",fg='bright_yellow'))
        time.sleep(0.5)
        check_required_tools(sleeper=True,output_style=1)
        time.sleep(0.5)
        
        if len(missings)!=0:
            time.sleep(0.5)
            check_missings_tools()
            time.sleep(0.5)
            check_dependencies()
        else:
            time.sleep(0.5)
            echo(style("[*] All required tools already installed.",fg='bright_green'))
            RUN_TOOL_STATUS_2=True
            echo(style("......................................................................",fg='bright_white'))
            check_dependencies()
        if RUN_TOOL_STATUS_1==True and RUN_TOOL_STATUS_2==True:
            print(f"\n")
            echo(style("Press ENTER to start Android Manage Tool",fg="bright_yellow",blink=True))
            run=input()
            andromanager.main_options()
        else: 
            print(f"\n")
            echo(style("[*] Install the missings required tools or requirements before running the tool.",fg='bright_red'))
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()

if __name__=="__main__":
    main()
