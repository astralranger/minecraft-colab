# -*- coding: utf-8 -*-
# %% [markdown]
"""
# Minecraft Colab - High Performance Minecraft 26.3 Server on Google Colab
# https://github.com/astralranger/minecraft-colab
"""

# %% [markdown]
"""
<a href="https://colab.research.google.com/github/astralranger/minecraft-colab/blob/main/MineColab.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

>[🔥 Starting](#scrollTo=ihPgtQu9TUs9)

>[▶ or 🛑  Console](#scrollTo=a0es2vGmTUs_)

>[⚓ Options](#scrollTo=Dc-Gb9a7TUtB)

>[📎  Log](#scrollTo=hhwFVhYMTUtB)

>[📰  Software](#scrollTo=lGqlIg5nTUtC)

>[🎈  Plugins, mods](#scrollTo=BYElubquTUtE)

>[📁 File Management](#scrollTo=zhtylbBNTUtG)


"""

# %% [markdown]
"""
----
"""

# %% [code]
# @markdown ##**[❗]  Set up** {display-mode: "form"}

# @markdown Check out [wiki of this project](https://minecolabimproved.wiki.gg/es/wiki/MineColab_Improved_Wiki) for more explanations
import requests
from requests import get
import sys
import os
from IPython.display import Javascript, display
from google.colab import output
#------------------------------------------------------------------------------------------------------------------------------------#
colabversion="0.3.5"
#------------------------------------------------------------------------------------------------------------------------------------#
# Fetching latest version info (safe non-blocking check)
url = "https://raw.githubusercontent.com/Prozoon700/MI-Test/main/version.json"
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    latest_version = data[0]['latest_version']
    print(f"Latest version available: {latest_version}")
    colabversion = latest_version
    print("Yehaa! Version up to date, you can continue using this notebook!")
except Exception as e:
    print(f"Notice: Version check skipped ({e}). Continuing...")

from time import sleep
from json import load, dump
from os.path import exists
from os import makedirs
from IPython.display import clear_output
%pip install -q jproperties
%pip install -q rich
from rich import print
%pip install -q pyngrok
%pip install -q BeautifulSoup4
%pip install -q ruamel.yaml
%pip install -q jupyter-ui-poll
if exists('/content/drive') == False:
  from google.colab import drive
  drive.mount('/content/drive')
drive_path = '/content/drive/MyDrive/minecraft'
SERVERCONFIG = f'{drive_path}/server_list.txt'
makedirs(drive_path, exist_ok=True)
makedirs(f'{drive_path}/logs', exist_ok=True)

def LOG(*args, sep=''):
  check = False
  args = list(args)
  for i in range(len(args)):
    args[i] = str(args[i])
    if '\n' in args[i]: args[i] = args[i].replace('\n', ''); args.insert(0, '\n[bold green][ LOG ][/bold green] '); check = True; break
  if check == False: args.insert(0, '[bold green][ LOG ][/bold green] ')
  print(sep.join(map(str, args)))

#---------------------------------------------------------------------------------- Print Box ------------------------------------------------------------------------------------------#
def print_msg_box(msg, indent=1, width=None, title=None):
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    border_color = "[bold gold3]"
    title_color = "[bold cyan]"
    text_color = "[bold white]"
    header_color = "[bold light_goldenrod1]"
    reset_color = "[/]"
    box = f'{border_color}+{"-" * (width + indent * 2)}+{reset_color}\n'  # upper_border
    if title:
        box += f'{border_color}|{space}{title_color}{title:<{width}}{reset_color}{space}{border_color}|\n'  # title
        box += f'{border_color}|{space}{"-" * len(title):<{width}}{space}{border_color}|\n'  # underscore
    box += ''.join([f'{border_color}|{space}{text_color}{line:<{width}}{reset_color}{space}{border_color}|\n' for line in lines])
    box += f'{border_color}+{"-" * (width + indent * 2)}+{reset_color}'  # lower_border
    print(box)

#------------------------------------------------------------------------------------------------------------------------------------#
log = "echo -e '\e[92m[ LOG ]\e[0m'" # Log function for bash
def ERROR(*args, sep=''):
  clear_output()
  check = False
  args = list(args)
  for i in range(len(args)):
    args[i] = str(args[i])
    if '\n' in args[i]: args[i] = args[i].replace('\n', ''); args.insert(0, '\n[bold red][ ERROR ][/bold red] '); check = True; break
  if check == False: args.insert(0, '[bold red][ ERROR ][/bold red] ')
  raise Exception(sep.join(map(str, args)))

def INFO(*args, sep=''):
  check = False
  args = list(args)
  for i in range(len(args)):
    args[i] = str(args[i])
    if '\n' in args[i]: args[i] = args[i].replace('\n', ''); args.insert(0, '\n[bold yellow][ INFO ][/bold yellow] '); check = True; break
  if check == False: args.insert(0, '[bold yellow][ INFO ][/bold yellow] ')
  print(sep.join(map(str, args)))

def MKDIR(path):
  from os import makedirs
  makedirs(path, exist_ok=True)

def DOWNLOAD_FILE(url, path, file_name, force = False, headers=None):
  if headers is None:
    headers = {'User-Agent': 'Mozilla/5.0'}
  if not force:
    if exists(path + '/' + file_name):
      LOG(f'File {file_name} already existed')
      return
  LOG('\nDownloading ' + file_name)
  r = GET(url, headers=headers)
  with open(path + '/' + file_name, 'wb') as f:
    f.write(r.content)

def GET(url, headers=None):
  if headers is None:
    headers = {'User-Agent': 'Mozilla/5.0'}
  r = get(url, headers=headers)
  if r.status_code == 200:
    return r
  else:
    ERROR('Error ' + str(r.status_code) + "! Could not retrieve resource from " + url)

def COLABCONFIG(server_name):
  return f"{drive_path}/{server_name}/colabconfig.txt"

def COLABCONFIG_LOAD(server_name):
  if exists(COLABCONFIG(server_name)):
    return load(open(COLABCONFIG(server_name)))
  else:
    ERROR('Please check whether you deleted your colabconfig file or not.')

def SERVER_IN_USE(server_name):
  if exists(f'{drive_path}/{server_name}') and server_name != '':
    return server_name
  else:
    serverconfig = load(open(SERVERCONFIG))
    if serverconfig.get('server_in_use', '') != '':
      return serverconfig['server_in_use']
    else:
      ERROR('Please create a minecraft server first using the Create Server cell!')

def JAR_LIST_RUN(server_version):
  return {'generic': 'server.jar', 'vanilla':'server.jar','snapshot': 'server.jar',
          'purpur' : 'server.jar', 'paper': 'server.jar', 'velocity' : 'server.jar', 'folia': 'server.jar',
          'fabric' : 'server.jar', 'arclight' : 'server.jar', 'mohist': 'server.jar', 'banner': 'server.jar'}

#------------------------------------------------------------------------------------------------------------------------------------#
LOG(f"\nColab Version: {colabversion}")
!sudo apt-get update -qq &>/dev/null && echo 'apt cache successfully updated' || echo "apt cache update note"
makedirs(drive_path, exist_ok=True)
makedirs(f'{drive_path}/logs', exist_ok=True)
if exists(SERVERCONFIG) == False:
  dump({"server_list": [], "server_in_use": "", "ngrok_proxy" : {'authtoken' : '', "region" : 'us'}, "zrok_proxy": {"authtoken": ''}, 'localtonet_proxy': {"authtoken": ''}, 'localxpose_proxy': {"authtoken": ''}, 'playit_proxy': {"secretkey": ""}}, open(SERVERCONFIG, 'w'))
%cd $drive_path
LOG('Setup Complete!')


# %% [code]
# @title 🔘 Choose server
# @markdown ####**Choosing minecraft server**
# @markdown ##### Helping to set the default server_name.
from os import listdir
from json import load, dump
from os.path import exists, isdir, join
import ipywidgets as widgets
from jupyter_ui_poll import ui_events

%cd $drive_path
LOG(f"\nColab Version: {colabversion}")
serverconfig = load(open(SERVERCONFIG))

def changeserver(server_to_use):
  global serverconfig
  if server_to_use in serverconfig.get('server_list', []):
    serverconfig['server_in_use'] = server_to_use
  else:
    serverconfig.setdefault('server_list', []).append(server_to_use)
    serverconfig['server_in_use'] = server_to_use
  dump(serverconfig, open(SERVERCONFIG, 'w'))
  LOG(f'Using server: {server_to_use}')

serverlist = [d for d in listdir(drive_path) if isdir(join(drive_path, d)) and d not in ["logs", ".ipynb_checkpoints"]]

if not serverlist:
  INFO('No servers found yet. Please proceed to the "Create Server" cell below to create your server!')
else:
  if len(serverlist) == 1:
    changeserver(serverlist[0])
  else:
    serverpicker = widgets.Dropdown(description="Server: ", options=[""]+serverlist)
    display(serverpicker)
    with ui_events() as poll:
      while serverpicker.value == '':
        poll(10)
        sleep(0.1)
    serverpicker.close()
    selserver=serverpicker.value
    changeserver(selserver)


# %% [markdown]
"""
---
"""

# %% [markdown]
"""
# 🔥 **Starting**
---

"""

# %% [code]
# @title 🛠️ Create Server { display-mode: "form" }
# @markdown #### **Configure & Create your Minecraft Server**
server_name = "minecraft_26_3" # @param {type:"string"}
server_type = "purpur" # @param ["purpur", "vanilla", "fabric", "paper"]
version = "26.3" # @param {type:"string"}
tunnel_service = "playit" # @param ["playit", "ngrok", "zrok", "argo", "localtonet"]
ngrok_token = "" # @param {type:"string"}
ngrok_region = "us" # @param ["us", "eu", "ap", "au", "sa", "jp", "in"]

from requests import get
import requests
from bs4 import BeautifulSoup
from time import sleep
from os.path import exists, join
from os import makedirs
from json import load, dump
from google.colab import output

drive_path = '/content/drive/MyDrive/minecraft'
SERVERCONFIG = f'{drive_path}/server_list.txt'

if server_name == "":
  ERROR("Please insert a name for your server.")

