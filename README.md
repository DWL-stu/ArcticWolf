<h1 align="center">ArcticWolf🐺 -- use a computer and a frp to set up your botnet and launch ddos attacks!</h1>
<em><h3 align="center">The easy and fast way to organize a botnet for ddos and launch an attack</h3></em>
<p align="center">
<img src="https://img.shields.io/badge/Python-3.7+-green" alt="Python" />  <img src="https://img.shields.io/badge/State-developing-blue" alt="State" />
<img src="https://img.shields.io/badge/Platform-Windows-orange" alt="Platform" />
<img src="https://img.shields.io/badge/License-Apache2.0-red" alt="License" /></p>
<em><h5 align="center">virus generater, botnet controller and DDOS attacker under python3</h5></em>

## 📸Highlights
* 🛎️No server required
* 😜Very easy to use  
* 🌞Highly customized viruses
* 🌐Able to launch UDPflood, HTTPflood, ICMPflood attacks

## 📕Getting started
🥰**Requirements**  
* [pyinstaller 5.13.2](https://github.com/pyinstaller/pyinstaller)
* [upx 4.0 (for best)](https://github.com/upx/upx)
* [pywin32 306](https://github.com/mhammond/pywin32)
* [python 3.7](https://python.org)

command to install all :
```sh
pip install pyinstaller==5.13.2 pywin32==306
```
👋**Install & Start**
* Install
```sh
git clone https://github.com/DWL-stu/ArcticWolf.git
```
* Start
```sh
python main.py
```

😈**Usage**  
* Input your ip and port (ex:127.0.0.1, 1234)
* Get the public network ip and port using frp and input it (ex:1.2.3.4, 12345)
* generate .py virus (using command : gen_exe) and spread the virus with removable disk
* use ddos attack method to attack!  

🦠**virus settings**  
* set your own config at ./Data/settings.json
  * Threads_num : number of threads
  * Attribute_hide : file attribute hide
  * self_starting : Modify the registry to implement self-start
  * Password : Password to connect the botnet
  * etc.
* The log will be recorded in ./Data/History.config
     
## 🦸Maintainers
[@D0WE1L1N](https://github.com/Duweilin).

## 🤝Reports

Please send bug reports and feature requests through [github issue tracker](https://github.com/DWL-stu/ArcticWolf/issues). ArcticWolf is currently under development now and it's open to any constructive suggestions.

 
## 📃License
The ArcticWolf attack script is released under [MIT license](https://github.com/DWL-stu/ArcticWolf/License).

***⭐️Leave a star if you like this project***