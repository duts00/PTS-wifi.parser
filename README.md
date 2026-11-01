# Pentest WiFi — Parser de Kismet NetXML

Script em Python 3 que realiza o parsing de arquivos `.kismet.netxml` (gerados pelo Kismet) para extrair e organizar informações sobre redes WiFi e clientes detectados. Desenvolvido durante estudos de Pentest WiFi, a partir de um código apresentado em curso, com melhorias de organização, visualização e exportação dos dados.

---

## Aviso Legal

Ferramenta destinada ao estudo e à análise de redes próprias ou de ambientes com autorização explícita. A captura e a análise de tráfego de redes WiFi de terceiros sem consentimento podem configurar crime (no Brasil, Lei 12.737/2012 e Marco Civil da Internet). Use de forma ética e responsável.

---

## Objetivo

A partir de um arquivo `.kismet.netxml`, o script extrai e apresenta:

- Redes WiFi detectadas (ESSID, BSSID)
- Clientes conectados
- Canal de operação
- Tipo de criptografia
- Fabricante dos dispositivos

Os dados são exibidos no terminal em formato tabular e exportados para arquivos TXT e CSV.

---

## Tecnologias

- Python 3
- `xml.etree.ElementTree` (biblioteca padrão)
- Kismet (para a geração do arquivo `.netxml`)

---

## Funcionalidades

### Listagem de redes WiFi

Exibe em formato de tabela: ESSID, BSSID, canal e criptografia.
Exporta para: `wifi.txt` e `wifi.csv`.

### Listagem de clientes WiFi

Exibe: ESSID, BSSID, MAC do cliente, fabricante do dispositivo e status do cliente.
Exporta para: `wifi_clients.txt` e `wifi_clients.csv`.

---

## Melhorias em relação ao código original

Partindo do código apresentado no curso, foram feitas melhorias de usabilidade, robustez e organização, mantendo a lógica de parsing:

- Caminho do arquivo e saída por argumentos de linha de comando (`argparse`), em vez de editar o script
- Modo direto (flags `--redes`/`--clientes`) para automação, além do menu interativo
- Correção de um problema de dados: cada rede passa a usar um dicionário próprio, evitando que valores de uma rede vazem para outra
- Exportação com o módulo `csv`, que trata corretamente campos com vírgula
- Tratamento de erros (arquivo inexistente, XML inválido) e de campos ausentes
- Dependência de `colorama` tornada opcional
- Saída no terminal em formato tabular, com cabeçalhos alinhados

---

## Como Utilizar

### Requisitos

- Python 3.x (apenas biblioteca padrão)
- `colorama` (opcional, apenas para cor no terminal; o script roda sem ele)
- Um arquivo `.kismet.netxml` gerado pelo Kismet

O caminho do arquivo é passado por argumento — não é mais necessário editar o script.

### Modo interativo (menu)

```bash
python3 parser_wifi.py dump-01.kismet.netxml
```

Abre o menu para escolher entre listar redes ou clientes.

### Modo direto (automatizável)

```bash
# apenas redes
python3 parser_wifi.py dump-01.kismet.netxml --redes

# redes e clientes, salvando em uma pasta específica
python3 parser_wifi.py dump-01.kismet.netxml --redes --clientes -o saida/
```

### Opções

| Flag | Função |
|---|---|
| `--redes` | Lista as redes WiFi |
| `--clientes` | Lista os clientes WiFi |
| `-o`, `--outdir` | Diretório de saída (padrão: atual) |
| `-h`, `--help` | Exibe a ajuda |

Ao final, os dados são exibidos no terminal e exportados para `wifi.txt`, `wifi.csv`, `wifi_clients.txt` e `wifi_clients.csv`.

---

## Possíveis Melhorias (exercícios)

- Filtros por criptografia, canal ou fabricante
- Exportação em JSON, além de TXT e CSV
- Resolução de fabricante por OUI (prefixo do MAC) a partir de uma base local
- Destaque automático de redes com criptografia fraca (WEP/aberta)

---

## Nota Final

Projeto de estudo em Pentest WiFi e Python aplicado à análise de redes. O objetivo é compreender como ferramentas de reconhecimento de redes sem fio organizam e interpretam os dados coletados — e, a partir disso, reconhecer configurações inseguras e reforçar a proteção das próprias redes.

---

Desenvolvido por duts00 — projeto de estudo em segurança da informação
