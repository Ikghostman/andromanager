#!/bin/python3

''' Tool menus defined here '''

from modules.build_table import builder as build
from modules.banners import main_banner as banner

def main_menu():
    columns= {
            "Android Manage Tool Menu": 'gold3',
            "Descriptions": 'deep_pink2',
            }

    rows= {
            "1.  ADB daemon": "Check, Start or Kill ADB Server",
            "2.  Devices":"Connected Devices Utilities",
            "3.  Ghather Device Informations": "Android device basic informations access",
            "4.  Advanced Access": "Advanced Management of device through ADB Operations",
            "5.  Goolgle FRP Bypass": "Try to bypass google frp on Android and Samsung",
            "6.  Power Manage": "Device Reboot Options",
            "99. Clear": "Clear Terminal",
            "0.  Exit": "Exit Android Manage Tool",
            }
    banner()
    build(columns,rows,style='bright_cyan',end_s=False)

def adb_utils_menu():
    columns= {
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }

    rows= {
            "1.  Check": "Check ADB daemon status",
            "2.  Start": "Start ADB daemon [server]",
            "3.  Stop": "Kill ADb daemon [server]",
            "4.  Restart": "Restart ADB daemon [server]",
            "99. Clear": "Clear Terminal",
            "0.  Return": "Back to Main mennu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def device_infos_menu():
    columns= {
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows= {
            "1.  Gather Device Infos": "Gather target device inforamtions",
            "99. Clear": "Clear Terminal screen",
            "0.  Return": "Go back to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def devices_utils_menu():
    columns= {
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows= {
            "1.  List devices": "List all connected devices",
            "2.  Connect": "Connect a device using IP Address [ADB TCP connection]",
            "3.  Scan Network": "Scan local network for devices discovery",
            "4.  Disconnect": "Disconnect a device",
            "5.  Select": "Select a device to manage",
            "6.  Enbale TCP connection": "Ability to connect to device using its IP over WI-FI",
            "99. Clear": "Clear Terminal screen",
            "0.  Return": "Go back to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def frp_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Android Goolgle FRP Bypass": "Assumes That ADB is already enabled",
            "2.  SAMSUNG FRP Bypass": "Try enable ADB and Bypass SAMSUNG FRP",
            "99. Clear": "Clear Terminal scren",
            "0.  Return": "Go back to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def device_access_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1"
            }
    rows={
            "1.  Shell": "Access to device shell [Terminal]",
            "2.  Camera Access": "Capture screenshot or Record [Anonymously]",
            "3.  Record or Stream audio": "Record or Stream audio from target device",
            "4.  File Manager": "Download, upload, copy, etc ... list files of target device",
            "5.  APP Manager": "Manage app packages: install, uninstall, extract , etc..",
            "6.  More Access": "Open links, upload and open files, mirror and many more ...",
            "7.  Telephony Datas": "Dumps Contatcs, Calls, etc ...",
            "99. Clear": "Clear Terminal Screen",
            "0.  Return": "Go back to Main menu",
            "00. Exit": "Exit Android Manage Tool"
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def power_manager_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Reboot": "Restart device",
            "2.  Recovery": "Reboot Device into recovery mode",
            "3.  Fastboot": "Reboot devcei into fastboot mode",
            "4.  Bootloader": "Reboot device inot bootloader",
            "99. Clear": "Clear Terminal screen",
            "0.  Return": "Go back to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def network_scan_menu():
    columns={
            "Options": "gold3",
            "Decriptions": "deep_pink1",
            }
    rows={
            "1.  IP with Vendor": "List Hots found with vendor informations",
            "2.  IP without vendor": "List Hosts found without vendor informations",
            "3.  All": "List all discovered hosts",
            "4.  Rescan": "Rescan network and update discovered hosts",
            "00. Return": "Go back to Main menu",
            "99. Clear": "Clear Terminal screen",
            "0.  Exit": "Exit Android Manage Tool"
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def cam_access_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Screenshot": "Capture screenshot [Anonymously]",
            "2.  Record screen": "Record target device screen for a given time [Anonymously]",
            "3.  Back": "Back to Device Accessed menu",
            "99. Clear": "Clear Terminal screen",
            "0.  Return": "Return to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def file_manager_menu():
    columns={
            "options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Download": "Download a file form target device",
            "2.  Upload": "Upload a file to target device",
            "3.  List": "List target device files",
            "4.  Copy Whatsapp": "Copy target device Whatsapp Messenger or Bussiness datas",
            "5.  Copy Images": "Copy target device Images",
            "6.  Back": "Back to Device Access menu",
            "0.  Return": "Return to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def app_manager_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Install": "Install apk file on target device",
            "2.  Uninstall": "Uninstall apk file on target device",
            "3.  List apps": "List applications installed on target device",
            "4.  Lauch": "Launch an installed app on target device",
            "5   Extract": "Extract app package form target device",
            "6.  Back": "Back to Device Accessed menu",
            "99. Clear": "Clear Terminal screen",
            "0.  Return": "Go back to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)
            
def copy_whatsapp_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  WhatsApp Messenger": "Copy whatsapp messenger datas",
            "2.  Wa Bussiness": "Copy WhatsApp Business datas",
            "3.  Back": "Back to File Manager options",
            "0.  Return": "Return To Main menu",
            "99. Clear": "Clear Terminal screen",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def microphone_access_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Record Audio": "Record  audio using target device",
            "2.  Stream Audio": "Stream audio from targer device",
            "3.  Back": "Go back to Device Access menu",
            "0.  Return": "Go back to Main menu",
            "99. Clear": "Clear Terminal screen",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def keycodes_menu():
    cols={
            "KEYCODES MENU": "green",
            "Send Keycodes to target device": "bright_blue",
            }
    rws={
            "99. Clear": "Enter 99 to Clear Terminal screen",
            "0.  Back": "Enter 0 to back to Advanced Access Options",
            "00. Exit": "Enter 00  to exit Android Manage Tool",
            }
    build(cols,rws,style='bright_cyan',end_s=False)
    columns={
            "Keycodes": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1":  "Keyboard Text Input",
            "2":  "Press HOME",
            "3":  "Press Back",
            "4":  "Access Recent Apps",
            "5":  "Press power Button",
            "6":  "Press DPAD UP",
            "7":  "Press DPAD DOWN",
            "8":  "Press DPAD LEFT",
            "9":  "Press DPAD RIGHT",
            "10": "Delete/Backspace press",
            "11": "Press ENTER",
            "12": "Press Volume UP",
            "13": "Press Volume Down",
            "14": "Meda Play",
            "15": "Media Pause",
            "16": "Press TAB",
            "17": "Press ESC",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def advanced_access_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Mirror device": "Mirror target device screen",
            "2.  Open Photo": "Upload and open photo on target device",
            "3.  Open Audio": "Upload and open audio file on target device",
            "4.  Open video": "Upload and open video on target device",
            "5.  Open link": "Open link on target device",
            "6.  Send Keydcodes": "Send keycodes to target device",
            "7.  Unlock": "Unlock device",
            "8.  Lock": "Lock device",
            "9.  Back": "Back Device Acess Options",
            "99. Clear": "Clear Terminal screen",
            "0.  Return": "Retrun to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)

def telephony_access_menu():
    columns={
            "Options": "gold3",
            "Descriptions": "deep_pink1",
            }
    rows={
            "1.  Dump Contacts": "Dump target device contacts",
            "2.  Dump Calls": "Dump target device calls logs",
            "3.  Dump SMS": "Dump target device messages",
            "4.  Send SMS": "Use target device to send sms to a specified phone number",
            "5.  Back": "Back to Device Access Options",
            "99. CLear": "Clear Terminal screen",
            "0.  Return": "Return to Main menu",
            "00. Exit": "Exit Android Manage Tool",
            }
    build(columns,rows,style='bright_cyan',end_s=False)
