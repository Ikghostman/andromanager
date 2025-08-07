
''' Tool main banner defined here '''

from modules.build_table import builder 
import os

version=open('__version__').readline()

def main_banner():
    colums= {
            'Android Device Manage Tool': 'bright_magenta',
            'Author': 'bright_blue',
            'Version': 'bright_yellow',
            }
    rows=   {
            '📱 Android Management Through ADB made Easy': 'IK GHostman -> https://github.com/Ik-Ghostman',
            }
    os.system(
            f"clear"
            )
    builder(colums,rows,style='bright_white',sr=version,end_s=True)
    
   
