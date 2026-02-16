import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# Bu dosya 'server_api.py' adıyla kaydedilmelidir.
# Görevi: AES ile şifrelenmiş veriyi almak ve çözmek (Decryption).

# Ortak Anahtar (16 byte - AES-128 için şarttır)
SHARED_KEY = b'1234567890123456'

def decrypt_message(encrypted_data):
    try:
        # Base64 formatından geri çevir
        raw_data = base64.b64decode(encrypted_data)
        
        # İlk 16 byte IV (Initialization Vector)
        iv = raw_data[:16]
        payload = raw_data[16:]
        
        # Şifre çözücü oluştur
        cipher = AES.new(SHARED_KEY, AES.MODE_CBC, iv)
        
        # Şifreyi çöz ve padding'i (dolgu) kaldır
        decrypted = unpad(cipher.decrypt(payload), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"Sifre Cozme Hatasi: {e}"

def aes_sunucu_baslat():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    
    print("--- AES-128 DINLEME MODU AKTIF: Port 5555 ---")
    print(f"Kullanilan Anahtar: {SHARED_KEY.decode()}")
    
    while True:
        client, addr = server.accept()
        data = client.recv(1024)
        if data:
            encrypted_msg = data.decode()
            print(f"\n📡 [AGDAN GELEN HAM VERI]: {encrypted_msg}")
            
            # Veriyi deşifre et
            original_msg = decrypt_message(encrypted_msg)
            print(f"🔓 [SIFRESI COZULMUS MESAJ]: {original_msg}")
            
            client.send(b"Mesaj alindi ve cozuldu.")
        client.close()

if __name__ == '__main__':
    aes_sunucu_baslat()