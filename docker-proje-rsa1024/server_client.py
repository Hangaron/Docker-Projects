import socket
import time
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# Bu dosya 'server_client.py' adıyla kaydedilmelidir.
# Görevi: Mesajı AES-128 ile kilitleyip göndermek (Encryption).

TARGET_HOST = os.getenv("TARGET_HOST", "host.docker.internal")
TARGET_PORT = 5555
SHARED_KEY = b'1234567890123456' # Sunucu ile aynı olmak zorunda

def encrypt_message(message):
    # AES CBC modu için rastgele bir IV oluşturulur
    cipher = AES.new(SHARED_KEY, AES.MODE_CBC)
    iv = cipher.iv
    
    # Mesajı blok boyutuna tamamla (padding) ve şifrele
    encrypted_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    
    # IV + Şifreli Veri birleştirilip Base64 ile metne çevrilir
    # Bu sayede ağda güvenle taşınabilir
    return base64.b64encode(iv + encrypted_bytes).decode('utf-8')

def baslat():
    print(f"--- AES-128 GÖNDERİCİ BAŞLATILDI (Hedef: {TARGET_HOST}) ---")
    time.sleep(5)
    
    while True:
        try:
            msg = "Gizli Bilgi: Gizli Gorev Basariyla Tamamlandi!"
            print(f"-> Orijinal Mesaj: {msg}")
            
            # Mesajı kilitle
            encrypted_payload = encrypt_message(msg)
            print(f"-> Sifrelenmis (AES): {encrypted_payload}")
            
            # Ağ üzerinden gönder
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_HOST, TARGET_PORT))
            s.send(encrypted_payload.encode())
            
            response = s.recv(1024)
            print(f"-> Sunucu Onayi: {response.decode()}")
            s.close()
            
        except Exception as e:
            print(f"Baglanti Hatasi: {e}")
        
        print("-" * 30)
        time.sleep(5)

if __name__ == '__main__':
    baslat()