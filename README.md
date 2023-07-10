# wol_server

Wake-on-LAN (WoL) server for broadcasting magic packets on a local network. For my
setup, my machines use static IP addresses, but I cannot configure the Telenet router
to remember these IP addresses. So I have this program always running on my CPU
server. When it receives a HTTP request to wake up a device, it the magic packet will
be broadcasted on the local network.

## 1. Installation

**Create Necessary Directories:**

```
mkdir -p ~/GitHub
mkdir -p ~/services
```

**Clone Repository:**

```
cd ~/GitHub
git clone git@github.com:btamm12/wol_server.git
cd wol_server
```

**Create Virtual Environment**
(note this requires anaconda)
```
make create_environment
```

**Create Executable File**

```
nano ~/services/wol_server.sh
```

Enter the following content:

```
cd /home/btamm12/GitHub/wol_server/
source /home/btamm12/anaconda3/bin/activate wol_server
make app
```

**Create Service File**

```
nano ~/services/wol_server.sh
```

Enter the following content:

```
[Unit]
Description=Wake-on-LAN Service
After=network.target
StartLimitIntervalSec=0

[Service]
Environment=PATH=/home/btamm12/anaconda3/bin/:/home/btamm12/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Type=simple
Restart=always
RestartSec=1
User=btamm12
ExecStart=bash /home/btamm12/services/wol_server.sh

[Install]
WantedBy=multi-user.target
```

**Create Symlink in System Service Directory:**

```
sudo ln -s ~/services/wol_server.service /etc/systemd/system
```

**Enable and Start Service:**

```
sudo systemctl daemon-reload
sudo systemctl enable wol_server
sudo systemctl start wol_server
```
