#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import os
import datetime
import time
import subprocess
import json
import uuid
from time import strftime
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = r"""
 __        ___ _ _____ ___ 
 \ \      / (_) |_   _|_ _|
  \ \ /\ / /| | | | |  | | 
   \ V  V / | | | | |  | | 
    \_/\_/  |_|_| |_| |___|

 WiFi NetXML Parser
 Study Project – Pentest WiFi
 Improved Output & Visualization
"""

def show_banner():
    os.system("clear")
    print(Fore.CYAN + BANNER)
    print(Style.DIM + " Author  : duts00")
    print(Style.DIM + " Context : Cybersecurity / WiFi Pentest Studies")
    print(Style.DIM + " Input   : .kismet.netxml (Kismet)")
    print(Style.DIM + " Output  : Terminal | TXT | CSV")
    print("-" * 60)


dic_wf = {}
dic_wfclient = {}
arquivo = '/caminho/para/dump-01.kismet.netxml'


def parse_xml_wf():
    filetxt = open('/caminho/para/wifi.txt', 'w')
    filecsv = open('/caminho/para/wifi.csv', 'w')

    tree = ET.parse(arquivo)
    root = tree.getroot()

    header = f"{'ESSID':<25} {'BSSID':<20} {'CHANNEL':<8} {'ENC':<10}"
    print(header)
    print('-' * len(header))

    filetxt.write(header + '\n')
    filetxt.write('-' * len(header) + '\n')
    filecsv.write('ESSID,BSSID,CHANNEL,ENC\n')

    for i in root.iter('detection-run'):
        for j in i:
            for h in j:
                if h.tag == 'SSID':
                    for y in h:
                        if y.tag == 'essid':
                            dic_wf[y.tag] = y.text
                        if y.tag == 'encryption':
                            dic_wf[y.tag] = y.text

                if h.tag == 'BSSID':
                    dic_wf[h.tag] = h.text

                if h.tag == 'channel':
                    dic_wf[h.tag] = h.text

                dic_wf.setdefault('essid', 'None')
                dic_wf.setdefault('encryption', 'None')

            essid = str(dic_wf.get('essid', 'None'))
            bssid = str(dic_wf.get('BSSID', 'None'))
            channel = str(dic_wf.get('channel', 'None'))
            enc = str(dic_wf.get('encryption', 'None'))

            line = f"{essid:<25} {bssid:<20} {channel:<8} {enc:<10}"
            print(line)

            filetxt.write(line + '\n')
            filecsv.write(f'{essid},{bssid},{channel},{enc}\n')

    filetxt.close()
    filecsv.close()


def parse_xml_wf_client():
    filetxt = open('/caminho/para/wifi_clients.txt', 'w')
    filecsv = open('/caminho/para/wifi_clients.csv', 'w')

    tree = ET.parse(arquivo)
    root = tree.getroot()

    header = f"{'ESSID':<25} {'BSSID':<20} {'CLIENT MAC':<18} {'MANUF':<20} {'STATUS':<10}"
    print(header)
    print('-' * len(header))

    filetxt.write(header + '\n')
    filetxt.write('-' * len(header) + '\n')
    filecsv.write('ESSID,BSSID,CLIENT_MAC,MANUF,STATUS\n')

    for i in root.iter('detection-run'):
        for j in i:
            for h in j:
                if h.tag == 'SSID':
                    for y in h:
                        if y.tag == 'essid':
                            dic_wfclient[y.tag] = y.text

                if h.tag == 'BSSID':
                    dic_wfclient[h.tag] = h.text

                if h.tag == 'wireless-client':
                    dic_wfclient['type'] = h.attrib.get('type', 'None')
                    for w in h:
                        if w.tag == 'client-mac':
                            dic_wfclient[w.tag] = w.text
                        if w.tag == 'client-manuf':
                            dic_wfclient[w.tag] = w.text

                    essid = dic_wfclient.get('essid', 'None')
                    bssid = dic_wfclient.get('BSSID', 'None')
                    client_mac = dic_wfclient.get('client-mac', 'None')
                    manuf = dic_wfclient.get('client-manuf', 'None')
                    status = dic_wfclient.get('type', 'None')

                    if essid != 'None':
                        line = f"{essid:<25} {bssid:<20} {client_mac:<18} {manuf:<20} {status:<10}"
                        print(line)
                        filetxt.write(line + '\n')
                        filecsv.write(f'{essid},{bssid},{client_mac},{manuf},{status}\n')

    filetxt.close()
    filecsv.close()


def main():
    show_banner()

    op = 99
    while int(op) > 0:
        print("\n 1 - Mostrar lista de Redes")
        print(" 2 - Mostrar lista de Clientes")
        print(" 0 - Sair\n")

        op = input(" > Digite um número: ")
        os.system('clear')
        show_banner()

        if op == '1':
            parse_xml_wf()
        elif op == '2':
            parse_xml_wf_client()

if __name__ == '__main__':
    main()
