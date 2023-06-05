import urllib.request
import sys
import os
import random
import time
import subprocess
import ctypes
from winreg import *

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    return bcolors.CYAN+'[i] '+bcolors.END
def success():
    return bcolors.GREEN+'[✓] '+bcolors.END
def err():
    return bcolors.RED+'[x] '+bcolors.END
def warning():
    return bcolors.YELLOW+'[!] '+bcolors.END
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
        print(f'{info()}Setting randomized MAC for {bcolors.BLUE}NetworkAddress{bcolors.END}... ')
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
    os.system('cls')
    choice = -1
    while choice < 1 or choice > 2:
        try:
            choice = int(input("{a}Select a mode{b}\n\n 1) Automatically change when disconnected from internet\n 2) One-time randomly change MAC address\n\nMode: ".format(a=bcolors.UNDERLINE, b=bcolors.END)))
            os.system('cls')
            break
        except:
            pass

    i = -1
    while i < 1:
        try:
            os.system('cls && wmic nic get name, index')
            i = int(input("Index: "))
            break
        except:
            os.system('cls')
    
    if choice == 1:
        os.system('cls')
        cooldown = 0
        while 1 and cooldown < 1:
            try:
                cooldown = int(input("Cooldown (seconds): "))
                break
            except:
                os.system('cls')

        disconnected = 0
        ping = 0
        try:
            while True:
                print('Pinging...')
                x = connect()
                os.system('cls')
                if x:
                    print(f'{success()}Internet still up.')
                    ping += 1
                else:
                    print(f'{info()}Disconnected! Changing to a new MAC address.')
                    newMac(i)
                    disconnected += 1
                    print(f'{info()}Cooldown 5 seconds after changing MAC address.')
                    time.sleep(5)
                print(f'Pinged: {bcolors.GREEN}{ping}{bcolors.END}\nDisconnected: {bcolors.RED}{disconnected}{bcolors.END}')
                time.sleep(cooldown)

        except Exception as e:
            print(e)
            proceed()

    elif choice == 2:
        try:
            newMac(i)
            proceed()
        except Exception as e:
            print(e)
            proceed()

if is_admin():
    try:
        main()
    except Exception as e:
        print(e)
        proceed()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", '"'+sys.executable+'"', '"' + os.path.basename(__file__) + '"', None, 1)
