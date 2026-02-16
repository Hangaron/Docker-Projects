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
# Görevi: Sunucunun X25519 anahtarını kullanarak en hızlı güvenli kanalı kurmak.

TARGET_HOST = os.getenv("TARGET_HOST", "host.docker.internal")
TARGET_PORT = 5555

def baslat():
    print(f"--- PERSON A (CLIENT) BAŞLATILDI (HEDEF: {TARGET_HOST}) ---")
    print("Kullanılan Eğri: Curve25519 (X25519)")
    time.sleep(5)
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_HOST, TARGET_PORT))
            
            # 1. ADIM: Sunucudan Raw X25519 Public Key al
            server_pub_raw_b64 = s.recv(1024)
            server_pub_raw = base64.b64decode(server_pub_raw_b64)
            server_public_key = ECC.import_key(server_pub_raw, curve_name='X25519')
            
            # 2. ADIM: Kendi X25519 geçici anahtarımızı üretelim
            my_key = ECC.generate(curve='X25519')
            
            # 3. ADIM: Ortak Sır üretimi (Key Agreement)
            shared_secret = key_agreement(static_priv=my_key, static_pub=server_public_key, kdf=lambda x: SHA256.new(x).digest())
            
            # 4. ADIM: Veriyi şifrele
            msg = "Gizli X25519 Mesaji: Dunyanin en hizli kriptografik egrisi!"
            print(f"-> Orijinal: {msg}")
            
            cipher_aes = AES.new(shared_secret, AES.MODE_CBC)
            iv = cipher_aes.iv
            ciphertext = cipher_aes.encrypt(pad(msg.encode(), AES.block_size))
            
            # 5. ADIM: Paketi gönder
            payload = {
                "client_pub": base64.b64encode(my_key.public_key().export_key(format='Raw')).decode(),
                "iv": base64.b64encode(iv).decode(),
                "data": base64.b64encode(ciphertext).decode()
            }
            s.send(json.dumps(payload).encode())
            
            print(f"-> X25519 hibrit paketi gonderildi.")
            print(f"-> Yanıt: {s.recv(1024).decode()}")
            s.close()
            
        except Exception as e:
            print(f"Hata: {e}")
        
        print("-" * 30)
        time.sleep(10)

if __name__ == '__main__':
    baslat()