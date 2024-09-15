import socket
from colorama import Style, Fore
import pyAesCrypt
import io
import zlib
import threading

class connect_covert:
    def __init__(self, target, port, password):
        self.target = target
        self.port = port
        self.password = password
        self.bufferSize = 64 * 1024
        self.conn = None
    
    def connect(self):
        try:
            if self.conn is None:
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn.connect((self.target, self.port))
                print(f"{Fore.GREEN}Connected to {self.target}:{self.port}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Already connected to {self.target}:{self.port}{Style.RESET_ALL}")
        except socket.error as e:
            print(f"{Fore.RED}Error connecting: {e}{Style.RESET_ALL}")
    
    def recieve_message(self):
        while True:
            try:
                compressed_message = self.conn.recv(1024)
                if compressed_message:
                    decoded_message = self.decrypt_with_zlib(compressed_message)
                    print(f"\n{Fore.CYAN}[" + f"{Fore.RED}Server" + f"{Fore.CYAN}]:" + f"{decoded_message}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error receiving message: {e}{Style.RESET_ALL}")
                break

    def secure_send(self, unsecure_message):
        try:
            pbdata = unsecure_message.encode("utf-8")
            fIn = io.BytesIO(pbdata)
            fCiph = io.BytesIO()
            pyAesCrypt.encryptStream(fIn, fCiph, self.password, self.bufferSize)
            encrypted_message = fCiph.getvalue()
            compressed_message = zlib.compress(encrypted_message)
            self.conn.send(compressed_message)
        except Exception as e:
            print(f"{Fore.RED}Error sending message: {e}{Style.RESET_ALL}")

    def decrypt_with_zlib(self, compressed_message):
        try:
            decompressed_message = zlib.decompress(compressed_message)
            fDecompressed = io.BytesIO(decompressed_message)
            fOut = io.BytesIO()
            pyAesCrypt.decryptStream(fDecompressed, fOut, self.password, self.bufferSize, len(decompressed_message))
            decrypted_message = fOut.getvalue().decode("utf-8")
            return decrypted_message
        except Exception as e:
            print(f"{Fore.RED}Decryption error: {e}{Style.RESET_ALL}")
            return None

    def send_message(self):
        while True:
            SET_USER = self.set_alias[6:]
            user_input = input(f"{SET_USER}@covert~# ")
            self.secure_send(user_input)
    
    def initialize_user(self):
        print(Style.BRIGHT + Fore.WHITE + "[" + Style.BRIGHT + Fore.GREEN + "*" + Style.BRIGHT + Fore.WHITE + "]" + Style.BRIGHT + Fore.WHITE + " Enter the alias you wish to go by")
        user_alias = input(":> ")
        print(Style.BRIGHT + Fore.WHITE + "[" + Style.BRIGHT + Fore.BLUE + "+" + Style.BRIGHT + Fore.WHITE + "]" + Style.BRIGHT + Fore.WHITE + f"You are now known as {user_alias}")
        self.set_alias = f"ALIAS {user_alias}"
        self.secure_send(self.set_alias)

if __name__ == "__main__":
    target = "127.0.0.1"
    port = 9001
    password = "secret"
    ss = connect_covert(target, port, password)
    ss.connect()
    ss.initialize_user()
    send_thread = threading.Thread(target=ss.send_message)
    receive_thread = threading.Thread(target=ss.recieve_message)
    send_thread.start()
    receive_thread.start()
    send_thread.join()
    receive_thread.join()
