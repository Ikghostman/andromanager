#!/bin/python3

from modules.banners import main_banner as banner
from modules.menus import device_access_menu, microphone_access_menu, cam_access_menu, file_manager_menu
from modules.menus import app_manager_menu, keycodes_menu, advanced_access_menu, telephony_access_menu
from modules.utils import back, clear, Quit, open_file, options_matcher, is_device_found
from modules.build_table import builder as build
from click import echo, style, prompt
from colorama import Fore
from subprocess import getoutput as get_data
import os
import time
import subprocess
import datetime

class ShellAccess:
    '''Class definied for further functions related to shell utils. but on shell access for now.'''
    
    def get_shell():
        try:
            if is_device_found():
                os.system("adb shell")
                banner()
                return device_access_options()
            else:
                return device_access_options()
        except Exception as e:
            print(f"{Fore.RED}ERROR: {Fore.YELLOW}{e}{Fore.RESET}")
            devices_acess_options()
        except KeyboardInterrupt:
            Quit()

class CameraAccess:
   
    '''Target device camera access classs for capturing screenshots and screen recording.''' 
    
    def screenshot():
    
        try:
            if is_device_found():
                echo(style("Enter output dircetory for screenshots or press enter for default", fg='bright_yellow'))
                output_dir=prompt("[path/to/location] The defaut path is:",default='files/screenshots')
                time = datetime.datetime.now()
                file_name = f"screenshot-{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}-{time.second}.png"
                os.system(f"adb shell screencap -p /sdcard/{file_name}")
                print(f"{Fore.GREEN}[*] Saving png file to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET}")
                info_columns={
                        "File Type": "magenta",
                        "File Location Information": "blue",
                        }
                info_rows={
                        "PNG": f"{os.getcwd()}/{output_dir}/{file_name}",
                        }
                os.system(f"adb pull /sdcard/{file_name} {output_dir}>/dev/null")
                os.system(f"adb shell rm /sdcard/{file_name}")
                build(info_columns,info_rows,style='bright_cyan',end_s=True)
            
                option=prompt("[Do yout want to open png file (y/n) ? >] ")
                if option.lower()=='y' or option.upper()=='Y':
                    open_file(filename=f"{output_dir}/{file_name}")
                    return cam_access_options()
                    
                else:
                    return cam_access_options()
                    
            else:
                return cam_access_options()
                
        except Exception as e:
            print(f"{Fore.RED}ERROR: {Fore.YELLOW}{e}")
            return cam_access_options()
            
        except KeyboardInterrupt:
            Quit()
        

    def record_screen():
        try:
            if is_device_found():
                echo(style("[Enter output directory for recorded video or press enter for default (No Copy Paste Please)>] ",fg='bright_yellow'))
                output_dir=prompt("[path/to/location] The default path is:",default='files/videos/screenrecords')
                time=datetime.datetime.now()
                file_name = f"video-{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}-{time.second}.mp4"
                duration =prompt("Enter the duration [in seconds] ")
                echo(style("Target device Screen Recording started...", fg='bright_yellow'))
                os.system(
                        f"adb shell screenrecord  --time-limit {duration} /sdcard/{file_name}>/dev/null"
                        )
                print(f"{Fore.GREEN}[*]Saving video to {Fore.RESET}{Fore.BLUE}{output_dir}...{Fore.RESET}")
                info_columns={
                        "File Type": "magenta",
                        "Location Information": "blue",
                        }
                info_rows={
                        "MP4": f"{os.getcwd()}/{output_dir}/{file_name}",
                        }
                os.system(f"adb pull /sdcard/{file_name} {output_dir}>/dev/null")
                os.system(f"adb shell rm  /sdcard/{file_name}>/dev/null")
                build(info_columns,info_rows,style='bright_cyan',end_s=True)
                option=prompt("[Do you want to watch the mp4 file (y/n) ? >] ")
                if option.lower()=='y' or option.upper()=='Y':
                    open_file(filename=f"{output_dir}/{file_name}")
                    return cam_access_options()
                    
                else:
                    return cam_access_options()
                    
            else:
                return cam_access_options()
                
        except Exception as e:
            print(f"{Fore.RED}ERROR: {Fore.YELLOW}{e}")
            return cam_access_options()
            
        except KeyboardInterrupt:
            Quit()
        