def SERVERSJAR(command, server_type=None, version=None):
  if command == "GetVersions":
    if server_type == None: ERROR("No server type specified.")
    if server_type == 'vanilla' or server_type == 'snapshot':
      rJSON = GET('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
      st = 'release' if server_type == 'vanilla' else 'snapshot'
      return [hit["id"] for hit in rJSON["versions"] if hit["type"] == st]
    elif server_type == 'purpur':
      rJSON = GET('https://api.purpurmc.org/v2/purpur').json()
      return [hit for hit in rJSON["versions"]]
    elif server_type == 'fabric':
      rJSON = GET('https://meta.fabricmc.net/v2/versions/game').json()
      return [hit['version'] for hit in rJSON if hit.get('stable')]
    elif server_type == 'paper':
      return ['26.3', '1.21.4', '1.20.4']
    return ['26.3']

  elif command == "GetDownloadUrl":
    if version == None: ERROR("No version specified.")
    if server_type == 'vanilla' or server_type == 'snapshot':
      rJSON = GET('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
      for hit in rJSON["versions"]:
        if hit['id'] == version:
          return GET(hit['url']).json()["downloads"]['server']['url']
      return GET(rJSON["versions"][0]['url']).json()["downloads"]['server']['url']

    elif server_type == 'purpur':
      purpur_info = GET(f'https://api.purpurmc.org/v2/purpur/{version}').json()
      build = purpur_info["builds"]["latest"]
      return f'https://api.purpurmc.org/v2/purpur/{version}/{build}/download'

    elif server_type == 'paper':
      # Paper v2 API has retired old endpoints, use Purpur (high-perf drop-in Paper fork) for 26.3
      LOG("[ INFO ] Using Purpur (high performance drop-in Paper fork) for version " + version)
      purpur_info = GET(f'https://api.purpurmc.org/v2/purpur/{version}').json()
      build = purpur_info["builds"]["latest"]
      return f'https://api.purpurmc.org/v2/purpur/{version}/{build}/download'

    elif server_type == 'fabric':
      installerVersion = GET('https://meta.fabricmc.net/v2/versions/installer').json()[0]["version"]
      fabricVersion = GET(f'https://meta.fabricmc.net/v2/versions/loader/{version}').json()[0]["loader"]["version"]
      return f"https://meta.fabricmc.net/v2/versions/loader/{version}/{fabricVersion}/{installerVersion}/server/jar"

    else:
      ERROR(f'Unsupported server type: {server_type}')

LOG(f"\nColab Version: {colabversion}")
server_folder = f'{drive_path}/{server_name}'

# Create directories
makedirs(server_folder, exist_ok=True)
makedirs(f'{drive_path}/logs', exist_ok=True)
makedirs(f'{server_folder}/tunnel', exist_ok=True)

# Pre-accept EULA immediately so the server starts cleanly without hanging
with open(f'{server_folder}/eula.txt', 'w') as f:
  f.write('eula=true\n')

LOG(f'Setting up server: {server_name}')
LOG(f'Type: {server_type} | Version: {version} | Tunnel: {tunnel_service}')

# Update serverconfig
serverconfig = load(open(SERVERCONFIG))
if server_name not in serverconfig.get('server_list', []):
  serverconfig.setdefault('server_list', []).append(server_name)
serverconfig['server_in_use'] = server_name

if tunnel_service == 'ngrok':
  if "ngrok_proxy" not in serverconfig:
    serverconfig["ngrok_proxy"] = {"authtoken": "", "region": "us"}
  if ngrok_token != "":
    serverconfig['ngrok_proxy']['authtoken'] = ngrok_token
    serverconfig['ngrok_proxy']['region'] = ngrok_region
  elif serverconfig['ngrok_proxy'].get('authtoken', '') == "":
    t = input('Enter your ngrok authtoken (or press enter if already configured): ')
    if t != "": serverconfig['ngrok_proxy']['authtoken'] = t

dump(serverconfig, open(SERVERCONFIG, 'w'))

# Save colabconfig
colabconfig = {"server_type": server_type, "server_version": version, "tunnel_service": tunnel_service}
dump(colabconfig, open(COLABCONFIG(server_name), 'w'))

# Download jar
jarname = 'server.jar'
download_url = SERVERSJAR("GetDownloadUrl", server_type, version)
LOG(f"Downloading {server_type} {version} server jar...")
DOWNLOAD_FILE(url=download_url, path=server_folder, file_name=jarname, force=True)

LOG(f'\n[ SUCCESS ] Server "{server_name}" created successfully with {server_type} {version}!')
LOG('Now scroll down to the "Console" cell and click Run to start your server!')


# %% [code]
from os.path import exists
from time import sleep
from json import load, dump
import ipywidgets as widgets
from jupyter_ui_poll import ui_events
# @title ####**Delete current server**

server_name = '' #  Get default server

serverconfig = load(open(SERVERCONFIG));
if server_name == '': server_name = serverconfig['server_in_use']
if serverconfig['server_list'] == []: ERROR("You haven't installed yet.")
else:

  # Auditing whether file is existed.
  if exists(f'{drive_path}/{server_name}') == False: ERROR("You haven't installed yet.")
  print(f'Are you sure to delete your current server ({server_name})? ([Y]Yes/[N]No) - ')
  while True: # Ask user to confirm.
    askdeletionwid = widgets.Text(value='',placeholder='[Y]Yes / [N]No',description='Delete?',disabled=False)#, layout=widgets.Layout(height='400px'))
    display(askdeletionwid)
    with ui_events() as poll:  # Wait until user chooses.
      while askdeletionwid.value == '':
        poll(10)
        sleep(0.1)
    askdeletionwid.close()
    askdeletion=askdeletionwid.value.lower()
    if askdeletion == 'y' or askdeletion == 'yes':
        LOG("Proceeding")
        break
    elif askdeletion == 'n' or askdeletion == 'no':
        ERROR("Cancelled by user.")
    else:
        print("Please use Yes or No.")

  LOG(f'Deleting {server_name}...')

  # Delete folder without noticable
  !rm -rf "{drive_path}/{server_name}" >/dev/null

  # Remove the folder name in server config txt files
  serverconfig['server_list'].remove(server_name)
  if serverconfig['server_in_use'] == server_name:
    try: serverconfig['server_in_use']= serverconfig['server_list'][0]
    except: serverconfig['server_in_use'] = ''
  dump(serverconfig, open(SERVERCONFIG, 'w'))

  LOG('Wait until deletion comes through.')
  sleep(40)
  LOG('Completed')

# %% [markdown]
"""
-----------------------------------------------------
"""

# %% [markdown]
"""
# ▶ **or** 🛑  **Console**
---
The main console for your minecraft server
"""

# %% [code]
# @title ▶️ or 🛑 Console (All-in-One Standalone) { display-mode: "form" }
# @markdown Run this single cell to start your Minecraft 26.3 server!
import os
import sys
import shutil
import threading
import re
from os import pathsep, environ, listdir, makedirs
from os.path import exists, join, expanduser
from time import sleep
from json import loads, load, dump
from IPython.display import clear_output

# 1. Mount Google Drive if not mounted
if not exists('/content/drive'):
  try:
    from google.colab import drive
    drive.mount('/content/drive')
  except Exception as e:
    pass

drive_path = '/content/drive/MyDrive/minecraft'
SERVERCONFIG = f'{drive_path}/server_list.txt'
colabversion = "0.3.5"
makedirs(drive_path, exist_ok=True)
makedirs(f'{drive_path}/logs', exist_ok=True)

def LOG(*args, sep=''):
  print('[ LOG ] ' + sep.join(map(str, args)))

def print_msg_box(msg, indent=1, width=None, title=None):
  lines = msg.split('\n')
  if not width: width = max(map(len, lines)) + 4
  border = '+' + '-' * (width + indent * 2) + '+'
  print(border)
  if title:
    print(f'| {" " * indent}{title:<{width}}{" " * indent}|')
    print(f'| {" " * indent}{"-" * len(title):<{width}}{" " * indent}|')
  for line in lines:
    print(f'| {" " * indent}{line:<{width}}{" " * indent}|')
  print(border)

# Get Server Name
server_name = 'minecraft_26_3'
if exists(SERVERCONFIG):
  try:
    s_cfg = load(open(SERVERCONFIG))
    if s_cfg.get('server_in_use'):
      server_name = s_cfg['server_in_use']
  except Exception:
    pass

tunnel_service = 'playit'
version = '26.3'
_type = 'purpur'

def CONFIG_PLAYIT():
  !pkill -9 playit >/dev/null 2>&1 || true
  !pkill -9 playitd >/dev/null 2>&1 || true
  !rm -f /run/playit/playitd.sock /tmp/playit.sock >/dev/null 2>&1 || true

  LOG("Ensuring stable Playit v0.15.26 is installed...")
  !sudo curl -SsL -o /usr/local/bin/playit https://github.com/playit-cloud/playit-agent/releases/download/v0.15.26/playit-linux-amd64 && sudo chmod +x /usr/local/bin/playit

  makedirs('/etc/playit', exist_ok=True)
  
  drive_playit_conf = f'{drive_path}/playit.toml'
  if exists(drive_playit_conf) and not exists('/etc/playit/playit.toml'):
    !cp '{drive_playit_conf}' /etc/playit/playit.toml

  LOG("Starting Playit tunnel daemon...")
  !playit start &> /content/drive/MyDrive/minecraft/logs/playit.txt &
  sleep(4)

  log_file = '/content/drive/MyDrive/minecraft/logs/playit.txt'
  claim_url = None
  tunnel_ip = None
  for _ in range(6):
    if exists(log_file):
      try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as pf:
          content = pf.read()
          for line in content.splitlines():
            if 'playit.gg/claim/' in line:
              match = re.search(r'https://playit\.gg/claim/[a-zA-Z0-9]+', line)
              if match: claim_url = match.group(0)
            if any(ext in line for ext in ['.gl.joinmc.link', '.playit.gg', '.tun.ply.gg']):
              tunnel_ip = line.strip()
      except Exception:
        pass
    if claim_url or tunnel_ip:
      break
    sleep(1)

  if claim_url:
    print_msg_box(f"\nClaim Link: {claim_url}\nOpen this link in your browser to activate your tunnel!", indent=2, width=70, title="PLAYIT CLAIM LINK")
  elif tunnel_ip:
    print_msg_box(f"\n{tunnel_ip}\n", indent=2, width=70, title="SERVER CONNECTION ADDRESS")

  if exists('/etc/playit/playit.toml'):
    !cp /etc/playit/playit.toml '{drive_playit_conf}' >/dev/null 2>&1 || true

def INSTALL_JAVA():
  j_check = !java -version 2>&1 | grep -E 'version "(25\.|26\.)'
  if len(j_check) > 0 and ("25." in j_check[0] or "26." in j_check[0]):
    LOG("Java 25 is active.")
    return

  LOG("Setting up Java 25...")
  !sudo apt-get update -qq >/dev/null 2>&1
  !sudo apt-get install -y openjdk-25-jre-headless openjdk-25-jdk >/dev/null 2>&1
  j_check = !java -version 2>&1 | grep -E 'version "(25\.|26\.)'
  if len(j_check) > 0 and ("25." in j_check[0] or "26." in j_check[0]):
    environ["JAVA_HOME"] = "/usr/lib/jvm/java-25-openjdk-amd64"
    return

  LOG("Installing Eclipse Temurin Java 25 directly...")
  !sudo mkdir -p /opt/java25
  !curl -sSL "https://api.adoptium.net/v3/binary/latest/25/ga/linux/x64/jdk/hotspot/normal/eclipse" | sudo tar -xzf - -C /opt/java25 --strip-components=1
  !sudo update-alternatives --install /usr/bin/java java /opt/java25/bin/java 2000
  !sudo update-alternatives --set java /opt/java25/bin/java
  environ["JAVA_HOME"] = "/opt/java25"
  environ["PATH"] = f"/opt/java25/bin:{environ.get('PATH', '')}"

def CONFIGURE_SERVER(run_dir):
  with open(f'{run_dir}/eula.txt', 'w') as f:
    f.write('eula=true\n')

  props_path = f'{run_dir}/server.properties'
  existing_lines = []
  if exists(props_path):
    try:
      with open(props_path, 'r', encoding='utf-8') as pf:
        existing_lines = pf.readlines()
    except Exception:
      pass

  filtered = [l for l in existing_lines if not any(l.strip().startswith(k) for k in ['online-mode=', 'white-list=', 'enforce-whitelist='])]
  filtered.append('online-mode=false\n')
  filtered.append('white-list=false\n')
  filtered.append('enforce-whitelist=false\n')

  with open(props_path, 'w', encoding='utf-8') as pf:
    pf.writelines(filtered)

  try:
    ops_file = f'{run_dir}/ops.json'
    ops_data = []
    if exists(ops_file):
      try: ops_data = load(open(ops_file))
      except: ops_data = []
    if not any(o.get('name', '').lower() == 'skywalker' for o in ops_data):
      ops_data.append({
        "uuid": "a9b16b8b-18fe-3cac-a53d-cb40e802fe61",
        "name": "skywalker",
        "level": 4,
        "bypassesPlayerLimit": False
      })
      with open(ops_file, 'w', encoding='utf-8') as of:
        dump(ops_data, of, indent=2)
  except Exception:
    pass

  try:
    with open(f'{run_dir}/whitelist.json', 'w', encoding='utf-8') as wf:
      dump([{"uuid": "a9b16b8b-18fe-3cac-a53d-cb40e802fe61", "name": "skywalker"}], wf, indent=2)
  except Exception:
    pass

  LOG("✅ Configured: online-mode=false (TLauncher support), white-list=false (open to all), Admin=skywalker")

def auto_save_sync(local_p, drive_p, stop_ev):
  while not stop_ev.is_set():
    stop_ev.wait(300)
    if stop_ev.is_set(): break
    try:
      if exists(f"{local_p}/world"):
        !rsync -a '{local_p}/world/' '{drive_p}/world/' >/dev/null 2>&1
        !rsync -a '{local_p}/world_nether/' '{drive_p}/world_nether/' >/dev/null 2>&1
        !rsync -a '{local_p}/world_the_end/' '{drive_p}/world_the_end/' >/dev/null 2>&1
    except Exception: pass

# ----------------- MAIN RUN -----------------
drive_server_path = f'{drive_path}/{server_name}'
local_server_path = f'/content/{server_name}'
makedirs(local_server_path, exist_ok=True)
makedirs(drive_server_path, exist_ok=True)

if not exists(f'{local_server_path}/server.jar'):
  if exists(f'{drive_server_path}/server.jar'):
    LOG("Copying server.jar from Google Drive...")
    !cp '{drive_server_path}/server.jar' '{local_server_path}/server.jar'
  else:
    LOG("Downloading Purpur 26.3 server jar...")
    !curl -sSL -o '{local_server_path}/server.jar' "https://api.purpurmc.org/v2/purpur/26.3/2641/download"
    !cp '{local_server_path}/server.jar' '{drive_server_path}/server.jar'

if exists(drive_server_path) and listdir(drive_server_path):
  LOG("⚡ Syncing server files from Google Drive to Local Fast NVMe Storage...")
  !rsync -a '{drive_server_path}/' '{local_server_path}/'

%cd $local_server_path

CONFIGURE_SERVER(local_server_path)
INSTALL_JAVA()
CONFIG_PLAYIT()

sync_stop = threading.Event()
sync_t = threading.Thread(target=auto_save_sync, args=(local_server_path, drive_server_path, sync_stop), daemon=True)
sync_t.start()

args = " -Xms4G -Xmx8G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true"
cmd = f'java -server {args} -jar server.jar nogui'

try:
  LOG("🚀 Starting Minecraft 26.3 Server on Fast Local Storage:")
  ! $cmd
finally:
  sync_stop.set()
  LOG("\n💾 Saving all world and server data back to Google Drive...")
  !rsync -a --delete '{local_server_path}/' '{drive_server_path}/'
  LOG("✅ Saved successfully to Google Drive! Server stopped.")


# %% [markdown]
"""
---
"""

# %% [markdown]
"""
# ⚓ **Options** (Java Only!)
---

"""

# %% [code]
from jproperties import Properties
from os.path import exists
from google.colab import files as fls
!pip install -q pillow
from PIL import Image

# @markdown ####**Server_custom**
choice = 'server_motd' # @param ["server_motd", "server_icon"]

server_name = SERVER_IN_USE(server_name = '')
file_path = f'{drive_path}/server-icon.png'
file_dest = f'{drive_path}/{server_name}/'

if exists(f"{drive_path}/{server_name}/server.properties") == False:
  ERROR('Running your minecraft server before editing properties')
else:
  LOG('Server: ' + server_name)
  if choice == 'server_icon':
    if exists(f"{drive_path}/{server_name}/server-icon.png"):
      LOG('Existing server-icon.png found.')
    url = input('Download_url (leave empty to upload manually): ')
    if url != '':
      try:
        DOWNLOAD_FILE(url=url, path=f'{drive_path}', file_name='server-icon.png')
        img = Image.open(f'{drive_path}/server-icon.png')
        img = img.resize((64, 64))
        img.save(f'{drive_path}/{server_name}/server-icon.png')
        LOG('Icon updated!')
      except Exception as e:
        ERROR('Failed to download icon: ' + str(e))
  elif choice == 'server_motd':
    motd = input('Enter your server MOTD: ')
    server_properties = Properties()
    with open(f"{drive_path}/{server_name}/server.properties", "rb") as f:
      server_properties.load(f, "utf-8")
    server_properties["motd"] = motd
    with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
      server_properties.store(f, encoding="utf-8")
    LOG("MOTD updated to: " + motd)


# %% [code]
from jproperties import Properties
from os.path import exists

# @markdown ####**Server properties**
Slots = 25 # @param {type:"slider", min:0, max:100, step:1}
Gamemode = "survival" # @param ["survival", "creative", "adventure", "spectator"]
Difficulty = "normal" # @param ["peaceful", "easy", "normal", "hard"]
Cracked = True # @param {type:"boolean"}
PVP = True # @param {type:"boolean"}
Command_block = True # @param {type:"boolean"}
Fly = True # @param {type:"boolean"}
Animals = True # @param {type:"boolean"}
Monsters = True # @param {type:"boolean"}
Villagers = True # @param {type:"boolean"}
Nether = True # @param {type:"boolean"}
Force_gamemode = False # @param {type:"boolean"}
Spawn_protection = 16 # @param {type:"slider", min:0, max:100, step:1}

#---------------------------------------------------------------------------------- MAIN CODE ------------------------------------------------------------------------------------#

server_name = SERVER_IN_USE(server_name = '')
if exists(f"{drive_path}/{server_name}/server.properties") == False: ERROR(' Running your minecraft server before editing properties')
else:
  LOG('Changing server.properties')
  server_properties = Properties() # Download file
  with open(f"{drive_path}/{server_name}/server.properties", "rb") as f:
      server_properties.load(f, "utf-8")
  # Configuring
  server_properties["max-players"] = str(Slots)
  server_properties["gamemode"] = Gamemode
  server_properties["difficulty"] = Difficulty
  dict_ = {'pvp': PVP, 'enable-command-block': Command_block, 'allow-flight': Fly, 'spawn-animals': Animals, 'spawn-monsters': Monsters,
          'spawn-npcs': Villagers, 'allow-nether': Nether, 'force-gamemode': Force_gamemode, 'spawn-protection': Spawn_protection, "online-mode" : not Cracked}
  for keys, value in dict_.items(): server_properties[keys] = str(value).lower()
  # Saving
  with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
      server_properties.store(f, encoding="utf-8")
  LOG('Completed')

# %% [markdown]
"""
---
"""

# %% [markdown]
"""
# 📎  **Log** (Java Only!)
---

"""

# %% [code]
from os.path import exists
from rich.console import Console

# @markdown ####**Shows latest log of your minecraft server**
LOG(f"\nColab Version: {colabversion}")
server_name = SERVER_IN_USE(server_name = '')
log_path = f'{drive_path}/{server_name}/logs/latest.log'
console = Console()
if exists(log_path):
  try:
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
      print(f.read())
  except Exception as e:
    ERROR("Could not read log file: " + str(e))
else:
  INFO("Log file not found yet. Has the server run at least once?")


# %% [markdown]
"""
---

"""

# %% [markdown]
"""
# 📰  **Software**
---

Change server software, tunnel and others.

---

+ Please checking whether your minecraft server is in Gdrive or not.
"""

# %% [code]

from json import load, dump
from requests import get
from bs4 import BeautifulSoup
from os.path import exists
from time import sleep
import ipywidgets as widgets
from jupyter_ui_poll import ui_events
# @title Change Server Software
# @markdown #### **Change server software**
# @markdown This cell will help you change the type of server you're running. Keep in mind this will delete your current server.

serverconfig = load(open(SERVERCONFIG)); server_name = serverconfig['server_in_use']; colabconfig = load(open(COLABCONFIG(server_name)))

# GUIDANCE
choice = input('Do you want to show(s)/hide(h) tunnels info? - ')
if 's' in choice: clear_output(); print("\n\n- **[Ngrok](https://ngrok.com)**\n  + Follow the prompts.\n  + The IP will change whenever you restart the server.\n\n- **[Cloudflare's argo](https://www.cloudflare.com/)** :\n    - If the 'Your free tunnel has started!' notification appears => Done.\n    - Access to your server:\n    1. Download [Cloudflared client](https://github.com/cloudflare/cloudflared/releases/).\n    2. Launch the binary with `<your Cloudflare file name> access tcp --hostname <tunnel_address> --url 127.0.0.1:25565` (note: tunnel_address is your address which has been set on your Cloudflare).\n    4. Finally, connect to `127.0.0.1:25565` from the minecraft client which is located in that machine.\n\n- **[Localtonet](https://localtonet.com/)**:\n  1. Navigate to [TCP-UDG](https://localtonet.com/tunnel/tcpudp) page. Select TCP in Protocol Types.\n  2. Get your authtoken from [Authtoken](https://localtonet.com/usertoken).\n  3. Pick the server you'd like your tunnel to operate on.\n  4. Input the IP and Port values the tunnel will listen to, in this case, for Minecraft, it's typically IP: 127.0.0.1 and Port: 25565.\n  5. Finally, create and start your tunnel by pressing the Start button.\n  - Read more on [how-to-use-localtonet-with-minecraft](https://localtonet.com/documents/using-localtonet-with-minecraft)\n\n- **[Zrok](https://zrok.io/)**:\n  1. Download the zrok app through [link](https://docs.zrok.io/docs/getting-started/)\n  2. Open the shell. Type `zrok invite` to sign up and get the authtoken\n  3. Follow the prompts\n  4. Acess to https://api.zrok.io to get fully management\n   - Read more on https://docs.zrok.io/docs/getting-started. \n\n- **[PlayIt](https://playit.gg/)**: follow the prompts."); sleep(20)
clear_output()

#---------------------------------------------------------------------------------- DELETE SERVER ------------------------------------------------------------------------------------#

if serverconfig['server_list'] == []: ERROR("You haven't installed any server yet. Please create one.")
else:
  LOG(f"\nColab Version: {colabversion}")
  # Auditing whether file is existed.
  if exists(f'{drive_path}/{server_name}') == False: ERROR("Server not found. Please create one")
  print(f'Are you sure to delete your current server ({server_name})? ([Y]Yes/[N]No) - ')
  while True: # Ask user to confirm.
    askdeletionwid = widgets.Text(value='',placeholder='[Y]Yes / [N]No',description='Delete?',disabled=False)#, layout=widgets.Layout(height='400px'))
    display(askdeletionwid)
    with ui_events() as poll:  # Wait until user chooses.
      while askdeletionwid.value == '':
        poll(10)
        sleep(0.1)
    askdeletionwid.close()
    askdeletion=askdeletionwid.value.lower()
    if askdeletion == 'y' or askdeletion == 'yes':
        LOG("Proceeding")
        break
    elif askdeletion == 'n' or askdeletion == 'no':
        ERROR("Cancelled by user.")
    else:
        print("Please use Yes or No.")
  LOG(f'Deleting {server_name}...')

  # Delete folder without noticable
  !rm -rf "{drive_path}/{server_name}"

  # Remove the folder name in server config txt files
  serverconfig['server_list'].remove(server_name)
  if serverconfig['server_in_use'] == server_name:
    try: serverconfig['server_in_use']= serverconfig['server_list'][0]
    except: serverconfig['server_in_use'] = ''
  dump(serverconfig, open(SERVERCONFIG, 'w'))

  LOG('Wait until deletion comes through'); sleep(40); LOG('Completed')

#---------------------------------------------------------------------------------- SLEEPING ------------------------------------------------------------------------------------#

LOG("Please wait.") ; sleep(10)

#---------------------------------------------------------------------------------- INSTALL SERVER ------------------------------------------------------------------------------------#
def SERVERSJAR(command, server_type=None, version=None):
  #Get the download URL (jar) AND return the detailed versions for each software (all)
  if command == "GetVersions":
    if server_type == None: ERROR("No server type specified.")
    Server_Jars_All = {
      'paper': 'https://api.papermc.io/v2/projects/paper', 'velocity': 'https://api.papermc.io/v2/projects/velocity',
      'purpur': 'https://api.purpurmc.org/v2/purpur',
      'mohist': 'https://mohistmc.com/api/v2/projects/mohist', 'banner': 'https://mohistmc.com/api/v2/projects/banner',
      'folia': 'https://api.papermc.io/v2/projects/folia'
    }
    if server_type == 'vanilla' or server_type=='snapshot':
      rJSON = GET('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
      if server_type == 'vanilla': server_type = 'release'
      if version != 'vanilla - latest_version': server_version = [hit["id"] for hit in rJSON["versions"] if hit["type"] == server_type]
      else:
        return rJSON['latest']['release']

    elif server_type == 'paper' or  server_type == 'velocity' or server_type == 'purpur' or server_type == 'mohist' or server_type == 'banner' or server_type == 'folia':
      rJSON = GET(Server_Jars_All[server_type]).json()
      server_version = [hit for hit in rJSON["versions"]]

    elif server_type == 'fabric':
      rJSON = GET('https://meta.fabricmc.net/v2/versions/game').json()
      server_version = [hit['version'] for hit in rJSON if hit['stable'] == True]

    elif server_type == 'forge':
      from bs4 import BeautifulSoup
      rJSON = GET('https://files.minecraftforge.net/net/minecraftforge/forge/index.html')
      soup = BeautifulSoup(rJSON.content, "html.parser")
      server_version = [tag.text for tag in soup.find_all('a') if '.' in tag.text and '\n' not in tag.text]
    elif server_type == "bedrock":
      import requests
      from bs4 import BeautifulSoup

      URL = "https://www.minecraft.net/en-us/download/server/bedrock/"
      BACKUP_URL = "https://raw.githubusercontent.com/ghwns9652/Minecraft-Bedrock-Server-Updater/main/backup_download_link.txt"
      HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

      try:
          page = requests.get(URL, headers=HEADERS, timeout=5)

          soup = BeautifulSoup(page.content, "html.parser")

          a_tag_res = []
          for a_tags in soup.findAll('a', attrs={"aria-label":"Download Minecraft Dedicated Server software for Ubuntu (Linux)"}):
            a_tag_res.append(a_tags['href'])

          download_link=a_tag_res[0]

      except requests.exceptions.Timeout:
          LOG("timeout raised, recovering")
          page = requests.get(BACKUP_URL, headers=HEADERS, timeout=5)

          download_link=page.text
      server_version = download_link.split('bedrock-server-')[1].split(".zip")[0]
    elif server_type == "arclight":
      LOG('Before going deeper, please check out https://github.com/IzzelAliz/Arclight')
      rJSON = GET('https://files.hypoglycemia.icu/v1/files/arclight/minecraft').json()['files']
      server_version  = [hit['name'] for hit in rJSON]
    return server_version

  elif command == "GetDownloadUrl":
    if version == None: ERROR("No version specified.")
    # RETURN DOWNLOAD URL
    if server_type == 'vanilla' or server_type=='snapshot':
      rJSON = GET('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
      if server_type == 'vanilla': server_type = 'release'
      for hit in rJSON["versions"]:
        if hit["type"] == server_type and hit['id'] == version:
          return GET(hit['url']).json()["downloads"]['server']['url']

    elif server_type == 'paper' or  server_type == 'velocity' or server_type == 'folia':
      build = GET(f'https://api.papermc.io/v2/projects/{server_type}/versions/{version}').json()["builds"][-1]
      jar_name = GET(f'https://api.papermc.io/v2/projects/{server_type}/versions/{version}/builds/{build}').json()["downloads"]["application"]["name"]
      return f'https://api.papermc.io/v2/projects/{server_type}/versions/{version}/builds/{build}/downloads/{jar_name}'

    elif server_type == 'purpur':
      build = GET(f'https://api.purpurmc.org/v2/purpur/{version}').json()["builds"]["latest"]
      return f'https://api.purpurmc.org/v2/purpur/{version}/{build}/download'

    elif server_type == 'mohist' or server_type == 'banner':
      return GET(f'https://mohistmc.com/api/v2/projects/{server_type}/{version}/builds').json()["builds"][-1]["url"]

    elif server_type == 'fabric':
      installerVersion = GET('https://meta.fabricmc.net/v2/versions/installer').json()[0]["version"]
      fabricVersion = GET(f'https://meta.fabricmc.net/v2/versions/loader/{version}').json()[0]["loader"]["version"]
      return "https://meta.fabricmc.net/v2/versions/loader/" + version + "/" + fabricVersion + "/" + installerVersion + "/server/jar"

    elif server_type == 'forge':
      from bs4 import BeautifulSoup
      rJSON = GET(f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html')
      soup = BeautifulSoup(rJSON.content, "html.parser")
      tag =  soup.find('a', title="Installer"); tag = str(tag); tag = tag[tag.find('"') + 1 :]
      link = tag[:tag.find('"')]; link = link[link.find('=') + 1:]; link = link[link.find('=') + 1:]
      return link

    elif server_type == 'arclight':
      rJSON = GET(f'https://files.hypoglycemia.icu/v1/files/arclight/minecraft/{version}/loaders').json()
      LOG('Available type: '); print([hit['name'] for hit in rJSON['files']])
      build = input(' Type: '); choice = input('Stable(st) or Snapshot(sn): ')
      if 'sn' in choice.lower(): choice = 'latest-snapshot';
      else: choice = "latest-stable";
      return f'https://files.hypoglycemia.icu/v1/files/arclight/minecraft/{version}/loaders/{build}/{choice}'

    elif server_type == 'bedrock':
      LOG('Selecting latest version available...')
      import requests
      from bs4 import BeautifulSoup

      URL = "https://www.minecraft.net/en-us/download/server/bedrock/"
      BACKUP_URL = "https://raw.githubusercontent.com/ghwns9652/Minecraft-Bedrock-Server-Updater/main/backup_download_link.txt"
      HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

      try:
          page = requests.get(URL, headers=HEADERS, timeout=5)

          soup = BeautifulSoup(page.content, "html.parser")

          a_tag_res = []
          for a_tags in soup.findAll('a', attrs={"aria-label":"Download Minecraft Dedicated Server software for Ubuntu (Linux)"}):
            a_tag_res.append(a_tags['href'])

          download_link=a_tag_res[0]

      except requests.exceptions.Timeout:
          LOG("timeout raised, recovering")
          page = requests.get(BACKUP_URL, headers=HEADERS, timeout=5)

          download_link=page.text

      return download_link
    else: ERROR('Wrong server type.')
  elif command == "GetServerTypes": return ['vanilla','snapshot','paper','purpur','mohist', "arclight",'velocity', 'banner', 'fabric',"folia", 'forge', 'bedrock']
  else: ERROR("Not a valid command.")

#---------------------------------------------------------------------------------- MAIN CODE ------------------------------------------------------------------------------------#
# Auditing whether file is existed.
if exists(f'{drive_path}/{server_name}'): ERROR('Bad server deletion. Please try again.')
  # Create folder
MKDIR(f'{drive_path}/{server_name}')
LOG('Checking if folder created. Please wait.')
sleep(40)
LOG("Select your server type:")
stdrop = widgets.Dropdown(description="Server Type:", options=[""]+SERVERSJAR("GetServerTypes")) # Ask for server type
display(stdrop)
with ui_events() as poll:
    while stdrop.value == '':
        poll(10)          # React to UI events (upto 10 at a time)
        sleep(0.1)
stdrop.close()
server_type=stdrop.value                                                                        # End asking
LOG(f'Choosen server type: {server_type}')
if server_type != "bedrock": # Check if server type isn't bedrock.
  LOG("Select your server version:")
  svdrop = widgets.Dropdown(description="Server version: ", style={'description_width': 'initial'}, options=['']+SERVERSJAR("GetVersions", server_type=server_type)) # Ask for server version
  display(svdrop)
  with ui_events() as poll:  # Wait until user chooses.
    while svdrop.value == '':
      poll(10)
      sleep(0.1)
  svdrop.close()
  version=svdrop.value                                                                                                                                               # End asking
  LOG(f'\nChoosen server version: {version}')
else:
  version=SERVERSJAR("GetVersions", server_type=server_type)

  LOG("Using latest bedrock version")
LOG("Select a Tunnel provider:")
tunnelsrvs = widgets.Dropdown(description="Tunnel Service: ", style={'description_width': 'initial'}, options=['','ngrok', 'argo', 'zrok', 'playit', 'localtonet', 'localxpose', 'tailscale', "minekube-gate"]) # Ask for server version
display(tunnelsrvs)
with ui_events() as poll:  # Wait until user chooses.
    while tunnelsrvs.value == '':
        poll(10)
        sleep(0.1)
tunnelsrvs.close()
tunnel_service=tunnelsrvs.value                                                                                                                                                                # End asking
LOG(f'Choosen Tunnel service: {tunnel_service}')
serverconfig = load(open(SERVERCONFIG))
serverconfig['server_list'] += [server_name]
serverconfig['server_in_use'] = server_name
if tunnel_service == 'ngrok':
  LOG("Tunnel Settings:")
  LOG('Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken')
  token = input('Your authtoken: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig['ngrok_proxy']['authtoken'] = token
  LOG('Available Regions:', ' ap - Asia/Pacific (Singapore)', ' au - Australia (Sydney)', ' eu - Europa (Frankfurt - Germany)', ' in - India (Mumbai)', ' jp - Japan (Tokyo)', ' sa - America (São Paulo - Brazil)', ' us - United States (Ohio)', sep='\n')
  serverconfig['ngrok_proxy']['region'] = input('Region: ')
elif tunnel_service == 'zrok':
  # Settings variable
  LOG("Tunnel Settings:")
  if "zrok_proxy" not in serverconfig:
    serverconfig["zrok_proxy"] = {"authtoken": ""}
  token = input('Your zrok token: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig['zrok_proxy']['authtoken'] = token
elif tunnel_service == 'localtonet':
  LOG("Tunnel Settings:")
  LOG('Get your authtoken from https://localtonet.com/usertoken')
  if "localtonet_proxy" not in serverconfig:
    serverconfig["localtonet_proxy"] = {"authtoken": ""}
  token = input('Your localtonet token: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig['localtonet_proxy']['authtoken'] = token
elif tunnel_service == 'localxpose':
  LOG("Tunnel Settings:")
  LOG('Get your authtoken from https://localxpose.io/dashboard/access')
  if "localxpose_proxy" not in serverconfig:
    serverconfig["localxpose_proxy"] = {"authtoken": ""}
  token = input('Your localxpose token: ')
  if token == "":
    ERROR("\nNo token provided.")
  serverconfig['localxpose_proxy']['authtoken'] = token
elif tunnel_service == 'tailscale':
  LOG("Tunnel Settings:")
  LOG('Get your authtoken from https://login.tailscale.com/admin/settings/keys . Make sure to select reusable')
  if "tailscale_proxy" not in serverconfig:
    serverconfig["tailscale_proxy"] = {"authtoken": ""}
  if "machine_info" not in serverconfig["tailscale_proxy"]:
    serverconfig["tailscale_proxy"]["machine_info"] = ""
  sleep(10)
  token = input('Your tailscale token: ')
  if token == "":
    ERROR("\nNo token provided.")
  serverconfig['tailscale_proxy']['authtoken'] = token
elif tunnel_service == 'minekube-gate':
  LOG('Get your token from https://app.minekube.com/orgs')
  if "minekube-gate_proxy" not in serverconfig:
    serverconfig["minekube-gate_proxy"] = {"token": ""}
  token = input('Your minekube token: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig["minekube-gate_proxy"]['token'] = token
dump(serverconfig, open(SERVERCONFIG, 'w'))
# Set up colabconfig
colabconfig = {"server_type": server_type, "server_version": version, "tunnel_service" : tunnel_service}
dump(colabconfig, open(COLABCONFIG(server_name),'w'))
# Download jar file
if server_type == "bedrock":
  DOWNLOAD_FILE(url = SERVERSJAR("GetDownloadUrl", server_type, version), path = f"{drive_path}/{server_name}", file_name='bedrock-server.zip', force=True, headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; BEDROCK-UPDATER)"})
  LOG("Unzipping bedrock server zip.")
  ! unzip {drive_path}/{server_name}/bedrock-server.zip -d {drive_path}/{server_name} >/dev/null && $log "Successfully unzipped" || echo "unzip error."
  LOG("Unzipped successfully")
  sleep(10)
  LOG('\nCompleted!')
else:
  if server_type == 'forge': jarname = 'forge-installer.jar' # The jar file name (forge need a special process)
  else: jarname = JAR_LIST_RUN(version)[server_type]
  DOWNLOAD_FILE(url= SERVERSJAR("GetDownloadUrl", server_type, version), path = f"{drive_path}/{server_name}", file_name= jarname, force=True)
  sleep(40)
  LOG('\nCompleted!')

# %% [markdown]
"""
## **🌐 Tunneling options**
---

"""

# %% [code]
# @title Change Tunnel Service
from json import load, dump
from requests import get
from bs4 import BeautifulSoup
from os.path import exists
from time import sleep

# @markdown #### **Tunnel Service** (Available tunnels: [ngrok](https://ngrok.com/), [cloudfare-argo](https://www.cloudflare.com/), [zrok.io](https://zrok.io/),  [playit.gg](https://playit.gg/), [localtonet](https://localtonet.com), [tailscale](https://tailscale.com/) and [Minekube-Gate](https://gate.minekube.com/) + playit)
tunnel_service = "minekube-gate" # @param ["Leave as it is", "argo", "zrok", "playit", "localtonet", "localxpose", "ngrok", "tailscale", "minekube-gate"]

serverconfig = load(open(SERVERCONFIG));
server_name = serverconfig['server_in_use']
colabconfig = load(open(COLABCONFIG(server_name)))

# GUIDANCE
choice = input('Do you want to show(s)/hide(h) tunnels info? - ')
if 's' in choice: clear_output(); print("\n\n- **[Ngrok](https://ngrok.com)**\n  + Follow the prompts.\n  + The IP will change whenever you restart the server.\n\n- **[Cloudflare's argo](https://www.cloudflare.com/)** :\n    - If the 'Your free tunnel has started!' notification appears => Done.\n    - Access to your server:\n    1. Download [Cloudflared client](https://github.com/cloudflare/cloudflared/releases/).\n    2. Launch the binary with `<your Cloudflare file name> access tcp --hostname <tunnel_address> --url 127.0.0.1:25565` (note: tunnel_address is your address which has been set on your Cloudflare).\n    4. Finally, connect to `127.0.0.1:25565` from the minecraft client which is located in that machine.\n\n- **[Localtonet](https://localtonet.com/)**:\n  1. Navigate to [TCP-UDG](https://localtonet.com/tunnel/tcpudp) page. Select TCP in Protocol Types.\n  2. Get your authtoken from [Authtoken](https://localtonet.com/usertoken).\n  3. Pick the server you'd like your tunnel to operate on.\n  4. Input the IP and Port values the tunnel will listen to, in this case, for Minecraft, it's typically IP: 127.0.0.1 and Port: 25565.\n  5. Finally, create and start your tunnel by pressing the Start button.\n  - Read more on [how-to-use-localtonet-with-minecraft](https://localtonet.com/documents/using-localtonet-with-minecraft)\n\n- **[Zrok](https://zrok.io/)**:\n  1. Download the zrok app through [link](https://docs.zrok.io/docs/getting-started/)\n  2. Open the shell. Type `zrok invite` to sign up and get the authtoken\n  3. Follow the prompts\n  4. Acess to https://api.zrok.io to get fully management\n   - Read more on https://docs.zrok.io/docs/getting-started. \n\n- **[PlayIt](https://playit.gg/)**: follow the prompts."); sleep(20)
clear_output()

#---------------------------------------------------------------------------------- MAIN CODE ------------------------------------------------------------------------------------#
LOG(f"\nColab Version: {colabversion}")
if tunnel_service == 'Leave as it is':
  tunnel_service = colabconfig['tunnel_service']
  LOG("\nDONE. No changes made.")
else:

  # Load serverconfig
  serverconfig = load(open(SERVERCONFIG))
  serverconfig['server_in_use'] = server_name

  # Set up colabconfig
  colabconfig['tunnel_service'] = tunnel_service
  dump(colabconfig, open(COLABCONFIG(server_name),'w'))


  LOG(f'\nDONE. Tunnel Service changed to {tunnel_service}')

# %% [markdown]
"""
---
"""

# %% [code]
# @title Change Tunnel Token
from json import load, dump
from requests import get
from bs4 import BeautifulSoup
from os.path import exists
from time import sleep

# @markdown #### **Tunnel Service** (Available tunnels: [ngrok](https://ngrok.com/), [cloudfare-argo](https://www.cloudflare.com/), [zrok.io](https://zrok.io/),  [playit.gg](https://playit.gg/), [localtonet](https://localtonet.com), [tailscale](https://tailscale.com/) and [Minekube-Gate](https://gate.minekube.com/) + playit)
tunnel_service = "minekube-gate" # @param ["zrok", "localtonet", "localxpose", "ngrok", "tailscale", "minekube-gate"]

serverconfig = load(open(SERVERCONFIG));
server_name = serverconfig['server_in_use']
colabconfig = load(open(COLABCONFIG(server_name)))

# GUIDANCE
choice = input('Do you want to show(s)/hide(h) tunnels info? - ')
if 's' in choice: clear_output(); print("\n\n- **[Ngrok](https://ngrok.com)**\n  + Follow the prompts.\n  + The IP will change whenever you restart the server.\n\n- **[Cloudflare's argo](https://www.cloudflare.com/)** :\n    - If the 'Your free tunnel has started!' notification appears => Done.\n    - Access to your server:\n    1. Download [Cloudflared client](https://github.com/cloudflare/cloudflared/releases/).\n    2. Launch the binary with `<your Cloudflare file name> access tcp --hostname <tunnel_address> --url 127.0.0.1:25565` (note: tunnel_address is your address which has been set on your Cloudflare).\n    4. Finally, connect to `127.0.0.1:25565` from the minecraft client which is located in that machine.\n\n- **[Localtonet](https://localtonet.com/)**:\n  1. Navigate to [TCP-UDG](https://localtonet.com/tunnel/tcpudp) page. Select TCP in Protocol Types.\n  2. Get your authtoken from [Authtoken](https://localtonet.com/usertoken).\n  3. Pick the server you'd like your tunnel to operate on.\n  4. Input the IP and Port values the tunnel will listen to, in this case, for Minecraft, it's typically IP: 127.0.0.1 and Port: 25565.\n  5. Finally, create and start your tunnel by pressing the Start button.\n  - Read more on [how-to-use-localtonet-with-minecraft](https://localtonet.com/documents/using-localtonet-with-minecraft)\n\n- **[Zrok](https://zrok.io/)**:\n  1. Download the zrok app through [link](https://docs.zrok.io/docs/getting-started/)\n  2. Open the shell. Type `zrok invite` to sign up and get the authtoken\n  3. Follow the prompts\n  4. Acess to https://api.zrok.io to get fully management\n   - Read more on https://docs.zrok.io/docs/getting-started. \n\n- **[PlayIt](https://playit.gg/)**: follow the prompts."); sleep(20)
clear_output()
#---------------------------------------------------------------------------------- MAIN CODE ------------------------------------------------------------------------------------#
LOG(f"\nColab Version: {colabversion}")

# Load serverconfig
serverconfig = load(open(SERVERCONFIG))
serverconfig['server_in_use'] = server_name
if tunnel_service == 'ngrok':
  LOG('Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken')
  token = input('Your authtoken: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig['ngrok_proxy']['authtoken'] = token
  LOG('Available Regions:', ' ap - Asia/Pacific (Singapore)', ' au - Australia (Sydney)', ' eu - Europa (Frankfurt - Germany)', ' in - India (Mumbai)', ' jp - Japan (Tokyo)', ' sa - America (São Paulo - Brazil)', ' us - United States (Ohio)', sep='\n')
  serverconfig['ngrok_proxy']['region'] = input('Region: ')
elif tunnel_service == 'zrok':
  # Settings variable
  if "zrok_proxy" not in serverconfig:
    serverconfig["zrok_proxy"] = {"authtoken": ""}
  token = input('Your zrok token: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig['zrok_proxy']['authtoken'] = token
elif tunnel_service == 'localtonet':
  LOG('Get your authtoken from https://localtonet.com/usertoken')
  if "localtonet_proxy" not in serverconfig:
    serverconfig["localtonet_proxy"] = {"authtoken": ""}
  token = input('Your localtonet token: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig['localtonet_proxy']['authtoken'] = token
elif tunnel_service == 'localxpose':
  LOG('Get your authtoken from https://localxpose.io/dashboard/access')
  if "localxpose_proxy" not in serverconfig:
    serverconfig["localxpose_proxy"] = {"authtoken": ""}
  token = input('Your localxpose token: ')
  if token == "":
    ERROR("\nNo token provided.")
  serverconfig['localxpose_proxy']['authtoken'] = token
elif tunnel_service == 'tailscale':
  LOG('Get your authtoken from https://login.tailscale.com/admin/settings/keys . Make sure to select reusable')
  if "tailscale_proxy" not in serverconfig:
    serverconfig["tailscale_proxy"] = {"authtoken": ""}
  if "machine_info" not in serverconfig["tailscale_proxy"]:
    serverconfig["tailscale_proxy"]["machine_info"] = ""
  sleep(10)
  token = input('Your tailscale token: ')
  if token == "":
    ERROR("\nNo token provided.")
  serverconfig['tailscale_proxy']['authtoken'] = token
elif tunnel_service == 'minekube-gate':
  LOG('Get your authtoken from https://localtonet.com/usertoken')
  if "minekube-gate_proxy" not in serverconfig:
    serverconfig["minekube-gate_proxy"] = {"token": ""}
  token = input('Your minekube token: ')
  if token == "":
    ERROR("\nNo token provided")
  serverconfig["minekube-gate_proxy"]['token'] = token

dump(serverconfig, open(SERVERCONFIG, 'w'))

LOG('\nDONE. Tunnel Token changed.')
LOG('\nMake sure to execute the "Change Tunnel Service" cell to use the correct tunnel provider.')

# %% [markdown]
"""
---
"""

# %% [code]
# @title Playit Options
from json import load, dump
from requests import get
from bs4 import BeautifulSoup
from os.path import exists
from time import sleep
from toml import load as tload
option = "Setup / Reset agent (for key renewal)" # @param ["Setup / Reset agent (for key renewal)","Reset agent (wipe)","Save secret key to drive","Change/set secret key"]
serverconfig = load(open(SERVERCONFIG));
server_name = serverconfig['server_in_use']
colabconfig = load(open(COLABCONFIG(server_name)))

# GUIDANCE

LOG(f"\nColab Version: {colabversion}")

#---------------------------------------------------------------------------------- MAIN CODE ------------------------------------------------------------------------------------#
! command -v playit || curl -SsL https://playit-cloud.github.io/ppa/key.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/playit.gpg > /dev/null && echo "deb [signed-by=/etc/apt/trusted.gpg.d/playit.gpg] https://playit-cloud.github.io/ppa/data ./" | sudo tee /etc/apt/sources.list.d/playit-cloud.list && sudo apt -qq update && sudo apt install playit >/dev/null && echo "Playit.gg installed" || echo "Failed to install playit"

secretfile=!playit secret-path
secretfile = secretfile[0]

if option == "Change/set secret key": # Set a custom playit key/agent
  if "playit_proxy" not in serverconfig:
    serverconfig["playit_proxy"] = {"secretkey": ""}
  token = input('Enter your playit secretkey: ')
  if token == "":
    ERROR("\nNo secretkey provided")
  serverconfig['playit_proxy']['secretkey'] = token
  dump(serverconfig, open(SERVERCONFIG, 'w'))

elif option == "Save secret key to drive": # Save colab's playit token to drive
    if secretfile != "/root/.config/playit_gg/playit.toml":
      with open(secretfile, "r") as f:
        file = tload(f)
      secretkey=file["secret_key"]
      if "playit_proxy" not in serverconfig:
        serverconfig["playit_proxy"] = {"secretkey": ""}
      serverconfig['playit_proxy']['secretkey'] = secretkey
      dump(serverconfig, open(SERVERCONFIG, 'w'))
    else: ERROR("Playit not setup. Please run the setup function.")
elif option == "Setup / Reset agent (for key renewal)": # Setup or reset agent and tokens.
  if secretfile != "/root/.config/playit_gg/playit.toml":
    LOG("Deleting previous agent key.")
    !printf '\e[36m[ PLAYIT ]\e[0m ' && playit reset
    !sleep 5
    LOG("Playit setup:")
    !printf '\e[36m[ PLAYIT ]\e[0m ' && playit setup
    !sleep 5
    LOG("Setup complete. Moving key to drive")
    with open(secretfile, "r") as f:
        file = tload(f)
    secretkey=file["secret_key"]
    if "playit_proxy" not in serverconfig:
      serverconfig["playit_proxy"] = {"secretkey": ""}
    serverconfig['playit_proxy']['secretkey'] = secretkey
    dump(serverconfig, open(SERVERCONFIG, 'w'))
    LOG("DONE")

  else:
    LOG("Playit setup:")
    !printf '\e[36m[ PLAYIT ]\e[0m ' && playit setup
    !sleep 5
    LOG("Setup complete. Saving key to drive")
    secretfile=!playit secret-path
    secretfile = secretfile[0]
    with open(secretfile, "r") as f:
        file = tload(f)
    secretkey=file["secret_key"]
    if "playit_proxy" not in serverconfig:
      serverconfig["playit_proxy"] = {"secretkey": ""}
    serverconfig['playit_proxy']['secretkey'] = secretkey
    dump(serverconfig, open(SERVERCONFIG, 'w'))
    LOG("DONE.")
elif option == "Reset agent (wipe)": # Resets playit token from colab and colab files.
  LOG("Playit Reset (wipe)")
  !printf '\e[36m[ PLAYIT ]\e[0m ' && playit reset
  serverconfig['playit_proxy']['secretkey'] = ""
  dump(serverconfig, open(SERVERCONFIG, 'w'))
  LOG("DONE.")

# %% [markdown]
"""
---
"""

# %% [markdown]
"""
# 🎈  **Plugins, mods** (Java Only!)

####Download modpack/mod/plugin from [curseforge](https://www.curseforge.com/Minecraft) and [modrinth](https://modrinth.com/)
---

"""

# %% [code]
from pyngrok import conf, ngrok
from os import environ, pathsep, listdir
from zipfile import ZipFile
from requests import get, post
from time import sleep
from json import load, dump, loads
from google.colab import files as fls

# @markdown ####**Your download choice**
choice = 'search' #@param ['search', 'url', 'upload_file', 'install_geysermc', 'dynmap support']

#@markdown #### **Your search name**
search_name_or_url = '' # @param {type: 'string'}

# @markdown #####Choose the place to download mod/modpack/plugin
software = 'Curseforge' # @param ["Curseforge", "Modrinth"]

# @markdown ####**Details:**
# @markdown
# @markdown ##### (none -> don't search (version -- doesn't wellcoming to do this), default -> set up according to colabconfig file)
categories = 'none'   #@param ['none', 'default', 'vanilla', 'fabric', 'forge', 'paper', 'purpur']
versions = "default" # @param ["default"] {allow-input: true}
project_types = 'none' # @param ['none', 'default', 'mods', 'plugins', 'modpacks']
index = 'none' #@param ['none', 'relevance', 'downloads', 'follows', 'newest', 'updated']

# CHecking and setting variable
server_name = SERVER_IN_USE(server_name = '')
if exists(f"{drive_path}/{server_name}/server.properties") == False: ERROR(' Running your minecraft server before editing properties')
else:
  colabconfig = COLABCONFIG_LOAD(server_name)
  if versions == 'default': versions = colabconfig["server_version"]
  if categories == 'default': categories = colabconfig['server_type']
  if project_types == 'default':
    if 'fabric' in categories or 'forge' in categories : project_types = 'mods'
    elif 'paper' in categories or 'purpur' in categories : project_types = 'plugins'
    elif 'arclight' in categories or 'mohist'  in categories or 'banner': project_types = input('Project type (mods or plugins or modpacks) : ');
  else: project_types = 'tmp';
  if 'arclight' in categories or 'mohist'  in categories or 'banner' in categories or 'vanilla' in categories or 'snapshot' in categories: categories = 'none';
  elif 'paper' in categories or 'purpur' in categories:  ERROR(f'Hmm, maybe you install the wrong types. Your server_type (currently) is {categories}') if project_types == 'mods' else print('') ;
  elif 'fabric' in categories or 'forge' in categories:  ERROR(f'Hmm, maybe you install the wrong types. Your server_type (currently) is {categories}') if project_types == 'plugins' else print('');
if 'vanilla' in categories or 'snapshot' in categories:  ERROR(f'Hmm, maybe you install the wrong types. Your server_type (currently) is {categories}') if project_types == "modpacks" else print('');
path = f'{drive_path}/{server_name}/{project_types}'
if exists(path) == False:
  MKDIR(path)
  sleep(40)
url = ''
if choice == 'url':
  if 'http' in search_name_or_url or 'https' in search_name_or_url: url = search_name_or_url
  else: url = input('Url: ')
search_name = search_name_or_url

# I will not do remove the class file. Because:
#   1. It is hard and very slow to extract them all
#   2. It will broken in some specific runtime

#----------------------------------------------------------------------------------- MAIN CODE ---------------------------------------------------------------------------#

class Download_:
  def __init__(self, choice, url, server_name, categories, versions, project_types, index):
    self.server_name = SERVER_IN_USE(server_name)
    if exists(f"{drive_path}/{self.server_name}/server.properties") == False: ERROR(' Running your minecraft server before editing properties')
    else:
      self.colabconfig = COLABCONFIG_LOAD(self.server_name)
      self.categories = categories
      self.versions = versions
      self.project_types = project_types
      self.index = index
      self.path = f'{drive_path}/{self.server_name}/{self.project_types}'
      self.choice = choice
      self.url = url
  def FACETS(self, software):
    # Get all the syntax
    categories = ''; index = ''; versions = ''
    if software == 'Modrinth':
      facets = "["
      if self.categories != 'none': facets += '["categories:' + self.categories + '"]';
      if facets != '[' and self.versions != 'none': facets += "," + '["versions:' + self.versions +'"]'
      elif self.versions != 'none': facets += '["versions:' + self.versions + '"]';
      if self.project_types == 'mods': project_types = 'mod'
      elif self.project_types == 'plugins': project_types = 'plugin'
      if facets != '[' and self.project_types != 'tmp': facets += "," + '["project_type:' + project_types + '"]'
      elif self.project_types != 'tmp': facets += '["project_type:' + project_types + '"]'
      facets += "]"; facetsInURL = "";
      if facets != "[]": facetsInURL += f'&facets={facets}'
      if self.index != "none": facetsInURL += f'&index={self.index}'
      return facetsInURL
    else:
      if self.categories != 'none':
        if self.categories == 'fabric': categories = 4 #Fabric
        elif self.categories == 'forge': categories = 1 #Forge
        elif self.categories == 'quilt': categories = 5 # quilt
        categories = f"&modLoaderType={categories}"
      if self.index != "none":
        if self.index == "relevance": index = 1 # Featured
        elif self.index == "downloads": index = 6 #TotalDownloads
        elif self.index == "follows": index = 2 #Popularity
        elif self.index == "newest": index = 11 #ReleasedDate
        elif self.index == "updated": index = 3 #LastUpdated
        index = f"&sortField={index}"
      if self.versions != "none": versions = f"&gameVersion={self.versions}"
      return categories + versions + index
  def SEARCH(self, search_name, software):
    project = {}
    LOG(f'\nSearching for the related of {search_name} ...\n')
    facetsInURL = self.FACETS(software)
    if software == "Modrinth":
      # Get syntax and get data
      rJSON = GET(f'https://api.modrinth.com/v2/search?query={search_name}{facetsInURL}').json()
      # Get the list of all relevant project
      for hit in rJSON['hits']:
        # Auditing if it for server or not.
        if hit['server_side'] == 'optional' or hit['server_side'] == 'required':
          # Get a full list title : description
          print(hit['slug'], " : ", hit['description'])
          project[hit['slug']] = hit['project_id']
    elif software == 'Curseforge':
      LOG(f"Curseforge doesn't have the exact searching key for cilent-side or server-side => you may get errors when running this {self.project_types}")
      # Because I haven't found any corresponded of project types in the search engine of Curseforge, I don't use it for searching.
      # The gameid of Minecraft is 432
      rJSON = GET(f"https://api.curse.tools/v1/cf/mods/search?gameId=432&searchFilter={search_name}{facetsInURL}").json()
      # Get the list of all relevant project
      for hit in rJSON["data"]:
        # Get a full list name: summary
        print(hit["name"], ' : ', hit["summary"])
        project[hit['name']] = str(hit["id"])
    # Checking whether your search name wrong or not. If yes => Get the name of project => Get project id
    project_names =''
    if project == {}: ERROR(f"\nSomething went wrong. Please check your search name.")
    else:
      LOG('\nType the project_name you want to download')
      project_names= input('Project_name: ')
      while project_names not in project:
        LOG('\nWrong project_names please type aigain. If you want to quit, type "None".')
        project_names= input('\nProject_name: ')
        if project_names == 'None': ERROR('Stopping...')
    return [project, project_names]
  def MODPACK(self, file_name, software):
    # settings up
    sleep(40)
    %cd $drive_path
    server_name = self.server_name
    path_drive = file_name
    while path_drive.find('.') != -1: path_drive = path_drive[path_drive.find('.')+1:]
    path_drive = file_name[: file_name.find('.' + path_drive)]
    if exists(f'{drive_path}/{self.server_name}/tmp/{path_drive}') == False:
      MKDIR(f'{self.server_name}/tmp/{path_drive}')
      sleep(40)
    # Unzipping modpack
    ! unzip -q '{server_name}/tmp/{file_name}' -d '{server_name}/tmp/{path_drive}' > /dev/null &&echo 'Unzip done' || echo 'Failed to unzip'
    sleep(30)
    # Copy the directory in orverrides and paste it (overrides includes the config files of the developer)
    try:
      for fln in listdir(f'{server_name}/tmp/{path_drive}/overrides'):
        ! mv -f '{server_name}/tmp/{path_drive}/overrides/{fln}' '{drive_path}/{server_name}' > /dev/null && echo 'Moving done' || echo 'Failed to move'
        sleep(40)
    except: pass
    # Each page give the difference file json. The file json give full details.
    # (Modrinth: modrinth.index.json- Download link, Curseforge: manifest.json - fileID, projectID) for mods which is included in modpack.
    if software == 'Modrinth':
      with ZipFile(f'{server_name}/tmp/{file_name}') as myzip:
        manifest = loads(myzip.read('modrinth.index.json'))['files']
        for file_ in manifest:
          path_ = file_["path"].split("/")[0]; file_name_ = file_["path"].split("/")[1]
          DOWNLOAD_FILE(url = file_["downloads"][0], path = f'{drive_path}/{self.server_name}/{path_}', file_name = file_name_)
    else:
      with ZipFile(f'{server_name}/tmp/{file_name}') as myzip:
        manifest = loads(myzip.read('manifest.json'))['files']
        for file_ in manifest:
          project_id =  file_["projectID"]; fileID = str(file_["fileID"]); rJSON = GET(f'https://api.curse.tools/v1/cf/mods/{project_id}/files/{fileID}').json()["data"]
          DOWNLOAD_FILE(url = f'https://www.curseforge.com/api/v1/mods/{project_id}/files/{fileID}/download', path = f'{drive_path}/{self.server_name}/mods', file_name = rJSON["fileName"])
  def Install_(self, search_name, software):
    LOG(f'Acessing: {self.server_name}')
    if self.choice == 'url':
      url = self.url
      # Find file_name in download url
      filename = input('File name (optional) : ')
      if filename == '':
        filename = url[url.find("/") + 1:]
        while filename.find("/")!= -1: filename = filename[filename.find("/") + 1:]
      else:
        format = input('Format : ')
        if f".{format}" not in filename: filename += f".{format}"
      # Download file
      if ' ' in filename: filename = filename.replace(' ', '_')
      DOWNLOAD_FILE(url= url, path = self.path, file_name= filename)
      if self.project_types == 'tmp': self.MODPACK(file_name= filename, software= software); sleep(40)
      LOG('\nCompleted')
    elif self.choice == 'upload_file':
      uploaded = fls.upload()
      try:
        file_ = [fn for fn in uploaded.keys()][0] # Get the name of the uploaded file
        filename = input('File name (optinal)') # The file name which you want to be
        if filename != '':
          format = input('Format : ')
          if format != '' and f".{format}" not in filename: filename += f".{format}"
          else: format = file_[file_.find('.'):]
          try:
            ! sudo mv -f '{drive_path}/{file_}' '{self.path}/{filename}.{format}'
          except: ERROR("Lol, you didn't upload file yet.")
        else:
          ! sudo mv -f '{drive_path}/{file_}' '{self.path}/{file_}'
        if self.project_types == 'tmp': self.MODPACK(file_name= filename, software= software); sleep(40)
        LOG('\nCompleted.')
      except: ERROR("Lol, you didn't upload file yet.")
    elif self.choice == 'search':
      a = self.SEARCH(search_name, software)
      project = a[0]; project_names = a[1]; check = False;
      project_id = project[project_names]
      if software == 'Modrinth': rJSON = GET(f'https://api.modrinth.com/v2/project/{project_id}/version').json()
      else: rJSON = GET(f'https://api.curse.tools/v1/cf/mods/{project_id}').json()['data']['latestFilesIndexes'];
      for data in rJSON:
        if software == 'Curseforge': gameversions= data["gameVersion"]
        else: gameversions = data["game_versions"]
        if self.versions in gameversions:
          if software == 'Curseforge': files = data['filename']; url = f'https://www.curseforge.com/api/v1/mods/{project_id}/files/' + str(data['fileId']) + '/download'
          else: files = data['files'][0]['filename']; url = data['files'][0]['url']
          if ' ' in files: files = files.replace(' ', '_')
          DOWNLOAD_FILE(url= url, path = self.path, file_name= files)
          check = True
        if check == True and self.project_types == 'tmp':  self.MODPACK(file_name= files, software= software); LOG('\nCompleted.'); break
        elif check: LOG('\nCompleted.'); break
      if check == False: ERROR(f"It seems that {self.software} doesn't support this {self.project_types}")
    elif choice == 'install_geysermc':
      if self.categories != 'none' and self.colabconfig['tunnel_service'] in ["playit", "zrok"] and self.categories != 'forge':
        if 'velocity' in self.categories:
          rJSON = GET('https://api.papermc.io/v2/projects/velocity').json()['versions']
          if self.versions not in rJSON: ERROR('Not found versions')
          if exists(f'{drive_path}/{server_name}/plugins') == False:
            MKDIR(f'{drive_path}/{server_name}/plugins')
            sleep(40)
          plugin = ['ViaVersion', 'ViaBackwards']
          for plugins in plugin:
            rJSON = GET(f'https://hangar.papermc.io/api/v1/projects/{plugins}/versions').json()['result']; check = False
            if self.categories.upper() in rJSON[0]['platformDependenciesFormatted']:
              for hit in rJSON:
                if self.versions in hit['platformDependencies'][self.categories.upper()]:
                  DOWNLOAD_FILE(url = hit["downloads"][self.categories.upper()]["downloadUrl"], path = f'{drive_path}/{self.server_name}/plugins', file_name = hit['downloads'][self.categories.upper()]["fileInfo"]['name'])
                  check = True; break
              if check == False: LOG(f"{plugins} can't be downloaded in your velocity server. You can try to install and upload it through website")
              else: LOG(f'Installing {plugins} done. Try to install  for more supporter version')
            else: LOG(f"{plugins} can't be downloaded in your velocity server. You can try to install and upload it through website")
          DOWNLOAD_FILE(url = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/velocity', path = f'{drive_path}/{server_name}/plugins', file_name = 'Geyser-Velocity.jar')
          LOG('You only need to install Floodgate on the BungeeCord or Velocity proxy server, unless you want to use the Floodgate API on the backend servers. Additionally, it will display Bedrock edition skins properly.')
          LOG('For more details. Check out https://wiki.geysermc.org/floodgate/setup/')
          DOWNLOAD_FILE(url = 'https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/velocity', path = f'{drive_path}/{server_name}/plugins', file_name = 'floodgate-velocity.jar')
        elif 'fabric' in self.categories:
          rJSON = GET('https://meta.fabricmc.net/v2/versions/game').json()['version']
          # warningserver_version
          if self.versions < rJSON and self.versions >= '1.17':
            LOG('Geyser-Fabric run only on 1.21.')
            LOG('To use Geyser with an older server version, you can use Geyser on a BungeeCord/Velocity proxy or Geyser-paper instead')
          else: ERROR(f"Your server_type isn't compatible for running Geyser_MC")
          LOG('Geyser only works with server-side mods. Mods that require a client-side install will not work!')
          LOG('Download geyser mc mods')
          DOWNLOAD_FILE(url = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric', path = f'{drive_path}/{self.server_name}/mods', file_name= 'Geyser-Fabric.jar')
          # Geyser mc mod require fabric api.
          LOG('Download Fabric api (requirement)')
          rJSON = GET(f'https://api.modrinth.com/v2/project/P7dR8mSH/version').json()
          check = False
          for data in rJSON:
            if self.versions in data["game_versions"]:
              files = data['files'][0]; url = files['url']
              DOWNLOAD_FILE(url= url, path = self.path, file_name= files['filename']); check = True
            if check: break
          if check == False: ERROR(f"It seems that theresn't fabric api for this minecraft version")
          LOG('Download floodgate')
          rJSON = GET(f'https://api.modrinth.com/v2/project/bWrNNfkb/version').json()
          check = False
          for data in rJSON:
            if versions in data["game_versions"]:
              files = data['files'][0]; url = files['url']
              DOWNLOAD_FILE(url= url, path = self.path, file_name= files['filename']); check = True
            if check: break
          if check == False: ERROR(f"It seems that theresn't fabric api for this minecraft version")
        elif 'paper' in self.categories or 'purpur' in self.categories:
          rJSON = GET('https://api.papermc.io/v2/projects/paper').json()['versions'][-1]
          if self.versions < rJSON and self.versions >= '1.17':
            plugin = ['ViaVersion', 'ViaBackwards']
            for plugins in plugin:
              rJSON = GET(f'https://hangar.papermc.io/api/v1/projects/{plugins}/versions').json()['result']; check = False
              if self.categories.upper() in rJSON[0]['platformDependenciesFormatted']:
                for hit in rJSON:
                  if self.versions in hit['platformDependencies'][self.categories.upper()]:
                    DOWNLOAD_FILE(url = hit["downloads"][self.categories.upper()]["downloadUrl"], path = f'{drive_path}/{self.server_name}/plugins', file_name = hit['downloads'][self.categories.upper()]["fileInfo"]['name'])
                    check = True; break
                if check == False: LOG(f"{plugins} can't be downloaded in your velocity server. You can try to install and upload it through website")
                else: LOG(f'Installing {plugins} done. Try to install  for more supporter version')
              else: LOG(f"{plugins} can't be downloaded in your velocity server. You can try to install and upload it through website")
          else: ERROR(f"Your server_type isn't compatible for running Geyser_MC")
          LOG('Download geyser mc plugin')
          DOWNLOAD_FILE(url = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot', path = f'{drive_path}/{self.server_name}/plugins', file_name= 'Geyser-Spigot.jar')
          LOG('Download floodgate')
          DOWNLOAD_FILE(url = 'https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot', path = f'{drive_path}/{self.server_name}/plugins', file_name = 'floodgate-spigot.jar')
        # Set up notification
        self.colabconfig['Geysermc']= 'notdone'
        dump(self.colabconfig, open(COLABCONFIG(self.server_name),'w'))
        # Ping
        LOG('\nInstalling done. Try to rerun the server to configuration.')
      else: ERROR(f"Your server_type isn't compatible for running Geyser_MC")
    elif choice == 'dynmap support':
      if self.categories == 'paper' or self.categories == 'purpur' or self.categories == 'fabric' or self.categories == 'forge':
        if self.colabconfig['tunnel_service'] != 'ngrok' or self.colabconfig['tunnel_service'] != 'playit' or self.colabconfig['tunnel_service'] != 'localtonet' or self.colabconfig['tunnel_service'] !='zrok': ERROR('The server is not compatible to use dynmap')
        if self.categories == 'fabric' or self.categories == 'forge': software = 'Curseforge'
        else: software = 'Modrinth'
        check = False
        if software == 'Modrinth': project_id = 'fRQREgAc'; rJSON = GET(f'https://api.modrinth.com/v2/project/{project_id}/version').json()
        else: project_id = '59433'; rJSON = GET(f'https://api.curse.tools/v1/cf/mods/{project_id}').json()['data']['latestFilesIndexes'];
        for data in rJSON:
          if software == 'Curseforge': gameversions= data["gameVersion"]
          else: gameversions = data["game_versions"]
          if self.versions in gameversions:
            if software == 'Curseforge' and self.catergories in ganeversions[0]: url = f'https://www.curseforge.com/api/v1/mods/{project_id}/files/' + str(data['fileId']) + '/download'
            elif self.categories in data['loaders']: url = data['files'][0]['url']
            DOWNLOAD_FILE(url= url, path = self.path, file_name= 'dynmap-server.jar')
            check = True
          if check: LOG('\nCheck https://github.com/webbukkit/dynmap/wiki/Installation-Setup-of-Dynmap-on-Linux for more informations.'); LOG('\nWe have done the step 1 in the set up dynmap guide. Enjoy!'); break
        if check == False: ERROR(f"It seems that there is an error in installing dynmap plugin/mod")
      else: ERROR('Wrong choice')

#----------------------------------------------------------------------------------- RUNNING ---------------------------------------------------------------------------#
LOG(f"\nColab Version: {colabversion}")
Download_(choice = choice, url = url, server_name = server_name, categories = categories, versions= versions, project_types= project_types, index= index).Install_( search_name = search_name.lower(), software = software)

# %% [markdown]
"""
---
"""

# %% [markdown]
"""
# **📁 File Management** (Java Only!)
---

"""

# %% [code]
from os.path import exists
from time import sleep
LOG(f"\nColab Version: {colabversion}")
# @markdown #### **Back up server or file?**
server_name= SERVER_IN_USE(server_name= '')
path = '/content/drive/MyDrive/minecraft' # Default path. Change to any location you wanna
choice = 'server' # @param ['server', 'file']
file_name = ''; file_backup = '';  server_backup = ''
if choice == 'server':
  server_backup = input('Server back up name: ')
else: file_name = input('File name'); file_backup = input('File back up name: ')

# Settings path
if file_name != '':
  path1 = path + f'/{server_name}/' + file_name
  if server_backup != '':
    if exists(f'{drive_path}/{server_backup}') == False:
      !mkdir '{drive_path}/{server_backup}'
      sleep(40)
  if file_backup != '' and server_backup != '': path2 = path + f'/{server_backup}/' + file_backup
  elif file_backup != '' and server_backup == '': path2 = path + f'/{server_name}/' + file_backup
  elif file_backup == '' and server_backup != '':  path2 = path + f'/{server_backup}/' + '(back-up)'
  else: path2 = path + f'/{server_name}/' + '(back-up)'
else:
  path1 = path + f'/{server_name}'
  if server_backup != '': path2 = path + f'/{server_backup}'
  else: path2 = path + f'/{server_name}' + '(back-up)'
# Checking and zipping
if exists(path1) == False: ERROR(' Creating your minecraft server before backing up files')
if exists(path2) == True: ERROR(' Back up path exists')
# Zipping
!zip -r '{path2}.zip' '{path1}' && echo "Zipping done!" || echo "Zipping faled."
# Download
INFO('We recommend you to download manually on Google Drive, anyways.')
choice = input('Download your file? (y/n) : ')
if choice == 'y': fls.download(f'{path2}.zip')

# %% [code]
from google.colab import files as fls
from os import listdir
LOG(f"\nColab Version: {colabversion}")

%cd $drive_path
# @markdown #### **World map uploader**
choice = 'upload_file' # @param ['upload_file', 'url']
world  = 'see all available' # @param ['see all available', 'world', 'world_nether', 'world_the_end']
server_name = SERVER_IN_USE(server_name = '')
print(server_name)

if exists(f"{drive_path}/{server_name}/world") == False: ERROR('Running your minecraft server')
else:
  INFO("This only applied on .zip files. Others will work too but won't be supported")
  if world == 'see all available':
    world_ = [i for i in listdir(f'{drive_path}/{server_name}') if 'world' in i]
    LOG('All world file found: ')
    for world in world_: print('       -       ', world)
    world = input('World file: ')
  if choice == 'url':
    # Download file
    INFO('Check that the .ZIP file or .ZIP file URL is direct to the world files.')
    sleep(4)
    url = input('Download link : ')
    DOWNLOAD_FILE(url= url, path= f"{drive_path}/{server_name}", file_name= 'tmp.zip')
    # Unzipping
    !sudo unzip {drive_path}/{server_name}/tmp.zip -d $world >/dev/null
    !rm -rf "{drive_path}/{server_name}/tmp.zip" >/dev/null
  else:
    %cd $drive_path/$server_name
    # Download file
    uploaded = fls.upload()
    try:
      file_name = [fn for fn in uploaded.keys()][0] # Get the name of the uploaded file
      # Unzipping
      zip_path = f'{drive_path}/{server_name}/{file_name}'
      !rm -rf "{drive_path}/{server_name}/world" "{drive_path}/{server_name}/world_nether" "{drive_path}/{server_name}/world_the_end"
      !sudo unzip '{zip_path}' -d '{world}' > /dev/null && echo "Unzipped successfully" || echo "Failed to unzip. Your file musn't has special characters like / ? ( ) among others. Check and try again. If you think this is an error contact us by our discord: https://discord.gg/XRFWV9EREu"
      !rm -rf "{drive_path}/{server_name}/{file_name}" >/dev/null
    except: ERROR("Lol, you didn't upload file yet.")
  %cd $drive_path

# %% [markdown]
"""
# **⚡ Server Improvement** (Java Only!)
---
"""

# %% [code]
from jproperties import Properties
from os.path import exists
from time import sleep
from ruamel.yaml import YAML
import sys
yaml = YAML()
LOG(f"\nColab Version: {colabversion}")

# @markdown #### **Improve the tps of your server.**
# @markdown ##### Some plugins/mods/settings will be affeted after running this function. Thinking carefully.

#---------------------------------------------------------------------------------- MAIN CODE ------------------------------------------------------------------------------------#

server_name = SERVER_IN_USE(server_name = ''); colabconfig = COLABCONFIG_LOAD(server_name)
if exists(f'{drive_path}/{server_name}/plugins') == True or exists(f'{drive_path}/{server_name}/mods') == True:
  if exists(f'{drive_path}/{server_name}/plugins') == True: path = f'{drive_path}/{server_name}/plugins'
  elif exists(f'{drive_path}/{server_name}/mods') == True: path = f'{drive_path}/{server_name}/mods'
  choice = input('Chunky (y/n) :')
  if 'y' in choice.lower():
    LOG('Installing chunky.'); LOG('Any plugin/software that enables/disables/reloads plugins on runtime. See this https://github.com/YouHaveTrouble/minecraft-optimization#plugins-enablingdisabling-other-plugins to understand why.')
    check = False; project_id = 'fALzjamp'; rJSON = GET(f'https://api.modrinth.com/v2/project/{project_id}/version').json()
    for data in rJSON:
      gameversions = data["game_versions"]
      if colabconfig['server_version'] in gameversions and colabconfig['server_type'] in data['loaders']: url = data['files'][0]['url']; DOWNLOAD_FILE(url= url, path = path, file_name= 'chunky.jar'); check = True
      if check: break
    if check == False: ERROR(f"It seems that there is an error in installing chunky.jar")

if exists(f"{drive_path}/{server_name}/server.properties") == False: ERROR(' Running your minecraft server before editing properties')
else:
  LOG('Changing server.properties')
  server_properties = Properties()
  with open(f"{drive_path}/{server_name}/server.properties", "rb") as f:
      server_properties.load(f, "utf-8")
  server_properties["sync-chunk-writes"] = 'false'
  server_properties['network-compression-threshold'] = '-1'
  server_properties['simulation-distance'] = '4'
  server_properties['view-distance'] = '7'
  with open(f"{drive_path}/{server_name}/server.properties", "wb") as f:
      server_properties.store(f, encoding="utf-8")

LOG('List of yaml files which have been edited: \n')
if exists(f'{drive_path}/{server_name}/purpur.yml'):
  with open(f'{drive_path}/{server_name}/purpur.yml', 'r') as file_:
    config = yaml.load(file_)
  config['use-alternate-keepalive'] = 'true'
  config['player']['teleport-if-outside-border'] = 'true'
  yaml.dump(config, sys.stdout)

if exists(f'{drive_path}/{server_name}/spigot.yml'):
  with open(f'{drive_path}/{server_name}/spigot.yml') as file_:
    config = yaml.load(file_)
  config['world-settings']['default']['view-distance'] = 'default'
  config['world-settings']['default']['mob-spawn-range'] = 3
  config['world-settings']['default']['entity-activation-range']['animals'] = 16
  config['world-settings']['default']['entity-activation-range']['monsters'] = 24
  config['world-settings']['default']['entity-activation-range']['raiders'] = 48
  config['world-settings']['default']['entity-activation-range']['misc'] = 8
  config['world-settings']['default']['entity-activation-range']['water'] = 8
  config['world-settings']['default']['entity-activation-range']['villagers'] = 16
  config['world-settings']['default']['entity-activation-range']['flying-monsters'] = 48
  config['world-settings']['default']['entity-tracking-range'] = {'players': 48, 'animals': 48, 'monsters': 48, 'misc': 32, 'other': 64}
  config['world-settings']['default']['merge-radius'] = {'item': 3.5, 'exp': 4.0}
  yaml.dump(config, sys.stdout)

if exists(f'{drive_path}/{server_name}/config/paper-world-defaults.yml'):
  with open(f'{drive_path}/{server_name}/config/paper-world-defaults.yml') as file_:
    config = yaml.load(file_)
  config['chunks']['delay-chunk-unloads-by'] -'10s'
  config['chunks']['max-auto-save-chunks-per-tick'] = 10
  config['chunks']['prevent-moving-into-unloaded-chunks'] = 'true'
  config['chunks']['entity-per-chunk-save-limit'] = {'area_effect_cloud': 8, 'arrow': 16, 'dragon_fireball': 3, 'egg': 8, 'ender_pearl': 8,
                                                     'experience_bottle': 3, 'experience_orb': 16, 'eye_of_ender': 8, 'fireball': 8, 'firework_rocket': 8,
                                                     'llama_spit': 3, 'potion': 8, 'shulker_bullet': 8, 'small_fireball': 8, 'snowball': 8, 'spectral_arrow': 16,
                                                     'trident': 16, 'wither_skull': 4}
  config['entities']['spawning']['non-player-arrow-despawn-rate'] = 20
  config['entities']['spawning']['despawn-ranges'] = {'ambient': {'hard': 72, 'soft': 30}, 'axolotl': {'hard': 72, 'soft': 30}, 'creature': {'hard': 72, 'soft': 30}, 'misc': {'hard': 72, 'soft': 30},
                                                      'monster': { 'hard': 72, 'soft': 30}, 'underground_water_creature': {'hard': 72, 'soft': 30}, 'water_ambient': {'hard': 72, 'soft': 30}, 'water_creature': {'hard': 72, 'soft': 30}}
  config['entities']['spawning']['per-player-mob-spawns'] = 'true'
  config['entities']['spawning']['alt-item-despawn-rate'] = {'enabled': 'true', 'items': {'cobblestone': 300, 'netherrack': 300, 'sand': 300, 'red_sand': 300, 'gravel': 300, 'dirt': 300, 'short_grass': 300, 'pumpkin': 300, 'melon_slice': 300, 'kelp': 300,
                                                                                          'bamboo': 300, 'sugar_cane': 300, 'twisting_vines': 300, 'weeping_vines': 300, 'oak_leaves': 300, 'spruce_leaves': 300, 'birch_leaves': 300, 'jungle_leaves': 300,
                                                                                          'acacia_leaves': 300, 'dark_oak_leaves': 300, 'mangrove_leaves': 300, 'cactus': 300, 'diorite': 300, 'granite': 300, 'andesite': 300, 'scaffolding': 600}}
  config['misc']['update-pathfinding-on-block-update'] = 'false'
  config['misc']['redstone-implementation'] = 'ALTERNATE_CURRENT'
  config['collisions']['max-entity-collisions'] = 2
  config['collisions']['fix-climbing-bypassing-cramming-rule']= 'true'
  config['environment']['optimize-explosions'] = 'true'
  config['environment']['nether-ceiling-void-damage-height'] = 127
  yaml.dump(config, sys.stdout)

if exists(f'{drive_path}/{server_name}/bukkit.yml'):
  with open(f'{drive_path}/{server_name}/bukkit.yml') as file_:
    config = yaml.load(file_)
  config['spawn-limits'] = {'monsters': 20, 'animals': 5, 'water-animals': 2, 'water-ambient': 2, 'water-underground-creature': 3, 'axolotls': 3, 'ambient': 1}
  config['ticks-per'] = {'monster-spawns': 10, 'animal-spawns': 400, 'water-spawns': 400, 'water-ambient-spawns': 400, 'water-underground-creature-spawns': 400, 'axolotl-spawns': 400, 'ambient-spawns': 400}
  yaml.dump(config, sys.stdout)

choice = input('More guide (y/n) ?')
if 'y' in choice.lower():
  if exists(f'{drive_path}/{server_name}/plugins'):
    LOG('NOTICES: ')
    LOG('Plugins removing ground items is not necessary. If you download those plugins, please remove them')
    LOG("Mob stacker plugins: \n It's really hard to justify using one.\n Stacking naturally spawned entities causes more lag than not stacking them at all due to the server constantly trying to spawn more mobs.\n The only 'acceptable' use case is for spawners on servers with a large amount of spawners.")
    LOG('Plugins enabling/disabling other plugins:\n Anything that enables or disables plugins on runtime is extremely dangerous.\n Loading a plugin like that can cause fatal errors with tracking data and disabling a plugin can lead to errors due to removing dependency. \n The /reload command suffers from exact same issues and you can read more about them in https://madelinemiller.dev/blog/problem-with-reload/')

  LOG('HOW TO MEASURE LAG: ')
  if colabconfig['server_type'] == 'paper':
    LOG("Paper offers a /mspt command that will tell you how much time the server took to calculate recent ticks. If the first and second value you see are lower than 50, then congratulations!\n Your server is not lagging! If the third value is over 50 then it means there was at least 1 tick that took longer. That's completely normal and happens from time to time, so don't panic.")
  if exists(f'{drive_path}/{server_name}/plugins'):
    LOG("Spark (https://spark.lucko.me/) is a plugin that allows you to profile your server's CPU and memory usage. You can read on how to use it on its wiki.\n There's also a guide on how to find the cause of lag spikes here: https://spark.lucko.me/docs/guides/Finding-lag-spikes")
  LOG("Way to see what might be going on when your server is lagging are Timings. Timings is a tool that lets you see exactly what tasks are taking the longest.\n It's the most basic troubleshooting tool and if you ask for help regarding lag you will most likely be asked for your Timings. Timings is known to have a serious performance impact on servers, it's recommended to use the Spark plugin over Timings and use Purpur or Pufferfish to disable Timings all together.")
  LOG("To get Timings of your server, you just need to execute the /timings paste command and click the link you're provided with.\n You can share this link with other people to let them help you. It's also easy to misread if you don't know what you're doing. ")
  LOG("There is a detailed video tutorial by Aikar (https://www.youtube.com/watch?v=T4J0A9l7bfQ) on how to read them.")

  LOG('Minecraft exploits and how to fix them: To see how to fix exploits that can cause lag spikes or crashes on a Minecraft server, refer to https://github.com/YouHaveTrouble/minecraft-exploits-and-how-to-fix-them')

LOG('Completed')

