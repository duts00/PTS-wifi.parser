# Pentest WiFi – Parser Kismet NetXML

Este projeto consiste em um script em **Python** desenvolvido durante estudos em **Pentest WiFi**, a partir de um código apresentado em curso.  
A versão aqui publicada mantém a lógica original de parsing, porém recebeu **melhorias na organização, visualização e exportação dos dados**, tornando o uso mais prático e legível.

---

## 🎯 Objetivo

Realizar o parsing de arquivos `.kismet.netxml` (gerados pelo Kismet) para extrair informações relevantes sobre:

- Redes WiFi detectadas
- Clientes conectados
- Canal de operação
- Tipo de criptografia
- Fabricante dos dispositivos

Os dados são exibidos no terminal de forma organizada e exportados para arquivos **TXT** e **CSV**.

---

## 🛠️ Tecnologias utilizadas

- Python 3
- xml.etree.ElementTree
- Kismet (para geração do arquivo `.netxml`)

---

## ⚙️ Funcionalidades

### 🔹 Listagem de Redes WiFi
Exibe em formato de tabela:
- ESSID
- BSSID
- Canal
- Criptografia

Gera os arquivos:
- `wifi.txt`
- `wifi.csv`

### 🔹 Listagem de Clientes WiFi
Exibe:
- ESSID
- BSSID
- MAC do cliente
- Fabricante do dispositivo
- Status do cliente

Gera os arquivos:
- `wifi_clients.txt`
- `wifi_clients.csv`

---

## ✨ Melhorias implementadas

Em relação ao código original utilizado no curso, foram realizadas as seguintes melhorias:

- Organização da saída no terminal em formato tabular
- Inclusão de cabeçalhos alinhados
- Melhor legibilidade visual dos dados
- Tratamento de campos ausentes (`None`)
- Padronização da exportação para CSV e TXT

> O foco das modificações foi melhorar a **usabilidade e apresentação dos resultados**, mantendo o funcionamento original do parser.

---

## ▶️ Como utilizar

1. Gere um arquivo `.kismet.netxml` utilizando o Kismet
2. Ajuste o caminho do arquivo no script:

```python
arquivo = '/caminho/para/dump-01.kismet.netxml'