class FileManager:
    
    '''Files handling class. Used to download, upload ,list target device files, etc ...'''
    
    def download_file():
        try:
            if is_device_found():
                echo(style("Enter target file's path on device (without /sdcard) e.g Xender/data): ",fg='bright_yellow'))
                path=prompt("[path/to/file] ")
                echo(style("[Enter output directory to save file or press enter for defaut (No Copy Paste Please)",fg='bright_yellow'))
                output_dir=prompt("[path/to/location] The deafult path is:",default='files/downloads/pulled_..files')
                if os.system(
                        f"adb shell test -e /sdcard/{path}"
                        )==0:
                    pass
                else:
                    echo(style("[!] Target file or path does not exsit",blink=True,fg='bright_red'))
                    time.sleep(0.5)
                    return file_manager_options()
                    
                print(f"{Fore.GREEN}[*] Saving {path} to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} ...")
                file_path=path.split("/")
                file_name=file_path[len(file_path)-1]
                get_type=file_name.split(".")
                file_type=get_type[len(get_type)-1].upper()
                info_col= {
                        "File Type": "magenta",
                        "Path on device": "blue",
                        "Location on computer": "bright_blue",
                        }
                info_row={
                        f"{file_type}": f"/sdcard/{path}",
                        }
                os.system(f" adb  pull /sdcard/{path} {output_dir}/{file_name} > /dev/null")
                build(info_col,info_row,style='bright_cyan',end_s=True,sr=f"{os.getcwd()}/{output_dir}/{file_name}")
                option=prompt("[Do yout want to open the file[y/n] ? (Only for media types. Check file name before)] ")
                if option.lower()=='y' or option.upper()=='Y':
                    open_file(filename=f"{output_dir}/{file_name}")
                    return file_manager_options()
                    
                else:
                    return file_manager_options()
                    
            else:
                return file_manager_options()
                
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {e}")
            return file_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        

    def upload_file():

        try:
            if is_device_found():
                echo(style("[*] Sepcify path to the file in computer (No Copy Paste Please): ", fg='bright_yellow'))
                file_path=input("[path/to/file>]: ")
                if file_path == "":
                    echo(style("[!] No File path sepcified ...",blink=True,fg='bright_red'))
                    times.sleep(0.5)
                    return file_manager_options()
                    
                else:
                    file_status=os.system(f"test -e {file_path}")
                    if file_status==0:
                        pass
                    else:
                        echo(style("[i] Specified file path not found", fg='red'))
                        time.sleep(0.5)
                        return file_manager_options()
                        
                    echo(style("[*] Destination directory in device (No Copy Paste please): ",fg='bright_yellow'))
                    destination=prompt("[Enter destion path on device>] ")
                    get_type=file_path.split("/")
                    file_name=get_type[len(get_type)-1]
                    name=file_name.split(".")
                    file_type=name[len(name)-1].upper()
                    print(f"{Fore.LIGHTGREEN_EX}[*] Uploading {Fore.LIGHTWHITE_EX}{file_name}{Fore.RESET} {Fore.LIGHTGREEN_EX}to target device{Fore.RESET} ...")
                    os.system(f"adb push {file_path} {destination}/{file_name} > /dev/null")
                    info_columns={
                            "File Type": "magenta",
                            "Path on computer": "bright_blue",
                            "Destination path on device": "blue",
                            }
                    info_rows={
                            f"{file_type}": f"{file_path}",
                            }
                    print(f"{Fore.GREEN}[i]{Fore.RESET} {Fore.RED}{file_name}{Fore.RESET} {Fore.GREEN}uploaded successfully to target device{Fore.RESET}")
                    build(info_columns,info_rows,style='bright_cyan',end_s=True,sr=f"{destination}/{file_name}")
                    medias_types=[
                            "MP3",
                            "MP4",
                            "PNG",
                            "JPG",
                            "JPEG",
                            "AVI",
                            "MPEG",
                            "MPG",
                            ]
                    for f_type in medias_types:
                        while file_type==f_type:
                            option=input(f"[Do you want to open {Fore.YELLOW}{file_name}{Fore.RESET} on target device (y/n) ?>]: ")
                            if option.lower()=='y' or option.upper()=='Y':
                                path=file_path
                                mimetype==magic.from_file(path,mime=True)
                                mimetype=mimetype.split("/")
                                file_type=mimetype[0]
                                file_ext=mimetype[1]
                                print(f"{Fore.MAGENTA}[*] Playing{Fore.RESET} {Fore.RED}{file_name}{Fore.RESET} {Fore.MAGENTA}on target device ...{Fore.RESET}")
                                os.system(
                                        f'adb shell am start -a android.intent.action.VIEW -d "file:///{destination}/{file_name}" -t {file_type}/{file_ext}>/dev/null'
                                        )
                                return file_manager_options()
                                
                            else:
                                return file_manager_options()
                                
                        else:
                            return file_manager_options()
                            
            else:
                return file_manager_options()
                

        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return file_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        
    
    def list_files():
        try:
            if is_device_found():
                files=get_data(f"adb shell ls -l -p /sdcard/")
                columns={
                        "": "",
                        "Android Device Files": "bright_green"
                        }
                rows={
                        "": files,
                        }
                build(columns,rows,style='bright_cyan',end_s=True)
                option=input(f"{Fore.RED}[Do you want to recurisvely list a specific directory (y/n) ?>]: {Fore.RESET}")
                if option.lower()=='y' or option.upper()=='Y':
                    directory=input(f"{Fore.GREEN}[Enter directory name] (without /sdcard/ e.g Xender): {Fore.RESET}")
                    dir_contents=get_data(f"adb shell ls -R /sdcard/{directory}")
                    columns={
                            "": "",
                            f"/sdcard/{directory} contents": "bright_green",
                            }
                    rows={
                            "":dir_contents,
                            }
                    build(columns,rows,style='bright_cyan',end_s=True)
                    return file_manager_options()
                    
                else:
                    return file_manager_options()
                    
            else:
                return file_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR: {Fore.YELLOW}{e}")
            return file_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        
    
    def copy_whatsapp_data():
        try:
            if is_device_found():
                columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                rows={
                        "1.  Whatsapp Messenger": "Copy Whatsapp Messenger Datas",
                        "2.  Wa Bussiness": "Copy Whatsapp Business Datas",
                        "3.  Back": "Back to File Manager option",
                        "0.  Return": "Return to Main menu",
                        "99. Clear": "Clear Terminal screen",
                        "00. Exit": "Exit Android Manage Tool",
                        }
                build(columns,rows,style='bright_cyan',end_s=False)
                option=input("[Choose an option>]: ")
                if option=='1':
                    echo(style("Enter outpout directory to save Whatsapp Messenger datas or press enter for default (No Copy Paste Please): ",fg='yellow'))
                    output_dir=prompt("[path/to/location>] The default path is: ",default='files/downloads/WhatsAppMessenger')
                    if os.system(
                            f'adb shell test -d "/sdcard/Android/media/com.whatsapp/WhatsApp"'
                            )==0:
                        data_path="/sdcard/Android/media/com.whatsapp/WhatsApp"
                    elif os.system(
                            f'adb shell test -d "/sdcard/WhatsApp"'
                            )==0:
                        data_path="/sdcard/WhatsApp"
                    else:
                        banner()
                        echo(style("[!] WhatsApp Messenger Folder not found on target device",fg='red'))
                        time.sleep(0.5)
                        return FileManager.copy_whatsapp_data()
                        
                    print(f"{Fore.GREEN}[i] Saving data to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} ...")
                    os.system(
                            f"adb pull {data_path} {output_dir}>/dev/null"
                            )
                    banner()
                    print(f"{Fore.LIGHTGREEN_EX}[i] Target device WhatsApp Messenger Datas copied successfully to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET}")
                    return FileManager.copy_whatsapp_data()
                    
            
                elif option=='2':
                    echo(style("Enter outpout directory to save Whatsapp Bussiness datas or press enter for defaut (No Copy Paste Please): ",fg='yellow'))
                    output_dir=prompt("[path/to/location>] The default path is: ",default='files/downloads/WaBussiness')
                    wa_dir_1=r"/sdcard/Android/media/com.whatsapp.w4b/WhatsApp\ Bussiness"
                    wa_dir_2=r"/sdcard/Android/WhatsApp\ Bussiness"
                    if os.system(
                            f'adb shell test -d {wa_dir_1}')==0:
                        data_path=r"/sdcard/Android/media/com.whatsapp.4web/WhatsApp\ Business"
                    elif os.system(
                            f'adb shell test -d "{wa_dir_2}')==0:
                        data_path=r"/sdcard/WhatsApp\ Bussiness"
                    else:
                        banner()
                        echo(style("[!] Whatsapp Bussiness Folder not found on target device",fg='red'))
                        return FileManager.copy_whatsapp_data()
                        
                    print(f"{Fore.GREEN}[i] Saving data to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} ...")
                    os.system(
                            f"adb pull {data_path} {output_dir}>/dev/null"
                            )
                    banner()
                    print(f"{Fore.LIGHTGREEN_EX}[i] Target device WhatsApp Bussiness Datas copied successfully to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET}")
                    return FileManager.copy_whatsapp_data()
                    
                elif option=='3':
                    banner()
                    file_manager_options()
                elif option=='99':
                    clear()
                    banner()
                    return FileManager.copy_whatsapp_data()
                elif option=='0':
                    back()
                elif option=='00':
                    Quit()
                else:
                    echo(style("[*] Unrecognized option, returning ...",blink=True,fg='red'))
                    time.sleep(0.5)
                    banner()
                    return FileManager.copy_whatsapp_data()
            else:
                return file_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return FileManager.copy_whatsapp_data()
            
        except KeyboardInterrupt:
            Quit()
        
    
    def copy_images():
        try:
            if is_device_found():
                columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                rows={
                        "1.  Copy Camera": "Copy All images in the /DCIM/Camera Folder",
                        "2.  Copy Screenshots": "Copyt All screeshots images",
                        "3.  Pictures": "Copy images in the pictures directory [include screenshots]",
                        "4.  Back": "Back to File Manager options",
                        "99. Clean": "Clear Terminal screen",
                        "0.  Return": "Go back to Main menu",
                        "00. Exit": "Exit Android Manager tool",
                        }
                build(columns,rows,style='bright_cyan',end_s=False)
                option=input("[Choose an option>]: ")
                if option=='1':
                    echo(style("Enter output directory to save Camera Photos or press enter for default (No Copy Paste Please): ",fg='bright_yellow'))
                    output_dir=prompt("[path/to/location>] The default is: ",default='files/images/camera')
                    if os.system(
                            f'adb shell test -d "/sdcard/DCIM/Camera"'
                            )==0:
                        data_path="/sdcard/DCIM/Camera"
                    else:
                        banner()
                        echo(style("[!] The Specified photos path does not exist",fg='red'))
                        time.sleep(0.5)
                        return FileManager.copy_images()
                        
                    print(f"{Fore.GREEN}[i] Saving Camera Images to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} ...")
                    os.system(
                            f"adb pull {data_path} {output_dir}>/dev/null"
                            )
                    banner()
                    print(f"{Fore.LIGHTGREEN_EX}[i] Target device Camera Images copied successfully to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET}")
                    return FileManager.copy_images()
                    
            
                elif option=='2':
                    echo(style("Enter output directory to save screenshots or press enter for default (No Copy Paste Please): ",fg='bright_yellow'))
                    output_dir=prompt("[path/to/location>] The default path is: ",default='files/images/screenshots')
                    if os.system(
                            f'adb shell test -d "/sdcard/Pictures/Screenshots"'
                                )==0:
                        data_path="/sdcard/Pictures/Screenshots"
                    else:
                        banner()
                        echo(style("[!] The Specified photos path does not exist",fg='red'))
                        return FileManager.copy_images()
                        
                    print(f"{Fore.GREEN}[i] Saving scrennshots Images to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} ...")
                    os.system(
                            f"adb pull {data_path} {output_dir}>/dev/null"
                            )
                    banner()
                    print(f"{Fore.LIGHTGREEN_EX}[i] Target device Screenshots copied successfully to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET}")
                    return FileManager.copy_images()
                    
            
                elif option=='3':
                    echo(style("Enter output directory to save Pictures or press enter for default (No Copy Paste Please): ",fg='bright_yellow'))
                    output_dir=prompt("[path/to/location>] The default path is: ",default='files/images/pictures')
                    if os.system(
                        f'adb shell test -d "/sdcard/Pictures"'
                        )==0:
                        data_path="/sdcard/Pictures"
                    else:
                        banner()
                        echo(style("[!] The Specified photos path does not exist",fg='red'))
                        time.sleep(0.5)
                        return FileManager.copy.images()
                        
                    print(f"{Fore.GREEN}[i] Saving pictures Images to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} ...")
                    os.system(
                            f"adb pull {data_path} {output_dir}>/dev/null"
                            )
                    banner()
                    print(f"{Fore.LIGHTGREEN_EX}[i] Target device Pictures copied successfully to{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET}")
                    return FileManager.copy_images()
                    
                elif option=='99':
                    banner()
                    return FileManager.copy_images()
                elif option=='0':
                    back()
                elif option=='00':
                    Quit()
                else:
                    banner()
                    echo(clik.style("[!] Unrecongnized option, returning ...",blink=True,fg='red'))
                    time.sleep(0.5)
                    return FileManager.copy_images()
            else:
                return file_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR: {Fore.YELLOW}{e}")
            return FileManager.copy_images()
            
        except KeyboardInterrupt:
            Quit()
        


