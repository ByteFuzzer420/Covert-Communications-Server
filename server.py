import socket
import threading
import os
from colorama import Style, Fore
import pyAesCrypt
import zlib
import io

class Covert_Communications:

    def __init__(self, Address, Port):
        self.Address = Address
        self.Port = Port
        self.server = None
        self.clients = []
        self.lock = threading.Lock()
        self.bufferSize = 64 * 1024
        self.password = "secret"
        self.all_messages = []

    server_side_key_store = []

    def start_server(self):
        self.server_side_key()
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.Address, self.Port))
        self.server.listen(5)
        print(f"[+] Server started on {self.Address}:{self.Port}")
        print(f"[*] The server-side key is: {self.server_side_key_store[0]}")

    def stop_server(self):
        if self.server:
            self.server.close()
            self.server = None
            print(f"[-] Server stopped")
        else:
            print("[-] Server is not running")
    
    def server_side_key(self):
        if not self.server_side_key_store:
            key = ''.join([chr(os.urandom(1)[0] % 26 + ord('a')) for _ in range(60)])
            self.server_side_key_store.append(key)
        return self.server_side_key_store[0]
    
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

    def secure_send(self, unsecure_message):
        password = 'secret'
        bufferSize = 64 * 1024
        pbdata = unsecure_message.encode("utf-8")
        fIn = io.BytesIO(pbdata)
        fCiph = io.BytesIO()
        fDec = io.BytesIO()
        pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
        encrypted_message_final = fCiph.getvalue()
        compress_message = zlib.compress(encrypted_message_final)
        fCiph.seek(0)
        for user in self.clients:
            user.sendall(compress_message)



    def receive_messages(self):
        while True:
            client, address = self.server.accept()
            with self.lock:
                self.clients.append(client)
            print(f"\n[+] New client connected: {address[0]}:{address[1]}")
            message = client.recv(1024)
            requested_alias = self.decrypt_with_zlib(message)
            if "ALIAS" in requested_alias:
                parsed_alias = requested_alias[6:]
                print(f'{address[0]}:{address[1]}: HAS REQUESTED THE ALIAS -> {parsed_alias}')
            else:
                pass

            thread = threading.Thread(target=self.handle_client, args=(client, address, parsed_alias))
            thread.start()
    
    def handle_client(self, client, address, alias):
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    break
                decrypted_message = self.decrypt_with_zlib(message)
                if decrypted_message:
                    formatted_message = f"{alias}:> {decrypted_message}"
                    print(f"{Fore.GREEN}[{address[0]}:{address[1]}] {formatted_message}{Style.RESET_ALL}")
                    self.all_messages.append(formatted_message)
                    self.secure_send(formatted_message)
            except Exception as e:
                print(f"{Fore.RED}Error handling client {address}: {e}{Style.RESET_ALL}")
                break
        with self.lock:
            self.clients.remove(client)
        client.close()
        print(f"[-] Client disconnected: {address[0]}:{address[1]}")

if __name__ == "__main__":
    address = ("127.0.0.1", 9001)
    server = Covert_Communications(address[0], address[1])
    server.start_server()
    server.receive_messages()
