import socket
import time
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# --- ROL TANIMI ---
# Bu dosya: Person A (İstemci / Client)
# Görevi: Sunucudan 2048-bitlik Public Key'i alıp mesajı kilitlemek.

TARGET_HOST = os.getenv("TARGET_HOST", "host.docker.internal")
TARGET_PORT = 5555

def baslat():
    print(f"--- PERSON A (CLIENT) BAŞLATILDI (HEDEF: {TARGET_HOST}) ---")
    print("Hedef Algoritma: RSA-2048")
    time.sleep(5)
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_HOST, TARGET_PORT))
            
            # Sunucudan 2048-bit Public Key alınıyor
            server_public_key_raw = s.recv(4096) 
            server_public_key = RSA.import_key(server_public_key_raw)
            
            msg = "Gizli RSA Mektubu: 2048-bit guvenlik testi."
            print(f"-> Orijinal Mesaj: {msg}")
            
            cipher_rsa = PKCS1_OAEP.new(server_public_key)
            encrypted_payload = base64.b64encode(cipher_rsa.encrypt(msg.encode())).decode()
            print(f"-> 2048-bit Public Key ile Kilitlendi: {encrypted_payload}")
            
            s.send(encrypted_payload.encode())
            print(f"-> Sunucu Yanıtı: {s.recv(1024).decode()}")
            s.close()
            
        except Exception as e:
            print(f"Hata: {e}")
        
        print("-" * 30)
        time.sleep(10)

if __name__ == '__main__':
    baslat()