class AppManager:

    '''Class for android device applicaton management. Used to install, uninstall, list or extract apps.'''

    def install_app():
        try:
            if is_device_found():
                echo(style("Enter path to apk file in computer (No Copy Paste Please): ",fg='bright_yellow'))
                app =input("[path/to/file>]: ")
                if app=="":
                    echo(style("[i] No file path specified !",blink=True,fg='red'))
                    time.sleep(0.5)
                    return app_manager_options()
            
                apk_file=app.strip('')
                if not os.path.isfile(apk_file):
                    banner()
                    echo(style("[i] The sepicied file does not exist !",fg='bright_red'))
                    time.sleep(0.5)
                    return app_manager_options()
                if apk_file.endswith(".apk")  or apk_file.endswith(".apex"):
                    status_columns={
                            "APK File": "magenta",
                            "Installation Status": "bright_green",
                            }
                    status_rows={
                            f"{apk_file}": "Installed Successfully on device"
                            }
                    app_name=apk_file.split("/")
                    name=app_name[-1]
                    print(f"{Fore.LIGHTGREEN_EX}[*] Installing{Fore.RESET} {Fore.WHITE}{name}{Fore.RESET} {Fore.LIGHTGREEN_EX}on device ...{Fore.RESET}") 
                    if  os.system(f"adb install {apk_file}>/dev/null")==0:
                        banner()
                        build(status_columns,status_rows,style='bright_cyan',end_s=True)
                        return app_manager_options()
                        
                    else:
                        banner()
                        status_rows[f"{apk_file}"]="Installation Aborted. Missing device or package ERROR"
                        status_columns['Installation Status']='bright_red'
                        build(status_columns,status_rows,style='bright_cyan',end_s=True)
                        return app_manager_options()
                else:
                    banner()
                    print(f"{Fore.RED}[i] The specified file is not installable !{Fore.RESET}")
                    return app_manager_options()
                    
            else:
                return app_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return app_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        
        


    def uninstall_app():
        try:
            if is_device_found():
                columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                rows={
                        "1. Select form list": "A list of applications",
                        "2. Package Name": "Manually enter package name",
                        }
                build(columns,rows,style='bright_cyan',end_s=False)
                option = prompt("[Choose an option]> ")
                if option=='1':
                    banner()
                    app_list=get_data(f"adb shell pm list packages -3").split("\n")
                    columns={
                            "Indexes":"red",
                            "Target Device third party Applications": "Bright_white",
                            }
                    rows={}
                    i=0
                    for app in app_list:
                        i+=1
                        app=app.replace("package:", "")
                        rows[str(i)]=app
                    build(columns,rows,style='bright_cyan',end_s=False)
                    app =input("[Choose app index [int]>] ")
                    if app=="":
                        echo(style("No index provide !",fg='red'))
                        time.sleep(0.5)
                        banner()
                        return app_manager_options()
                    if app not in rows.keys():
                        echo(style("Invalid index provided",fg='red'))
                        time.sleep(0.5)
                        banner()
                        return app_manager_options()

                    else:
                        match app:
                            case opt:
                                for key, value in rows.items():
                                    if key==opt:
                                        package = rows[key]
                    print(f"{Fore.RED}[*] Uninstalling{Fore.RESET} {Fore.WHITE}{package}{Fore.RESET}")
                    os.system(f"adb uninstall {package}>/dev/null")
                    print(f"{Fore.YELLOW}{package}{Fore.RESET} {Fore.GREEN}uninstalled successfully from target device{Fore.RESET}")
                    return app_manager_options()
                    

                elif option == "2":
                    banner()
                    echo(style("Enter Package Name: ",fg='bright_yellow'))
                    package_name = prompt("[pkgname>] ")
                    if package_name == "":
                        banner()
                        echo(style("[!] No package name provided !",blink=True,fg='brigh_red'))
                        time.sleep(0.5)
                        return app_manager_options()
                        
                    else:
                        banner()
                        os.system(f"adb uninstall {package_name}>/dev/null")
                        print(f"{Fore.YELLOW}{package_name}{Fore.RESET} {Fore.GREEN}uninstalled sucessfully from target device{Fore.RESET}")
                        return app_manager_options()
                        
                else:
                    banner()
                    echo(style("[!] Invalid Selection !",fg='red'))
                    time.sleep(0.5)
                    return app_manager_options()
                    
            else:
                return app_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return app_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        


    def launch_app():
        try:
            if is_device_found():
                columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                rows={
                        "1. Select form list": "A list of applications",
                        "2. Package Name": "Manually enter package name",
                        }
                build(columns,rows,style='bright_cyan',end_s=False)
                option = input("[Choose an option>]: ")
                if option=='1':
                    banner()
                    app_list=get_data(f"adb shell pm list packages -3").split("\n")
                    columns={
                            "Index":"red",
                            "Applications": "Bright_white",
                            }
                    rows={}
                    i=0
                    for app in app_list:
                        i+=1
                        app.replace("package:", "")
                        rows[str(i)]=app
                    build(columns,rows,style='bright_cyan',end_s=False)
                    app = input("[Choose app index [int]>]: ")
                    if app.isdigit():
                        if int(app) <= len(app_list) and int(app) > 0:
                            package = app_list[int(app) - 1].replace("package:", "")
                            banner()
                            print(f"{Fore.GREEN}Running{Fore.RESET} {Fore.YELLOW}{package}{Fore.RESET} {Fore.GREEN}on device ...{Fore.RESET}")
                            os.system(
                                    f"adb shell monkey -p {package} 1"
                                    )
                            return app_manager_options()
                            
                        else:
                            banner()
                            echo(style("[!] Invalid app index ",blink=True,fg='brigh_red'))
                            time.sleep(0.5)
                            return app_manager_options()
                            
                    else:
                        banner()
                        echo(style("[i] Unpexcted Integer detected !",blink=True,fg='red'))
                        time.sleep(0.5)
                        return app_manager_options()
                        

                elif mode == "2":
                    banner()
                    clik.echo(clik.style("Enter Package Name: ",fg='bright_yellow'))
                    package_name = input("[pkgname>]: ")
                    if package_name == "":
                        banner()
                        clik.echo(style("[!] No package name provided !",blink=True,fg='brigh_red'))
                        time.sleep(0.5)
                        return app_manager_options()
                        
                    else:
                        banner()
                        print(f"{Fore.GREEN}Running{Fore.RESET} {Fore.YELLOW}{package}{Fore.RESET} {Fore.GREEN}on device ...{Fore.RESET}")
                        os.system(f"adb shell monkey  -p {package_name} 1")
                        return app_manager_options()
                        
                else:
                    banner()
                    echo(style("[!] Invalid Selection !",fg='red'))
                    time.sleep(0.5)
                    return app_manager_options()
                    
            else:
                return app_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return app_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        


    def list_apps():
        try:
            if is_device_found():
                columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                rows={
                        "1. Third Party APPS": "A list of third party applications",
                        "2. All": "List all available applications on device",
                        }
                build(columns,rows,style='bright_cyan',end_s=False)
                option = input("[Choose an option>]: ")
                if option=='1':
                    banner()
                    app_list=get_data(f"adb shell pm list packages -3").split("\n")
                    columns={
                            "Index":"red",
                            "Applications": "Bright_white",
                            }
                    rows={}
                    i=0
                    for app in app_list:
                        i+=1
                        app.replace("package:", "")
                        rows[str(i)]=app
                    build(columns,rows,style='bright_cyan',end_s=False)
                    return app_manager_options()
                    

                elif option == "2":
                    banner()
                    app_list=get_data(f"adb shell pm list packages").split("\n")
                    columns={
                            "Index":"red",
                            "Applications": "Bright_white",
                            }
                    rows={}
                    i=0
                    for app in app_list:
                        i+=1
                        app.replace("package:", "")
                        rows[str(i)]=app
                    build(columns,rows,style='bright_cyan',end_s=False)
                    return app_manager_options()
                    
                else:
                    banner()
                    echo(style("[!] Invalide selection !",fg='bright_red'))
                    time.sleep(0.5)
                    return app_manager_options()
                    
            else:
                return app_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return app_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        
    def extract_app():
        try:
            if is_device_found():
                columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                rows={
                        "1. Select form list": "A list of applications",
                        "2. Package Name": "Manually enter package name",
                        }
                build(columns,rows,style='bright_cyan',end_s=False)
                option = input("[Choose an option>]: ")
                if option=='1':
                    app_list=get_data(f"adb shell pm list packages -3").split("\n")
                    columns={
                            "Indexes":"red",
                            "Target Device third party Applications": "Bright_white",
                            }
                    rows={}
                    i=0
                    for app in app_list:
                        i+=1
                        app=app.replace("package:", "")
                        rows[str(i)]=app
                    build(columns,rows,style='bright_cyan',end_s=False)
                    app =input("[Choose app index [int]>] ")
                    if app=="":
                        echo(style("No Index selected !",fg='red'))
                        banner()
                        time.sleep(0.5)
                        return app_manager_options()
                    if app not in rows.keys():
                        echo(style("No valid index provided !",fg='red'))
                        time.sleep(0.5)
                        banner()
                        return app_manager_options()
                    else:
                        match app:
                            case opt:
                                for key, value in rows.items():
                                    if key==opt:
                                        global package
                                        package = rows[key]
                    echo(style("Enter output directory to save extracted app or press enter for default (No Copy Paste Please): ",fg='bright_yellow'))
                    output_dir=prompt("[path/to/dir] the default is:",default='files/downloads/extracted_apps')
                    banner()
                    print(f"{Fore.GREEN}[*] Extracting{Fore.RESET} {Fore.YELLOW}{package}{Fore.RESET}")
                    try:
                        path=get_data(f"adb shell pm path {package}")
                        path=path.replace("package:", "")
                        apk_name=path.split("/")
                        apk_name=apk_name[-1]
                        name=package.split('.')
                        name=name[1]
                        if os.path.isfile(f"{output_dir}/{name}.apk"):
                            print(f"{Fore.RED}[i] App alreay exist in{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} {Fore.RED}or it's another one with the same name{Fore.RESET}: {name}.apk{Fore.RESET}")
                            return app_manager_options()
                            
                        else:
                            os.system(f"adb pull {path} temp > /dev/null")
                            os.system(f"mv temp/*.apk {output_dir}/{name}.apk&&rm -f temp/*.apk")
                            print(f"{Fore.YELLOW}[*] Package {package}{Fore.RESET} extracted successfully to {Fore.BLUE}{output_dir}{Fore.RESET}")
                            print(f"{Fore.MAGENTA}[i] Extracted apk name:{Fore.RESET} {Fore.WHITE}{apk_name}{Fore.RESET} {Fore.YELLOW}Renamed to:{Fore.RESET}{Fore.RED} {name}.apk{Fore.RESET}")
                            return app_manager_options()
                            
                    except Exception as e:
                        banner()
                        print(f"{Fore.RED}ERROR: {Fore.YELLOW}{e}{Fore.RESET}")
                        return app_manager_options()
                        

                elif option == "2":
                    echo(style("Enter Package Name: ",fg='bright_yellow'))
                    package= input("[pkgname>] ")
                    if package == "":
                        banner()
                        echo(style("[!] No package name provided !",blink=True,fg='brigh_red'))
                        time.sleep(0.5)
                        return app_manager_options()
                        
                    else:
                        echo(style("Enter output directory to save extracted app or press enter for default (No Copy Paste Please): ",fg='bright_yellow'))
                        output_dir=prompt("[path/to/dir] the default is:",default='files/downloads/extracted_apps')
                        print(f"{Fore.GREEN}[*] Extracting{Fore.RESET} {Fore.YELLOW}{package}{Fore.RESET}")
                        try:
                            path=get_data(f"adb shell pm path {package}")
                            path=path.replace("package:", "")
                            apk_name=path.split("/")
                            apk_name=apk_name[-1]
                            name=package.split(".")
                            name=name[1]
                            if os.path.isfile(f"{output_dir}/{name}.apk"):
                                print(f"{Fore.RED}[i] App alreay exist in{Fore.RESET} {Fore.BLUE}{output_dir}{Fore.RESET} {Fore.RED}or it's another one with the same name{Fore.RESET}: {name}.apk{Fore.RESET}")
                                return app_manager_options()
                                
                            else:
                                os.system(f"adb pull {path} temp > /dev/null")
                                os.system(f"mv temp/*.apk {output_dir}/{name}.apk&&rm -f temp/*.apk")
                                print(f"{Fore.YELLOW}[*] Package {package}{Fore.RESET} extracted successfully to {Fore.BLUE}{output_dir}{Fore.RESET}")
                                print(f"{Fore.MAGENTA}[i] Extracted apk name:{Fore.RESET} {Fore.WHITE}{apk_name}{Fore.RESET} {Fore.YELLOW}Renamed to:{Fore.RESET}{Fore.RED} {name}.apk{Fore.RESET}")
                                return app_manager_options()
                                
                        except Exception as e:
                            banner()
                            print(f"{Fore.RED}ERROR: {Fore.YELLOW}{e}{Fore.RESET}")
                            return app_manager_options()
                            
                else:
                    banner()
                    echo(style("[!] Invalid Selection !",fg='red'))
                    time.sleep(0.5)
                    return app_manager_options()
                    
            else:
                return app_manager_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return app_manager_options()
            
        except KeyboardInterrupt:
            Quit()
        

