import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# =================================================================
# PROJE HİYERARŞİSİ
# =================================================================
# YÖNTEM 2: RSA (Asimetrik Şifreleme)
#   --> İÇ YOL 1: RSA-1024 (Tamamlandı)
#   --> İÇ YOL 2: RSA-2048 (Tamamlandı)
#   --> İÇ YOL 3: RSA-4096 (Şu an bu projedesiniz - ZİRVE)
# =================================================================

# --- ROL TANIMI ---
# Bu dosya: Person B (Sunucu / API / Server)
# Görevi: 4096-bitlik devasa bir anahtar üretir. Bu işlem biraz zaman alabilir!

print("--- RSA-4096 ANAHTAR ÇİFTİ ÜRETİLİYOR... (Lütfen Bekleyin) ---")
# 4096 bitlik anahtar üretimi (İç Yol 3 - En Üst Seviye Güvenlik)
# Not: Bu işlem bilgisayar hızına göre 2-10 saniye sürebilir.
key = RSA.generate(4096)
private_key = key.export_key()
public_key = key.publickey().export_key()

def rsa_sunucu_baslat():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    
    print("\n" + "="*40)
    print("YÖNTEM 2: RSA | İÇ YOL 3: 4096-BIT")
    print("PERSON B (API/SERVER) HAZIR")
    print("="*40)
    print(f"\n[PUBLIC KEY (Dışarıya Verilecek - Devasa Boyut)]:\n{public_key.decode()[:100]}... (devamı var)")

    while True:
        client, addr = server.accept()
        
        # Devasa Public Key gönderiliyor
        client.send(public_key)
        
        # 4096-bit şifreli veri için buffer boyutunu 8192'ye çıkardık
        data = client.recv(8192) 
        if data:
            encrypted_msg = data.decode()
            print(f"\n📡 [AGDAN GELEN ŞİFRELİ (Büyük Paket)]: {encrypted_msg[:50]}...")
            
            try:
                cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
                decrypted = cipher_rsa.decrypt(base64.b64decode(encrypted_msg))
                print(f"🔓 [4096-BIT PRIVATE KEY İLE ÇÖZÜLDÜ]: {decrypted.decode()}")
                client.send(b"RSA-4096 basariyla cozuldu. Askeri standart onaylandi.")
            except Exception as e:
                print(f"❌ Deşifre Hatası: {e}")
                
        client.close()

if __name__ == '__main__':
    rsa_sunucu_baslat()