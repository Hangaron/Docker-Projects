import socket
from Crypto.PublicKey import ECC
from Crypto.Protocol.DH import key_agreement
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
import base64
import json

# =================================================================
# PROJE HİYERARŞİSİ
# =================================================================
# YÖNTEM 3: ECC (Elliptic Curve Cryptography)
#   --> İÇ YOL 1: NIST P-256 (Tamamlandı)
#   --> İÇ YOL 2: X25519 / Ed25519 (Şu an bu projedesiniz - HIZ ŞAMPİYONU)
#   --> İÇ YOL 3: Brainpool / Custom Curves (Planlanan)
# =================================================================

# --- ROL TANIMI ---
# Bu dosya: Person B (Sunucu / API / Server)
# Görevi: Modern X25519 anahtarını paylaşır ve gelen paketleri deşifre eder.

print("--- ECC (X25519) ANAHTAR ÇİFTİ ÜRETİLİYOR... ---")
# X25519 anahtarları üretmek inanılmaz hızlıdır.
my_key = ECC.generate(curve='X25519')
public_key_raw = my_key.public_key().export_key(format='Raw') # Modern raw format

def ecc_sunucu_baslat():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    
    print("\n" + "="*45)
    print("YÖNTEM 3: ECC | İÇ YOL 2: X25519 (Modern)")
    print("PERSON B (API/SERVER) AKTİF - HIZLI MOD")
    print("="*45)
    print(f"\n[X25519 PUBLIC KEY (Raw)]: {base64.b64encode(public_key_raw).decode()}\n")

    while True:
        client, addr = server.accept()
        
        # 1. ADIM: Raw Public Key'imizi gönderelim
        client.send(base64.b64encode(public_key_raw))
        
        # 2. ADIM: İstemciden gelen hibrit paketi alalım
        data = client.recv(4096)
        if data:
            try:
                payload = json.loads(data.decode())
                # İstemcinin gönderdiği public key'i al
                client_pub_raw = base64.b64decode(payload['client_pub'])
                client_pub_key = ECC.import_key(client_pub_raw, curve_name='X25519')
                
                iv = base64.b64decode(payload['iv'])
                ciphertext = base64.b64decode(payload['data'])
                
                # 3. ADIM: X25519 Key Agreement (Diffie-Hellman)
                shared_secret = key_agreement(static_priv=my_key, static_pub=client_pub_key, kdf=lambda x: SHA256.new(x).digest())
                
                # 4. ADIM: AES Deşifre
                cipher_aes = AES.new(shared_secret, AES.MODE_CBC, iv)
                decrypted = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)
                
                print(f"🔓 [X25519 + AES ÇÖZÜLDÜ]: {decrypted.decode()}")
                client.send(b"X25519 basariyla cozuldu. En modern egriden selamlar!")
            except Exception as e:
                print(f"❌ Deşifre Hatası: {e}")
                
        client.close()

if __name__ == '__main__':
    ecc_sunucu_baslat()