import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# =================================================================
# PROJE HİYERARŞİSİ
# =================================================================
# YÖNTEM 2: RSA (Asimetrik Şifreleme)
#   --> İÇ YOL 1: RSA-1024 (Şu an bu projedesiniz)
#   --> İÇ YOL 2: RSA-2048 (Sıradaki)
#   --> İÇ YOL 3: RSA-4096 (Planlanan)
# =================================================================

# --- ROL TANIMI ---
# Bu dosya: Person B (Sunucu / API / Server)
# Görevi: Kendi anahtar çiftini üretir, Public Key'i paylaşır ve Private Key ile şifreyi çözer.

print("--- RSA-1024 ANAHTAR ÇİFTİ ÜRETİLİYOR... ---")
# 1024 bitlik anahtar üretimi (İç Yol 1)
key = RSA.generate(1024)
private_key = key.export_key()
public_key = key.publickey().export_key()

def rsa_sunucu_baslat():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    
    print("\n" + "="*40)
    print("YÖNTEM 2: RSA | İÇ YOL 1: 1024-BIT")
    print("PERSON B (API/SERVER) HAZIR")
    print("="*40)
    print(f"\n[PUBLIC KEY (Dışarıya Verilecek)]:\n{public_key.decode()}\n")

    while True:
        client, addr = server.accept()
        
        # Önce Person A'ya Public Key'i gönderiyoruz (El sıkışma)
        client.send(public_key)
        
        # Sonra Person A'dan bu key ile şifrelenmiş veriyi alıyoruz
        data = client.recv(2048)
        if data:
            encrypted_msg = data.decode()
            print(f"📡 [AGDAN GELEN ŞİFRELİ]: {encrypted_msg}")
            
            # Kendi Private Key'imizle çözüyoruz
            try:
                cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
                decrypted = cipher_rsa.decrypt(base64.b64decode(encrypted_msg))
                print(f"🔓 [PRIVATE KEY İLE ÇÖZÜLDÜ]: {decrypted.decode()}")
                client.send(b"RSA-1024 basariyla cozuldu.")
            except Exception as e:
                print(f"❌ Deşifre Hatası: {e}")
                
        client.close()

if __name__ == '__main__':
    rsa_sunucu_baslat()