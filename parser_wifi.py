#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import os
import requests
import datetime
import requests
import time
import subprocess
import json
import uuid
from time import strftime

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
                if(h.tag == 'SSID'):
                    for y in h:
                        if(y.tag == 'essid'):
                            dic_wf[y.tag] = y.text
                        if(y.tag == 'encryption'):
                            dic_wf[y.tag] = y.text
                        if('encryption' not in dic_wf):
                            dic_wf['encryption'] = 'None'
                if(h.tag == 'BSSID'):
                    dic_wf[h.tag] = h.text
                if(h.tag == 'channel'):
                    dic_wf[h.tag] = h.text
                if('essid' not in dic_wf):
                    dic_wf['essid'] = 'None'
                if('encryption' not in dic_wf):
                    dic_wf['encryption'] = 'None'
            essid = str(dic_wf['essid'])
            bssid = str(dic_wf['BSSID'])
            channel = str(dic_wf['channel'])
            enc = str(dic_wf['encryption'])
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
    header = f"{'ESSID':<25} {'BSSID':<20} {'CLIENTE MAC':<18} {'Cliente EQP':<20} {'Status':<10}"
    print(header)
    print('-' * len(header))
    filetxt.write(header + '\n')
    filetxt.write('-' * len(header) + '\n')
    filecsv.write('ESSID,BSSID,CLIENTE MAC,Cliente EQP,Status\n')
    for i in root.iter('detection-run'):
        for j in i:
            for h in j:
                if(h.tag == 'SSID'):
                    for y in h:
                        if(y.tag == 'essid'):
                            dic_wfclient[y.tag] = y.text
                        if(y.tag == 'encryption'):
                            dic_wfclient[y.tag] = y.text
                if(h.tag == 'BSSID'):
                    dic_wfclient[h.tag] = h.text
                if(h.tag == 'wireless-client'):
                    dic_wfclient['type'] = h.attrib['type']
                    for w in h:
                        if(w.tag == 'client-mac'):
                            dic_wfclient[w.tag] = w.text
                        if(w.tag == 'client-manuf'):
                            dic_wfclient[w.tag] = w.text
                    essid = str(dic_wfclient.get('essid', 'None'))
                    bssid = str(dic_wfclient.get('BSSID', 'None'))
                    client_mac = str(dic_wfclient.get('client-mac', 'None'))
                    client_manuf = str(dic_wfclient.get('client-manuf', 'None'))
                    status = str(dic_wfclient.get('type', 'None'))
                    if(essid != 'None'):
                        line = f"{essid:<25} {bssid:<20} {client_mac:<18} {client_manuf:<20} {status:<10}"
                        print(line)
                        filetxt.write(line + '\n')
                        filecsv.write(f'{essid},{bssid},{client_mac},{client_manuf},{status}\n')
    filetxt.close()
    filecsv.close()

def main():
    op = 99
    while (int(op) > 0):
        print("\n 1 - Mostrar lista de Redes\n")
        print(" 2 - Mostrar lista de Clientes\n")
        print(" 0 - Sair\n")
        op = input(" > Digite um número: ")
        os.system('clear')
        if(op == '1'):
            parse_xml_wf()
        if(op == '2'):
            parse_xml_wf_client()

if __name__ == '__main__':
    main()
