import urllib.request
import sys
import os
import random
import time
import colorama
import subprocess
import ctypes
from winreg import *

def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def info():
    return colorama.Fore.CYAN+'[i] '+colorama.Fore.WHITE
def success():
    return colorama.Fore.GREEN+'[✓] '+colorama.Fore.WHITE
def err():
    return colorama.Fore.RED+'[x] '+colorama.Fore.WHITE
def warning():
    return colorama.Fore.YELLOW+'[!] '+colorama.Fore.WHITE
def proceed():
    input("\nPress enter to continue...")

def cmd(c):
    p = [i for i in c.split(' ')]
    retcode = subprocess.call(p, 
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)

def randomMac():
    a = "0123456789ABDEF"
    o = ""
    for i in range(12):
        if i == 1:
                o += "26AE"[random.randint(0, 3)] # Windows doesn't change your MAC address if the second character is else than this. For more info: https://stackoverflow.com/questions/5115649/changing-mac-address-through-registry-does-not-work
        else:
            o += a[random.randint(1, len(a)-1)]
    return o

def newMac(index):
    index = str(index)
    try:
        keyval="SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\000"+index
        if not os.path.exists("keyval"):
            CreateKey(HKEY_LOCAL_MACHINE, keyval)

        Registrykey= OpenKey(HKEY_LOCAL_MACHINE, keyval, 0, KEY_WRITE)
        print(f'{info()}Setting randomized MAC for {colorama.Fore.BLUE}NetworkAddress{colorama.Fore.WHITE}... ')
        mac = randomMac()
        SetValueEx(Registrykey,"NetworkAddress", 0, REG_SZ, mac)
        CloseKey(Registrykey)

        # Disable the network adapter
        print(f'{info()}Disabling network adapter {index}')
        cmd(f"wmic path win32_networkadapter where index={index} call disable")

        # Enable the network adapter
        print(f'{info()}Enabling network adapter {index}')
        cmd(f"wmic path win32_networkadapter where index={index} call enable")
        print(f"{success()}Successfully updated MAC address")
        print(f"{info()}New MAC: {mac}")
        return True
    
    except Exception as e:
        print("\n"+err()+f"{e}")
        proceed()
        return False
    
def main():
    os.system('wmic nic get name, index')
    i = str(input("Index: "))
    while True:
        x = connect()
        if x:
            print(f'{success()}Internet still up.')
        else:
            print(f'{info()}Disconnected! Changing to a new MAC address.')
            newMac(i)
            print(f'{info()}Cooldown 5 seconds after changing MAC address.')
            time.sleep(5)
        time.sleep(1)

if is_admin():
    main()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", '"'+sys.executable+'"', '"' + os.path.basename(__file__) + '"', None, 1)