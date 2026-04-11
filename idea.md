

# script1: Utilizamos un bucle while 1 para ejecutar el comando durante 3600 segundos
'''
while [ 1 ]
do
    curl --silent https://tria.ge/reports/public?limit=1000 | grep -i data-clipboard | awk -F"\"" '{ print $4}' >> hashes_triage.txt
    sleep 3600
done
'''


# script2: VX Vault
'''
import requests
import hashlib
import re
import time


def download_page(url):
    page = requests.get(url)
    content = page.content.decode('utf-8')
    return content

def detect_ips(content):
    # buscar IP
    ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content)
    return ips

def detect_hashes_md5(content):
    hashes = re.findall(r'[a-fA-F\d]{32,40}', content)
    hashes_calculated = [hashlib.md5(hash.encode('utf-8')).hexdigest() for hash in hashes]
    return hashes_calculated

def detect_hashes_sha256(content):
    hashes = re.findall(r'[a-fA-F\d]{32,40}', content)
    hashes_calculated = [hashlib.sha256(hash.encode('utf-8')).hexdigest() for hash in hashes]
    return hashes_calculated

def bajar_hashes_virusshare():
    #PAra bajar un zip de 700 megas con todo bajar de aqui: https://virusshare.com/hashes
    url = 'https://virusshare.com/hashfiles/VirusShare_00000.md5'
    content = download_page(url)
    hashes = detect_hashes_md5(content)
    #print(hashes)


def bajar_hashes_triage():
    url = 'https://tria.ge/reports/public?limit=1000'
    content = download_page(url)
    hashes = detect_hashes_sha256(content)
    guardar_fichero_en_disco('hashes_triage.txt', hashes)
    print(hashes)
    #print(content)

def bajar_hashes_valhalla():
    url = 'https://valhalla.nextron-systems.com'
    content = download_page(url)
    hashes = detect_hashes_sha256(content)
    guardar_fichero_en_disco('hashes_valhalla.txt', hashes)
    #print(hashes)

def bajar_hashes_vxvault():
    url = 'http://vxvault.net/ViriList.php?s=0&m=100'
    content = download_page(url)
    hashes = detect_hashes_md5(content)
    guardar_fichero_en_disco('hashes_md5_vxvault.txt', hashes)
    ips = detect_ips(content)
    guardar_fichero_en_disco('ips_vxvault.txt', ips)
    print (hashes)
    print (ips)

def guardar_fichero_en_disco(fichero, hashes):
    file = open(fichero, 'a')
    for value in hashes:
        file.write(value + '\n')
    file.close


#bajar_hashes_valhalla()
#bajar_hashes_triage()


#PAra bajar un zip de 700 megas con todo bajar de aqui: https://virusshare.com/hashes
#PAra bajar más IOC de Twitter: https://github.com/0xDanielLopez/TweetFeed#page_facing_up-data-collected
#Github con IOC de malware actualizado https://github.com/executemalware/Malware-IOCs



while True:
    print ("Bajando...")
    #bajar_hashes_triage()
    #bajar_hashes_valhalla()
    bajar_hashes_vxvault()
    time.sleep(3600)
	
'''	
	
	
	
	
	
	






#script3

'''
import requests
import hashlib
import re
import time


def download_page(url):
    page = requests.get(url)
    content = page.content.decode('utf-8')
    return content


def detect_hashes_md5(content):
    hashes = re.findall(r'[a-fA-F\d]{32,40}', content)
    hashes_calculated = [hashlib.md5(hash.encode('utf-8')).hexdigest() for hash in hashes]
    return hashes_calculated

def detect_hashes_sha256(content):
    hashes = re.findall(r'[a-fA-F\d]{32,40}', content)
    hashes_calculated = [hashlib.sha256(hash.encode('utf-8')).hexdigest() for hash in hashes]
    return hashes_calculated

def bajar_hashes_virusshare():
    #PAra bajar un zip de 700 megas con todo bajar de aqui: https://virusshare.com/hashes
    url = 'https://virusshare.com/hashfiles/VirusShare_00000.md5'
    content = download_page(url)
    hashes = detect_hashes_md5(content)
    #print(hashes)


def bajar_hashes_triage():
    url = 'https://tria.ge/reports/public?limit=1000'
    content = download_page(url)
    hashes = detect_hashes_sha256(content)
    guardar_fichero_en_disco('hashes_triage.txt', hashes)
    print(hashes)
    #print(content)

def bajar_hashes_valhalla():
    url = 'https://valhalla.nextron-systems.com'
    content = download_page(url)
    hashes = detect_hashes_sha256(content)
    guardar_fichero_en_disco('hashes_valhalla.txt', hashes)
    #print(hashes)

def guardar_fichero_en_disco(fichero, hashes):
    file = open(fichero, 'a')
    for value in hashes:
        file.write(value + '\n')
    file.close


#bajar_hashes_valhalla()
#bajar_hashes_triage()


#PAra bajar un zip de 700 megas con todo bajar de aqui: https://virusshare.com/hashes
#PAra bajar más IOC de Twitter: https://github.com/0xDanielLopez/TweetFeed#page_facing_up-data-collected
#Github con IOC de malware actualizado https://github.com/executemalware/Malware-IOCs



while True:
    print ("Bajando...")
    bajar_hashes_triage()
    bajar_hashes_valhalla()
    time.sleep(3600)
	
'''


#Servicios gratuitos en la nube
  Tier gratuito generoso

  Railway
  - Similar a Render pero con mejor UX
  - $5 crédito gratis/mes (suficiente para proyectos pequeños)
  - Deploys desde GitHub, soporte para casi cualquier lenguaje
  - Muy bueno para proyectos Python

  Fly.io
  - 3 VMs pequeñas gratis + 3GB storage
  - Más orientado a contenedores (Docker)
  - Bueno si tu app ya está dockerizada

  Koyeb
  - 1 servicio gratuito siempre activo (sin sleep como Render free)
  - Soporte nativo para Python, Node, Go
  - Buena opción si necesitas que no duerma

  Funciones/Serverless (distinto modelo)

  Vercel / Netlify
  - Ideales para APIs sin estado o funciones pequeñas
  - Tier gratuito muy generoso
  - Limitados para procesos largos o background jobs

  Cloudflare Workers
  - Extremadamente rápido, edge computing
  - 100k requests/día gratis
  - Limitado a JS/WASM (no Python directo)

  Para tu caso específico (el miner)

  Dado que tu proyecto hace scraping periódico y publica en Telegram, lo que más te conviene es:

  ┌────────────┬───────────────┬───────────┬────────┐
  │ Plataforma │ Sleep en free │ Cron jobs │ Python │
  ├────────────┼───────────────┼───────────┼────────┤
  │ Render     │ Si            │ Si (paid) │ Si     │
  ├────────────┼───────────────┼───────────┼────────┤
  │ Railway    │ No            │ Si        │ Si     │
  ├────────────┼───────────────┼───────────┼────────┤
  │ Koyeb      │ No            │ No nativo │ Si     │
  ├────────────┼───────────────┼───────────┼────────┤
  │ Fly.io     │ Configurable  │ No nativo │ Si     │
  └────────────┴───────────────┴───────────┴────────┘

  Railway sería mi recomendación principal como alternativa — tiene mejor DX que Render y el crédito mensual cubre perfectamente proyectos personales pequeños.