class MicrophoneAccess():

    '''Android microphone and audio access class. Used to record or stream audio on target device.'''
    
    def record_audio():
        try:
            if is_device_found():
                androversion=get_data(f"adb shell getprop ro.build.version.release")
                version=int(androversion.split('.')[0])
                columns={
                        "Required Android Version": "gold3",
                        "Detected Android Version": "bright_magenta",
                        "Compatibility": "bright_green",
                        }
                rows={
                        "Android 11 or Higher",
                        f"Android {version}",
                        }
                if version < 11:
                    columns['Compatibility']='red'
                    banner()
                    build(columns,rows,sr='False',style='bright_cyan',end_s=False)
                    echo(style("[i] Detected device version does not support the record audio future !",fg='brigh_red'))
                    return microphone_access_options()
                    
                echo(style("[i] Enter output directory to save Recordings or press ENTER for default (No Copy Paste Please): ",fg='bright_yellow'))
                output_dir=prompt("[path/to/dir] the default is: ", default='files/downloads/audio/recordings')
                instant=datetime.datetime.now()
                file_name=f"mic-audio-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.opus"
                mode_columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                mode_rows={
                        "1. Miccrophone": "Use target device microphone to record",
                        "2. Device audio ": "Record Target device audio",
                        }
                build(mode_columns,mode_rows,style='bright_cyan',end_s=False)
                mode=input("[Choose record mode [int]>]: ")
                match mode:
                    case '1':
                        try:
                            option_columns={
                                    "Options": "gold3",
                                    "Descriptions": "deep_pink1",
                                    }
                            option_rows={
                                    "1. Stream and Record": "Stream and record audio on target device",
                                    "2. Record Only": "No streaming. Record only",
                                    }
                            build(option_columns,option_rows,style='bright_cyan',end_s=False)
                            option=input("[Choose an option [int]>]: ")
                            if option=='1':
                                try:
                                    banner()
                                    print(f"{Fore.WHITE}[i] Saving recordings to: {Fore.RESET}{Fore.BLUE}{os.getcwd()}/{output_dir}{Fore.RESET}")
                                    echo(style("[*] Target device microphone audio record tiggered ... Press CTRL+C in xterm to stop",fg='bright_green'))
                                    os.system(
                                            f"xterm -title 'Recording Audio' -bg black -fg cyan -e 'scrcpy --no-video --audio-source=mic --record={output_dir}/{file_name}' &"
                                            )
                                    return microphone_access_options()
                                    
                                except Exception as e:
                                    print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                                    return mircophone_access_options()
                                    
                                except KeyboardInterrupt:
                                    banner()
                                    echo(style("[*] Recording Operation canceled !, audio data saved .",fg='bright_magenta'))
                                    return microphone_access_options()
                                    
                            elif option=='2':
                                try:
                                    banner()
                                    print(f"{Fore.WHITE}[i] Saving recordings to: {Fore.RESET}{Fore.BLUE}{os.getcwd()}/{output_dir}{Fore.RESET}")
                                    echo(style("[*] Target device microphone audio record tiggered ... Press CTRL+C in xterm to stop",fg='bright_green'))
                                    os.system(
                                            f"xterm -title 'Recording Audio' -bg black -fg cyan -e 'scrcpy --no-video --audio-source=mic --no-playback --record={output_dir}/{file_name}' &"
                                            )
                                    return microphone_access_options()
                                    
                                except Exception as e:
                                    print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                                    return mircophone_access_options()
                                    
                                except KeyboardInterrupt:
                                    banner()
                                    echo(style("[*] Recording Operation canceled !, audio data saved .",fg='bright_magenta'))
                                    return microphone_access_options()
                                    
                            else:
                                banner()
                                echo(style("[i] Unrecognized option !",blink=True,fg='red'))
                                time.sleep(0.5)
                                return microphone_access_options()
                                
                        except Exception as e:
                            banner()
                            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                            return microphone_access_options()
                            
                        except KeyboardInterrupt:
                            Quit()
                    case '2':
                        try:
                            file_name=f"device-audio-{file_name}.opus"
                            option_columns={
                                    "Options": "gold3",
                                    "Descriptions": "deep_pink1",
                                    }
                            option_rows={
                                    "1. Stream and Record": "Stream and record audio on target device",
                                    "2. Record Only": "No streaming. Record only",
                                    }
                            build(option_columns,option_rows,style='bright_cyan',end_s=False)
                            option=input("[Choose an option [int]>]: ")
                            if option=='1':
                                try:
                                    banner()
                                    print(f"{Fore.WHITE}[i] Saving recordings to: {Fore.RESET}{Fore.BLUE}{os.getcwd()}/{output_dir}{Fore.RESET}")
                                    echo(style("[*] Target device microphone audio record tiggered ... Press CTRL+C in xterm to stop",fg='bright_green'))
                                    os.system(
                                            f"xterm -title 'Recording Audio' -bg black -fg cyan -e 'scrcpy --no-video  --record={output_dir}/{file_name}' &"
                                            )
                                    choice=prompt(f"[Do yout want to open the recorded audio ? (y/n) ]")
                                    if str(choice).lower()=='y' or str(choice).upper()=='Y':
                                        open_file(filename=f'{output_dir}/{file_name}')
                                        
                                    else:
                                        return microphone_access_options()
                                        
                                except Exception as e:
                                    print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                                    return mircophone_access_options()
                                    
                                except KeyboardInterrupt:
                                    banner()
                                    echo(style("[*] Recording Operation canceled !, audio data saved .",fg='bright_magenta'))
                                    return microphone_access_options()
                                    
                            elif option=='2':
                                try:
                                    banner()
                                    print(f"{Fore.WHITE}[i] Saving recordings to: {Fore.RESET}{Fore.BLUE}{os.getcwd()}/{output_dir}{Fore.RESET}")
                                    echo(style("[*] Target device microphone audio record tiggered ... Press CTRL+C in xterm to stop",fg='bright_green'))
                                    os.system(
                                            f"xterm -title 'Recording Audio' -bg black -fg cyan -e 'scrcpy --no-video --no-playback --record={output_dir}/{file_name}' &"
                                            )
                                    choice=prompt("[Do you want to open recorded audio ? (y/n) ]")
                                    if str(choice).lower()=='y' or str(choice).upper()=='Y':
                                        open_file(filename=f'{output_dir}/{file_name}')
                                        
                                    else:
                                        return microphone_access_options()
                                        
                                except Exception as e:
                                    print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                                    return mircophone_access_options()
                                    
                                except KeyboardInterrupt:
                                    banner()
                                    echo(style("[*] Recording Operation canceled !, audio data saved .",fg='bright_magenta'))
                                    return microphone_access_options()
                                    
                            else:
                                banner()
                                echo(style("[i] Unrecognized option !",blink=True,fg='red'))
                                time.sleep(0.5)
                                return microphone_access_options()
                                
                        except Exception as e:
                            banner()
                            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                            return microphone_access_options()
                            
                        except KeyboardInterrupt:
                            Quit()
                    case other:
                        banner()
                        echo(style("[i] Unrecognized mode ! .",blink=True,fg='red'))
                        time.sleep(0.5)
                        return microphone_access_options()
                        
            else:
                return microphone_access_options()
                

        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return mircophone_access_options()
            
        
    
    def stream_audio():
        try:
            if is_device_found():
                androversion=get_data(f"adb shell getprop ro.build.version.release")
                version=int(androversion.split('.')[0])
                columns={
                        "Required Android Version": "gold3",
                        "Detected Android Version": "bright_magenta",
                        "Compatibility": "bright_green",
                        }
                rows={
                        "Android 11 or Higher",
                        f"Android {version}",
                        }
                if version < 11:
                    columns['Compatibility']='red'
                    banner()
                    build(columns,rows,sr='False',style='bright_cyan',end_s=False)
                    echo(style("[i] Detected device version does not support the record audio future !",fg='brigh_red'))
                    return microphone_access_options()
                    
                mode_columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1",
                        }
                mode_rows={
                        "1. Miccrophone": "Stream using target device microphone",
                        "2. Device audio ": "Stream using target device audio",
                        }
                build(mode_columns,mode_rows,style='bright_cyan',end_s=False)
                mode=prompt("[Choose record mode [int]>] ")
                match mode:
                    case '1':
                        try:
                            echo(style("[*] Streaming target device Microphone audio ...Press CTRL+C in xterm to stop",fg='bright_green'))
                            os.system(
                                    f"xterm -title 'Streaming Audio' -bg black -fg cyan -e 'scrcpy --no-video --audio-source=mic' &"
                                    )
                            return microphone_access_options()
                            
                        except Exception as e:
                            banner()
                            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                            return microphone_access_options()
                            
                        except KeyboardInterrupt:
                            banner()
                            echo(style("[i] Target device microphone streaming aborted successfully.",fg='red'))
                            return microphone_access_options()
                            
                    case '2':
                        try:
                            echo(style("[*] Streaming target device audio ...Press CTRL+C in xterm to stop",fg='bright_green'))
                            os.system(
                                    f"xterm -title 'Streaming Audio' -bg black -fg cyan -e 'scrcpy --no-video' &"
                                    )
                            return microphone_access_options()
                            
                        except Exception as e:
                            banner()
                            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                            return microphone_access_options()
                            
                        except KeyboardInterrupt:
                            banner()
                            echo(style("[i] Target device audio streaming aborted successfully.",fg='red'))
                            return micrcophone_access_options()
                    case other:
                        echo(style("Unrecognized record mode !",fg='red'))
                        time.sleep(0.5)
                        return microphone_access_options()

                            
            else:
                return microphone_access_options()
                
        except Exception as e:
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return microphone_access_options()
            
        except KeyboardInterrupt:
            Quit()
        

