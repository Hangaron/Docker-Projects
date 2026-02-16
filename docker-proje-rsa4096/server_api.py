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
#   --> İÇ YOL 1: NIST P-256 (Şu an bu projedesiniz - MODERN)
#   --> İÇ YOL 2: Ed25519 (Planlanan)
#   --> İÇ YOL 3: Brainpool Curves (Planlanan)
# =================================================================

# --- ROL TANIMI ---
# Bu dosya: Person B (Sunucu / API / Server)
# Görevi: ECC anahtarını paylaşır ve gelen ECDH paketlerini deşifre eder.

print("--- ECC (NIST P-256) ANAHTAR ÇİFTİ ÜRETİLİYOR... ---")
# RSA-4096'nın aksine ECC anahtar üretimi çok hızlıdır!
my_key = ECC.generate(curve='P-256')
public_key_pem = my_key.public_key().export_key(format='PEM')

def ecc_sunucu_baslat():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    
    print("\n" + "="*40)
    print("YÖNTEM 3: ECC | İÇ YOL 1: NIST P-256")
    print("PERSON B (API/SERVER) HAZIR")
    print("="*40)
    print(f"\n[ECC PUBLIC KEY]:\n{public_key_pem}\n")

    while True:
        client, addr = server.accept()
        
        # 1. ADIM: Public Key'imizi gönderelim
        client.send(public_key_pem.encode())
        
        # 2. ADIM: İstemciden gelen karmaşık paketi alalım
        data = client.recv(4096)
        if data:
            try:
                payload = json.loads(data.decode())
                client_pub_key = ECC.import_key(payload['client_pub'])
                iv = base64.b64decode(payload['iv'])
                ciphertext = base64.b64decode(payload['data'])
                
                # 3. ADIM: Ortak Sırrı (Shared Secret) üretelim
                # Bizim Private Key + İstemcinin Public Key = Ortak Sır
                shared_secret = key_agreement(static_priv=my_key, static_pub=client_pub_key, kdf=lambda x: SHA256.new(x).digest())
                
                # 4. ADIM: AES ile deşifre edelim
                cipher_aes = AES.new(shared_secret, AES.MODE_CBC, iv)
                decrypted = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)
                
                print(f"🔓 [ECC + ECDH İLE ÇÖZÜLDÜ]: {decrypted.decode()}")
                client.send(b"ECC-256 basariyla cozuldu. Cok daha hizli ve guvenli!")
            except Exception as e:
                print(f"❌ Deşifre Hatası: {e}")
                
        client.close()

if __name__ == '__main__':
    ecc_sunucu_baslat()