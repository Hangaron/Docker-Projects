import socket
import time
import os
from Crypto.PublicKey import ECC
from Crypto.Protocol.DH import key_agreement
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
import base64
import json

# --- ROL TANIMI ---
# Bu dosya: Person A (İstemci / Client)
# Görevi: Sunucunun Brainpool anahtarı ile regülasyonlu şifrelemeyi başlatmak.

TARGET_HOST = os.getenv("TARGET_HOST", "host.docker.internal")
TARGET_PORT = 5555

def baslat():
    print(f"--- PERSON A (CLIENT) BAŞLATILDI (HEDEF: {TARGET_HOST}) ---")
    print("Kullanılan Eğri: Brainpool P256r1")
    time.sleep(5)
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_HOST, TARGET_PORT))
            
            # 1. ADIM: Sunucudan Brainpool Public Key al
            server_pub_pem = s.recv(2048)
            server_public_key = ECC.import_key(server_pub_pem.decode())
            
            # 2. ADIM: Kendi Brainpool geçici anahtarımızı üretelim
            my_key = ECC.generate(curve='brainpoolP256r1')
            
            # 3. ADIM: Ortak Sır üretimi (Key Agreement)
            shared_secret = key_agreement(static_priv=my_key, static_pub=server_public_key, kdf=lambda x: SHA256.new(x).digest())
            
            # 4. ADIM: Veriyi şifrele
            msg = "Gizli Mesaj: Brainpool egrisi ile askeri seviye koruma."
            print(f"-> Orijinal: {msg}")
            
            cipher_aes = AES.new(shared_secret, AES.MODE_CBC)
            iv = cipher_aes.iv
            ciphertext = cipher_aes.encrypt(pad(msg.encode(), AES.block_size))
            
            # 5. ADIM: Paketi gönder
            payload = {
                "client_pub": my_key.public_key().export_key(format='PEM'),
                "iv": base64.b64encode(iv).decode(),
                "data": base64.b64encode(ciphertext).decode()
            }
            s.send(json.dumps(payload).encode())
            
            print(f"-> Brainpool hibrit paketi gonderildi.")
            print(f"-> Yanıt: {s.recv(1024).decode()}")
            s.close()
            
        except Exception as e:
            print(f"Hata: {e}")
        
        print("-" * 30)
        time.sleep(10)

if __name__ == '__main__':
    baslat()