class AdvancedAccess:

    '''Class defined for some quick special operations. Used to open files or links on android device, and to mirror device screen, and others'''

    def mirror():
        try:
            if is_device_found():
                columns={
                        "Options": "gold3",
                        "Descriptions": "deep_pink1"
                        }
                rows={
                        "1. Default Mode": "Mirror device with best quality",
                        "2. Fast Mode": "For High performance purpose but low quality",
                        "3. Custom Mode": "Manually set to increase performance",
                        }
                build(columns,rows,style='bright_cyan',end_s=False)
                mode=input("[Choose mirror mode [int]>]: ")
                if mode=='1':
                    os.system(
                            f"xterm -title 'Mirror Device'  -bg black -fg cyan -e 'scrcpy' &"
                            )
                    return advanced_access_options()
                    
                elif mode=='2':
                    os.system(
                            f"xterm -title 'Mirror Device' -bg  black -fg cyan -e 'scrcpy -m 1024 -b 1M' &"
                            )
                    return advanced_access_options()
                    
                elif mode=='3':
                    size=prompt("[Enter size limit (e.g 1024)] ")
                    bitrate=prompt("[Enter bit-rate: the default is",default='Mbps')
                    frame=prompt("[Enter frame-rate (e.g 15)] ")
                    os.system(
                            f"xterm -title 'Mirror Device' -bg black -fg cyan -e 'scrcpy -m {size} -b {bitrate}M --max-fps {frame}' &"
                            )
                    return advanced_access_options()
                    
                else:
                    echo(style("[i] Unrecognized mirror mode !",blink=True,fg='red'))
                    time.sleep(0.5)
                    return advanced_access_options()
                    
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
    def open_photo():
        try:
            if is_device_found():
                echo(style("Enter path to photo on computer (No Copy Paste Please): ",fg='bright_yellow'))
                path=input("[path/to/photo]: ")
                if path=="":
                    echo(style("No photo file path specified !.",blink=True,fg='red'))
                    time.sleep(0.5)
                    return advanced_access_options()
                    
                else:
                    path=path.strip()
                    file=path.split("/")
                    file_name=file[-1]
                    if not os.path.isfile(path):
                        echo(style("The specified photo file does not exist !",blink=True,fg='red'))
                        time.sleep(0.5)
                        return advanced_access_options()
                        
                    else:
                        os.system(
                                f"adb push {path} /sdcard/{file_name} > /dev/null"
                                )
                    print(f"{Fore.GREEN}[*] Opening{Fore.RESET} {Fore.LIGHTWHITE_EX}{file_name}{Fore.RESET} {Fore.GREEN}on target device{Fore.RESET} ...")
                    os.system(
                            f'adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/{file_name}" -t image/jpeg > /dev/null'
                            )
                    return advanced_access_options()
                    
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
    def open_audio():
        try:
            if is_device_found():
                echo(style("Enter path to audio file on computer (No Copy Paste Please): ",fg='bright_yellow'))
                path=input("[path/to/audio]: ")
                if path=="":
                    echo(style("No audio file path specified !.",blink=True,fg='red'))
                    time.sleep(0.5)
                    return advanced_access_options()
                    
                else:
                    path=path.strip()
                    file=path.split("/")
                    file_name=file[-1]
                    if not os.path.isfile(path):
                        echo(style("The specified audio file does not exist !",blink=True,fg='red'))
                        time.sleep(0.5)
                        return advanced_access_options()
                        
                    else:
                        os.system(
                                f"adb push {path} /sdcard/{file_name} > /dev/null"
                                )
                    print(f"{Fore.GREEN}[*] Opening{Fore.RESET} {Fore.LIGHTWHITE_EX}{file_name}{Fore.RESET} {Fore.GREEN}on target device{Fore.RESET} ...")
                    os.system(
                            f'adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/{file_name}" -t audio/mp3 > /dev/null'
                            )
                    return advanced_access_options()
                    
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
    
    def open_video():
        try:
            if is_device_found():
                echo(style("Enter path to video file on computer (No Copy Paste Please): ",fg='bright_yellow'))
                path=input("[path/to/video]: ")
                if path=="":
                    echo(style("No video file path specified !.",blink=True,fg='red'))
                    time.sleep(0.5)
                    return advanced_access_options()
                    
                else:
                    path=path.strip()
                    file=path.split("/")
                    file_name=file[-1]
                    if not os.path.isfile(path):
                        echo(style("The specified video file does not exist !",blink=True,fg='red'))
                        return advanced_access_options()
                        
                    else:
                        os.system(
                                f"adb push {path} /sdcard/{file_name} > /dev/null"
                                )
                    print(f"{Fore.GREEN}[*] Opening{Fore.RESET} {Fore.LIGHTWHITE_EX}{file_name}{Fore.RESET} {Fore.GREEN}on target device{Fore.RESET} ...")
                    os.system(
                            f'adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/{file_name}" -t video/mp4 > /dev/null'
                            )
                    return advanced_access_options()
                    
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
    def open_link():
        try:
            if is_device_found():
                echo(style("Enter URL (e.g https://gtihub.com",fg='bright_yellow'))
                url=input("[Enter URL]: ")
                if url=="":
                    echo(style("No valid input provided !",blink=True,fg='red'))
                    time.sleep(0.5)
                    return advanced_access_options()
                    
                else:
                    print(f"{Fore.GREEN}[*] Openning{Fore.RESET} {Fore.BLUE}{url}{Fore.RESET} {Fore.GREEN}on target device ...{Fore.RESET}")
                    os.system(
                            f"adb shell am start -a android.intent.action.VIEW -d {url} > /dev/null"
                            )
                    return advanced_access_options()
                    
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RESET}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
    
    def keycodes():
        def clean():
            banner()
            return AdvancedAccess.keycodes()
        try:
            if is_device_found():
                keycodes_menu()
                key=input("[Choose keycode option [int]>] ")
                match key:
                    case '1':
                        banner()
                        text=input(f"{Fore.LIGHTWHITE_EX}[Enter text{Fore.RESET} {Fore.LIGHTYELLOW_EX}(Don't quote your text){Fore.RESET}{Fore.LIGHTWHITE_EX}] {Fore.RESET}")
                        if not text=="":
                            message=text.strip()
                            message=message.split(" ")
                            for msg in message:
                                os.system(f"adb shell input text '{msg}'")
                                os.system(f"adb shell input keyevent 62")
                                print(f"{Fore.BLUE}[*] TEXT:{Fore.RED} ['{text}']{Fore.RESET} {Fore.GREEN}Entered successfully.{Fore.RESET}")
                                return AdvancedAccess.keycodes()
                        else:
                            echo(style("No data provided !",fg='red'))
                            time.sleep(0.5)
                            return AdvancedAccess.keycodes()
                    case '2':
                        banner()
                        os.system(f"adb shell input keyevent 3")
                        echo(style("[*] Pressed HOME BUTTON", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '3':
                        banner()
                        os.system(f"adb shell input keyevent 4")
                        echo(style("[*] Pressed BACK BUTTON", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '4':
                        banner()
                        os.system(f"adb shell input keyevent 187")
                        echo(style("[*] Pressed Recent Apps BUTTON", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '5':
                        banner()
                        os.system(f"adb shell input keyevent 26")
                        echo(style("[*] Pressed Power BUTTON", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '6':
                        banner()
                        os.system(f"adb shell input keyevent 19")
                        echo(style("[*] Pressed DPAD UP", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '7':
                        banner()
                        os.system(f"adb shell input keyevent 20")
                        echo(style("[*] Pressed DPAD DOWN", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '8':
                        banner()
                        os.system(f"adb shell input keyevent 21")
                        echo(style("[*] Pressed DPAD LEFT", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '9':
                        banner()
                        os.system(f"adb shell input keyevent 22")
                        echo(style("[*] Pressed DPAD RIGHT", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '10':
                        banner()
                        os.system(f"adb shell input keyevent 67")
                        echo(style("[*] Pressed Delete/Backspace", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '11':
                        banner()
                        os.system(f"adb shell input keyevent 66")
                        echo(style("[*] Pressed Enter", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '12':
                        banner()
                        os.system(f"adb shell input keyevent 24")
                        echo(style("[*] Pressed VOLUME UP", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '13':
                        banner()
                        os.system(f"adb shell input keyevent 25")
                        echo(style("[*] Pressed VOLUME DOWN", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '14':
                        banner()
                        os.system(f"adb shell input keyevent 126")
                        echo(style("[*] Pressed Media Play", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '15':
                        banner()
                        os.system(f"adb shell input keyevent 127")
                        echo(style("[*] Pressed Media Pause", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '16':
                        banner()
                        os.system(f"adb shell input keyevent 61")
                        echo(style("[*] Pressed TAB KEY", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycodes()
                        
                    case '17':
                        banner()
                        os.system(f"adb shell input keyevent 111")
                        echo(style("[*] Pressed ESC KEY", blink=True,fg='bright_yellow'))
                        return AdvancedAccess.keycode()
                        
                    case '99':
                        banner()
                        clean()
                    case '0':
                        banner()
                        return advanced_access_options()
                    case '00':
                        Quit()
                    case other:
                        banner()
                        echo(style("[i] Invalid keycode option !",blink=True,fg='red'))
                        time.sleep(0.5)
                        return AdvancedAccess.keycodes()
                        
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
        
    
    def unlock_device():
        try:
            if is_device_found():
                password=input("[Enter passowrd or press ENTER for default>] ")
                os.system(f"adb shell input keyevent 26")
                os.system(f"adb shell input swipe 200 900 200 300 200")
                if not password=="":
                    os.system(f"adb shell input text {password}")
                    os.system(f"adb shell input keyevent 66")
                echo(style("[*] Device unlocked",fg='green'))
                return advanced_access_options()
                
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
        
    def lock_device():
        try:
            if is_device_found():
                os.system(f"adb shell input keyevent 26")
                echo(style("[*] Device Locked.",fg='green'))
                
            else:
                return advanced_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return advanced_access_options()
            
        except KeyboardInterrupt:
            Quit()
        
class TelephonyAccess:

    '''Android contacts and sms data access class.'''
    
    def dump_contacts():
        try:
            if is_device_found():
                echo(style("Enter output directory to save Contact file or press ENTER for default (No Copy Paste Please)",fg='bright_yellow'))
                output_dir=prompt("[path/to/dir] the default is: ",default='files/downloads/telephony/contacts')
                instant=datetime.datetime.now()
                file_name=f"dumped_contacts_{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.txt"
                print(f"{Fore.GREEN}[*] Extracting all contacts and saving to: {Fore.RESET}{Fore.BLUE}{os.getcwd()}/{output_dir}/{file_name}")
                os.system(
                        f"adb shell content query --uri content://contacts/phones/ --projection display_name:number > {output_dir}/{file_name}"
                        )
                return telephony_access_options()
                
            else:
                return telephony_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return telephony_access_options()
            
        except KeyboardInterrupt:
            Quit()
        
    
    def dump_calls_log():
        try:
            if is_device_found():
                echo(style("Enter output directory to save Calls Log file or press ENTER for default (No Copy Paste Please)",fg='bright_yellow'))
                output_dir=prompt("[path/to/dir] the default is: ",default='files/downloads/telephony/call_logs')
                instant=datetime.datetime.now()
                file_name=f"dumped_calls_log_{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.txt"
                print(f"{Fore.GREEN}[*] Extracting all Calls log and saving to: {Fore.RESET}{Fore.BLUE}{os.getcwd()}/{output_dir}/{file_name}")
                os.system(
                        f"adb shell content query --uri content://call_log/calls/ --projection name:number:duration:date > {output_dir}/{file_name}"
                        )
                return telephony_access_options()
                
            else:
                return telephony_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return telephony_access_options()
            
        except KeyboardInterrupt:
            Quit()
        
    def dump_sms():
        try:
            if is_device_found():
                echo(style("Enter output directory to save SMS file or press ENTER for default (No Copy Paste Please)",fg='bright_yellow'))
                output_dir=prompt("[path/to/dir] the default is: ",default='files/downloads/telephony/sms')
                instant=datetime.datetime.now()
                file_name=f"dumped_sms_{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.txt"
                print(f"{Fore.GREEN}[*] Extracting all contacts and saving to: {Fore.RESET}{Fore.BLUE}{os.getcwd()}/{output_dir}/{file_name}")
                os.system(
                        f"adb shell content query --uri content://sms/phones/ --projection address:date:body > {output_dir}/{file_name}"
                        )
                return telephony_access_options()
                
            else:
                return telephony_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return telephony_access_options()
            
        except KeyboardInterrupt:
            Quit()
        
    
    def send_sms():
        try:
            if is_device_found():
                print(f"{Fore.WHITE}[{Fore.RESET}{Fore.RED}WARRRNING{Fore.RESET}{Fore.WHITE}]{Fore.RESET} {Fore.LIGHTGREEN_EX}Feature tested on Android 12 Only.{Fore.RESET}")
                version=get_data(f"adb shell getprop ro.build.version.release")
                if int(version) > 12 :
                    print(f"{Fore.LIGHTMAGENTA_EX}[i] Target device Version:{Fore.RESET} {Fore.RED}{int(version)}{Fore.RESET} {Fore.LIGHTMAGENTA_EX}is higher to the reuqired for trying this feature.")
                    return telephony_access_options()
                    
                else:
                    echo(style(f"Enter phone number with country code (e.g +226xxxxxxxx): ",fg='bright_yellow'))
                    number=input("[number>]: ")
                    if number=="":
                        echo(style("[i] No phone number provided !",blink=True,fg='red'))
                        time.sleep(0.5)
                        return telephony_access_options()
                        
                    else:
                        try:
                            msg=input("[Enter message>]: ")
                            if not msg=="":
                                print(f"[*] Sending SMS to {Fore.GREEN}{number} ...{Fore.RESET}")
                                os.system(
                                    f"adb shell service call isms 5 i32 0 s16 'com.android.mms.service' s16 'null' s16 '{number}' s16 'null' s16 '{msg}' s16 'null' s16 'null' s16 'null' s16 'null'"
                                    )
                                echo(style("[*] Message delivered successfully.",fg='bright_green'))
                                return telephony_access_options()
                            else:
                                echo(style("No data provided !",blink=True,fg='red'))
                                time.sleep(0.5)
                                return telephony_access_options()
                            
                        except Exception as e:
                            banner()
                            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
                            return telephony_access_options()
                            
                        except KeyboardInterrupt:
                            banner()
                            echo(style("[!] SMS send aborted !.",fg='red'))
                            return telephony_access_options()
                            
            else:
                return telephony_access_options()
                
        except Exception as e:
            banner()
            print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
            return telephony_access_options()
            
        except KeyboardInterrupt:
            Quit()
        


def advanced_access_options():
    def clean():
        banner()
        return advanced_access_options()
    try:
        advanced_access_menu()
        option=input("[Choose an option [int]>]: ")
        options_list={
                "1":  AdvancedAccess.mirror,
                "2":  AdvancedAccess.open_photo,
                "3":  AdvancedAccess.open_audio,
                "4":  AdvancedAccess.open_video,
                "5":  AdvancedAccess.open_link,
                "6":  AdvancedAccess.keycodes,
                "7":  AdvancedAccess.unlock_device,
                "8":  AdvancedAccess.lock_device,
                "9":  device_access_options,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            advanced_access_options()
    except Exception as e:
        banner()
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
        return advanced_access_options()
    except KeyboardInterrupt:
        Quit()

def telephony_access_options():
    def clean():
        banner()
        return telephony_access_options()
    try:
        telephony_access_menu()
        option=input("[Choose an option [int]>]: ")
        options_list={
                "1":  TelephonyAccess.dump_contacts,
                "2":  TelephonyAccess.dump_calls_log,
                "3":  TelephonyAccess.dump_sms,
                "4":  TelephonyAccess.send_sms,
                "5":  device_access_options,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            telephony_access_options()
    except Exception as e:
        banner()
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
        return telephony_access_options()
        
    except KeyboardInterrupt:
        Quit()

def microphone_access_options():
    def clean():
        banner()
        return microphone_access_options()
    try:
        microphone_access_menu()
        option=input("[Choose an option [int]>]: ")
        options_list={
                "1":  MicrophoneAccess.record_audio,
                "2":  MicrophoneAccess.stream_audio,
                "3":  device_access_options,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            mircophone_access_options()
    except Exception as e:
        banner()
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
        return microphone_access_options()
    except KeyboardInterrupt:
            Quit()

def cam_access_options():
    def clean():
        banner()
        return cam_access_options()
    try:
        cam_access_menu()
        option=input("[Choose an option [int]>]: ")
        options_list={
                "1":  CameraAccess.screenshot,
                "2":  CameraAccess.record_screen,
                "99": clean,
                "3":  device_access_options,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            cam_access_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
    except KeyboardInterrupt:
        Quit()

def file_manager_options():
    def clean():
        banner()
        return file_manager_options()
    try:
        file_manager_menu()
        option=input("[Choose an option [int]>]: ")
        options_list={
                "1":  FileManager.download_file,
                "2":  FileManager.upload_file,
                "3":  FileManager.list_files,
                "4":  FileManager.copy_whatsapp_data,
                "5":  FileManager.copy_images,
                "99": clean,
                "6":  device_access_options,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            file_manager_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
    except KeyboardInterrupt:
        Quit()

def app_manager_options():
    def clean():
        banner()
        return app_manager_options()
    try:
        app_manager_menu()
        option=input("[Choose an option [int]>]: ")
        options_list={
                "1":  AppManager.install_app,
                "2":  AppManager.uninstall_app,
                "3":  AppManager.list_apps,
                "4":  AppManager.launch_app,
                "5":  AppManager.extract_app,
                "99": clean,
                "6":  device_access_options,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            app_manager_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
    except KeyboardInterrupt:
        Quit()

def device_access_options():
    def clean():
        banner()
        return device_access_options()
    try:
        device_access_menu()
        option=input("[Choose an option [int]>]: ")
        options_list={
                "1":  ShellAccess.get_shell,
                "2":  cam_access_options,
                "3":  microphone_access_options,
                "4":  file_manager_options,
                "5":  app_manager_options,
                "6":  advanced_access_options,
                "7":  telephony_access_options,
                "99": clean,
                "0":  back,
                "00": Quit,
                }
        options_matcher(option,options_list)
        if option !=0:
            device_access_options()
    except Exception as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {Fore.YELLOW}{e}")
    except KeyboardInterrupt:
        Quit()
