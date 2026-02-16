import socket
import time
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# --- ROL TANIMI ---
# Bu dosya: Person A (İstemci / Client)
# Görevi: Sunucudan Public Key'i alır, mesajı bu key ile kilitler ve geri gönderir.

TARGET_HOST = os.getenv("TARGET_HOST", "host.docker.internal")
TARGET_PORT = 5555

def baslat():
    print(f"--- PERSON A (CLIENT) BAŞLATILDI (HEDEF: {TARGET_HOST}) ---")
    time.sleep(5)
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_HOST, TARGET_PORT))
            
            # 1. ADIM: Sunucunun Public Key'ini al
            server_public_key_raw = s.recv(1024)
            server_public_key = RSA.import_key(server_public_key_raw)
            
            # 2. ADIM: Mesajı bu Public Key ile şifrele
            msg = "Gizli RSA Mektubu: Asimetrik Sifreleme Testi"
            print(f"-> Orijinal Mesaj: {msg}")
            
            cipher_rsa = PKCS1_OAEP.new(server_public_key)
            encrypted_payload = base64.b64encode(cipher_rsa.encrypt(msg.encode())).decode()
            print(f"-> Public Key ile Kilitlendi: {encrypted_payload}")
            
            # 3. ADIM: Şifreli mesajı gönder
            s.send(encrypted_payload.encode())
            
            print(f"-> Sunucu Yanıtı: {s.recv(1024).decode()}")
            s.close()
            
        except Exception as e:
            print(f"Hata: {e}")
        
        print("-" * 30)
        time.sleep(10)

if __name__ == '__main__':
    baslat()