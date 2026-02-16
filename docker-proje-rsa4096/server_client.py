import socket
import time
import os
from Crypto.PublicKey import ECC
from Crypto.Protocol.DH import key_agreement
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
import base64

# --- ROL TANIMI ---
# Bu dosya: Person A (İstemci / Client)
# Görevi: Sunucunun ECC Public Key'ini kullanarak ortak bir anahtar üretmek (ECDH) ve veriyi şifrelemek.

TARGET_HOST = os.getenv("TARGET_HOST", "host.docker.internal")
TARGET_PORT = 5555

def baslat():
    print(f"--- PERSON A (CLIENT) BAŞLATILDI (HEDEF: {TARGET_HOST}) ---")
    print("Seçilen Algoritma: ECC (NIST P-256 Curve)")
    time.sleep(5)
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_HOST, TARGET_PORT))
            
            # 1. ADIM: Sunucunun ECC Public Key'ini al
            server_pub_key_raw = s.recv(2048)
            server_public_key = ECC.import_key(server_pub_key_raw)
            
            # 2. ADIM: Kendi geçici (ephemeral) ECC anahtarımızı üretelim
            my_key = ECC.generate(curve='P-256')
            
            # 3. ADIM: ECDH ile Ortak Sır (Shared Secret) üretelim
            # Sunucu B'nin Public Key + Bizim Private Key = Ortak Sır
            shared_secret = key_agreement(static_priv=my_key, static_pub=server_public_key, kdf=lambda x: SHA256.new(x).digest())
            
            # 4. ADIM: Mesajı bu ortak sır ile AES kullanarak şifreleyelim
            msg = "Gizli ECC Mesaji: WhatsApp ve Blockchain bu teknolojiyi kullaniyor!"
            print(f"-> Orijinal Mesaj: {msg}")
            
            cipher_aes = AES.new(shared_secret, AES.MODE_CBC)
            iv = cipher_aes.iv
            ciphertext = cipher_aes.encrypt(pad(msg.encode(), AES.block_size))
            
            # 5. ADIM: Kendi Public Key'imizi ve Şifreli Veriyi paketleyelim
            # Sunucunun deşifre yapabilmesi için bizim geçici public key'imize ihtiyacı var
            payload = {
                "client_pub": my_key.public_key().export_key(format='PEM'),
                "iv": base64.b64encode(iv).decode(),
                "data": base64.b64encode(ciphertext).decode()
            }
            
            import json
            s.send(json.dumps(payload).encode())
            
            print(f"-> ECC tabanli hibrit sifreleme ile paket gonderildi.")
            print(f"-> Sunucu Yanıtı: {s.recv(1024).decode()}")
            s.close()
            
        except Exception as e:
            print(f"Hata: {e}")
        
        print("-" * 30)
        time.sleep(10)

if __name__ == '__main__':
    baslat()