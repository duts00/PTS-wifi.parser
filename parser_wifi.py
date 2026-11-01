#!/usr/bin/env python3
"""
parser_wifi.py - Parser de arquivos Kismet NetXML (redes e clientes WiFi).

Projeto de estudo em Pentest WiFi. Uso autorizado apenas: redes proprias
ou ambientes com permissao explicita.

Exemplos:
    python3 parser_wifi.py dump-01.kismet.netxml
    python3 parser_wifi.py dump-01.kismet.netxml --redes
    python3 parser_wifi.py dump-01.kismet.netxml --redes --clientes -o saida/
"""

import os
import csv
import argparse
import xml.etree.ElementTree as ET

# Colorama e opcional: se nao estiver instalado, o script roda sem cor.
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class _Sem:
        def __getattr__(self, _):
            return ""
    Fore = Style = _Sem()


BANNER = r"""
 __        ___ _ _____ ___
 \ \      / (_) |_   _|_ _|
  \ \ /\ / /| | | | |  | |
   \ V  V / | | | | |  | |
    \_/\_/  |_|_| |_| |___|

 WiFi NetXML Parser
 Study Project - Pentest WiFi
"""


def show_banner():
    print(Fore.CYAN + BANNER)
    print(Style.DIM + " Author  : duts00")
    print(Style.DIM + " Input   : .kismet.netxml (Kismet)")
    print(Style.DIM + " Output  : Terminal | TXT | CSV")
    print("-" * 60)


def _texto(elemento, tag, padrao="None"):
    """Retorna o texto de um sub-elemento, ou um padrao se ausente/vazio."""
    achado = elemento.find(tag)
    if achado is not None and achado.text:
        return achado.text.strip()
    return padrao


def extrair_redes(root):
    """Extrai a lista de redes. Um dicionario NOVO por rede (sem vazamento)."""
    redes = []
    for net in root.iter("wireless-network"):
        ssid = net.find("SSID")
        rede = {
            "ESSID": _texto(ssid, "essid") if ssid is not None else "None",
            "BSSID": _texto(net, "BSSID"),
            "CHANNEL": _texto(net, "channel"),
            "ENC": _texto(ssid, "encryption") if ssid is not None else "None",
        }
        redes.append(rede)
    return redes


def extrair_clientes(root):
    """Extrai a lista de clientes, ligando cada um a sua rede."""
    clientes = []
    for net in root.iter("wireless-network"):
        ssid = net.find("SSID")
        essid = _texto(ssid, "essid") if ssid is not None else "None"
        bssid = _texto(net, "BSSID")
        for cli in net.iter("wireless-client"):
            clientes.append({
                "ESSID": essid,
                "BSSID": bssid,
                "CLIENT_MAC": _texto(cli, "client-mac"),
                "MANUF": _texto(cli, "client-manuf"),
                "STATUS": cli.attrib.get("type", "None"),
            })
    return clientes


def exibir_e_exportar(colunas, larguras, registros, base_saida, outdir):
    """Imprime em tabela no terminal e exporta para TXT e CSV."""
    if not registros:
        print(Fore.YELLOW + " Nenhum registro encontrado.")
        return

    header = "  ".join(f"{c:<{w}}" for c, w in zip(colunas, larguras))
    print(Fore.CYAN + header)
    print("-" * len(header))
    for reg in registros:
        linha = "  ".join(f"{str(reg[c]):<{w}}" for c, w in zip(colunas, larguras))
        print(linha)

    os.makedirs(outdir, exist_ok=True)
    txt_path = os.path.join(outdir, base_saida + ".txt")
    csv_path = os.path.join(outdir, base_saida + ".csv")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write("-" * len(header) + "\n")
        for reg in registros:
            f.write("  ".join(f"{str(reg[c]):<{w}}"
                               for c, w in zip(colunas, larguras)) + "\n")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(registros)

    print(Style.DIM + f"\n [ok] {len(registros)} registro(s) | {txt_path} | {csv_path}")


def mostrar_redes(root, outdir):
    colunas = ["ESSID", "BSSID", "CHANNEL", "ENC"]
    larguras = [25, 20, 8, 12]
    exibir_e_exportar(colunas, larguras, extrair_redes(root), "wifi", outdir)


def mostrar_clientes(root, outdir):
    colunas = ["ESSID", "BSSID", "CLIENT_MAC", "MANUF", "STATUS"]
    larguras = [25, 20, 18, 20, 10]
    exibir_e_exportar(colunas, larguras, extrair_clientes(root), "wifi_clients", outdir)


def menu(root, outdir):
    """Modo interativo (quando nenhuma flag de acao e passada)."""
    while True:
        print("\n 1 - Mostrar lista de Redes")
        print(" 2 - Mostrar lista de Clientes")
        print(" 0 - Sair\n")
        op = input(" > Digite um numero: ").strip()
        if op == "1":
            mostrar_redes(root, outdir)
        elif op == "2":
            mostrar_clientes(root, outdir)
        elif op == "0":
            break
        else:
            print(Fore.YELLOW + " Opcao invalida.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parser de Kismet NetXML (uso autorizado apenas).",
        epilog="Exemplo: python3 parser_wifi.py dump-01.kismet.netxml --redes -o saida/",
    )
    parser.add_argument("arquivo", help="Arquivo .kismet.netxml gerado pelo Kismet")
    parser.add_argument("--redes", action="store_true", help="Lista as redes WiFi")
    parser.add_argument("--clientes", action="store_true", help="Lista os clientes WiFi")
    parser.add_argument("-o", "--outdir", default=".",
                        help="Diretorio de saida dos arquivos (padrao: atual)")
    return parser.parse_args()


def main():
    args = parse_args()
    show_banner()

    if not os.path.isfile(args.arquivo):
        raise SystemExit(f" [erro] Arquivo nao encontrado: {args.arquivo}")

    try:
        root = ET.parse(args.arquivo).getroot()
    except ET.ParseError as e:
        raise SystemExit(f" [erro] XML invalido: {e}")

    # Se passou flag de acao, executa direto (modo automatizavel).
    if args.redes or args.clientes:
        if args.redes:
            mostrar_redes(root, args.outdir)
        if args.clientes:
            mostrar_clientes(root, args.outdir)
    else:
        # Sem flag -> modo interativo (menu).
        menu(root, args.outdir)


if __name__ == "__main__":
    main()
