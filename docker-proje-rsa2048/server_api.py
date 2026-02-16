import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# =================================================================
# PROJE HİYERARŞİSİ
# =================================================================
# YÖNTEM 2: RSA (Asimetrik Şifreleme)
#   --> İÇ YOL 1: RSA-1024 (Tamamlandı)
#   --> İÇ YOL 2: RSA-2048 (Şu an bu projedesiniz)
#   --> İÇ YOL 3: RSA-4096 (Planlanan)
# =================================================================

# --- ROL TANIMI ---
# Bu dosya: Person B (Sunucu / API / Server)
# Görevi: 2048-bitlik anahtar çifti üretir ve Private Key ile şifreyi çözer.

print("--- RSA-2048 ANAHTAR ÇİFTİ ÜRETİLİYOR... ---")
# 2048 bitlik anahtar üretimi (İç Yol 2 - Modern Standart)
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

def rsa_sunucu_baslat():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    
    print("\n" + "="*40)
    print("YÖNTEM 2: RSA | İÇ YOL 2: 2048-BIT")
    print("PERSON B (API/SERVER) HAZIR")
    print("="*40)
    print(f"\n[PUBLIC KEY (Dışarıya Verilecek)]:\n{public_key.decode()}\n")

    while True:
        client, addr = server.accept()
        
        # Person A'ya 2048-bitlik Public Key gönderilir
        client.send(public_key)
        
        data = client.recv(4096) # Anahtar büyüdüğü için buffer boyutunu artırdık
        if data:
            encrypted_msg = data.decode()
            print(f"📡 [AGDAN GELEN ŞİFRELİ]: {encrypted_msg}")
            
            try:
                cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
                decrypted = cipher_rsa.decrypt(base64.b64decode(encrypted_msg))
                print(f"🔓 [2048-BIT PRIVATE KEY İLE ÇÖZÜLDÜ]: {decrypted.decode()}")
                client.send(b"RSA-2048 basariyla cozuldu.")
            except Exception as e:
                print(f"❌ Deşifre Hatası: {e}")
                
        client.close()

if __name__ == '__main__':
    rsa_sunucu_baslat()