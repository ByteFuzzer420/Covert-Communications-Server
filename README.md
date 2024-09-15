![Covert-Communications-Server](https://img.shields.io/github/license/kathuluman/Covert-Communications-Server?color=blue&style=for-the-badge) 
![Version](https://img.shields.io/github/v/tag/kathuluman/Covert-Communications-Server?color=blue&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-3.0.0-green?style=for-the-badge)

# Covert-Communications-Server
A Python project I developed inspired by one of my personal projects. With this Covert Communications Server you can ensure that all of your messages to all clients are encrypted and unbreakable.

## Overview

This Covert Communications server uses AES encryption for all communication and client to server connection meaning that all data that goes through in or out is encrypted using a secret key.
If one where to forensically analyze the network traffic for this communications server all they would see is compressed encrypted data. All data sent between the server and connected clients
are compressed using `zlib` compression, utilizing this will help minimize the amount of encrypted bytes being sent directly for both optimization and better obfuscation.

## Features

- **AES Encryption**: Encryptes all socket data in and out using AES.
- **Compression**: Minimizes byte count by compressing all data using `zlib`

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/kathuluman/Covert-Communications-Server.git
    cd Covert-Communications-Server
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

2. **Run the Tool**:
    ```bash
    python3 saerveserver.py
    ```

### Usage for windows

1. **Create a Virtual Enviorment**:
    ```bash
    python3 -m venv venv
    #OR specify the install path of your python installation.
    C:\Users\USER\AppData\Local\Programs\PythonX\python.exe -m venv venv
    ```

2. **Activate The Virtual Enviorment**:
    ```bash
    .\venv\Scripts\activate
    ```

3. **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Program**:
    ```bash
    python server.py
    ## or if you are connecting to a server just run the client program
    python client.py
    ```

## Example

```bash
$ python .\client.py
Connected to 127.0.0.1:9001
[*] Enter the alias you wish to go by
:> PDiddy
[+]You are now known as PDiddy
PDiddy@covert~# Hello World!
PDiddy@covert~#
[Server]:PDiddy:> Hello World!
PDiddy@covert~#
```
