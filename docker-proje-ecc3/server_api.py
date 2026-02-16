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
#   --> İÇ YOL 2: X25519 / Ed25519 (Tamamlandı)
#   --> İÇ YOL 3: Brainpool P256r1 (Şu an bu projedesiniz - FİNAL)
# =================================================================

# --- ROL TANIMI ---
# Bu dosya: Person B (Sunucu / API / Server)
# Görevi: Brainpool P256r1 eğrisi kullanarak en üst düzey regülasyonlu iletişimi yönetmek.

print("--- ECC (Brainpool P256r1) ANAHTAR ÇİFTİ ÜRETİLİYOR... ---")
# Brainpool eğrileri matematiksel olarak daha karmaşıktır.
my_key = ECC.generate(curve='brainpoolP256r1')
public_key_pem = my_key.public_key().export_key(format='PEM')

def ecc_sunucu_baslat():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    
    print("\n" + "="*45)
    print("YÖNTEM 3: ECC | İÇ YOL 3: BRAINPOOL P256R1")
    print("PERSON B (API/SERVER) AKTİF - BİLİMSEL MOD")
    print("="*45)
    print(f"\n[BRAINPOOL PUBLIC KEY]:\n{public_key_pem[:100]}...\n")

    while True:
        client, addr = server.accept()
        
        # 1. ADIM: Public Key'imizi gönderelim
        client.send(public_key_pem.encode())
        
        # 2. ADIM: İstemciden gelen hibrit paketi alalım
        data = client.recv(4096)
        if data:
            try:
                payload = json.loads(data.decode())
                client_pub_key = ECC.import_key(payload['client_pub'])
                
                iv = base64.b64decode(payload['iv'])
                ciphertext = base64.b64decode(payload['data'])
                
                # 3. ADIM: Key Agreement (Diffie-Hellman)
                shared_secret = key_agreement(static_priv=my_key, static_pub=client_pub_key, kdf=lambda x: SHA256.new(x).digest())
                
                # 4. ADIM: AES Deşifre
                cipher_aes = AES.new(shared_secret, AES.MODE_CBC, iv)
                decrypted = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)
                
                print(f"🔓 [BRAINPOOL + AES ÇÖZÜLDÜ]: {decrypted.decode()}")
                client.send(b"Brainpool P256r1 basariyla cozuldu. Guvenlik serisi tamamlandi!")
            except Exception as e:
                print(f"❌ Deşifre Hatası: {e}")
                
        client.close()

if __name__ == '__main__':
    ecc_sunucu_baslat()