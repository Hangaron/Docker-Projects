import telnetlib
import time
import os

# Bu dosya 'server_client.py' adıyla kaydedilmelidir.
# Görevi: Telnet üzerinden Sunucu B'ye bağlanıp bilgileri açık metin göndermek.

# Wireshark için trafiği dışarı zorluyoruz
TELNET_HOST = os.getenv("TELNET_HOST", "host.docker.internal")
TELNET_PORT = 2323

def baslat():
    print(f"--- TELNET ISTEMCISI BASLATILDI (Hedef: {TELNET_HOST}) ---")
    time.sleep(5)
    
    while True:
        try:
            print(f"-> {TELNET_HOST} adresine Telnet ile baglaniliyor...")
            tn = telnetlib.Telnet(TELNET_HOST, TELNET_PORT, timeout=10)
            
            # Kullanıcı adı girişi
            tn.read_until(b"Kullanici Adi: ")
            tn.write(b"admin\n")
            
            # Şifre girişi (Ağda açıkça görünecek!)
            tn.read_until(b"Sifre: ")
            tn.write(b"secret123\n")
            
            # Komut gönderimi
            tn.write(b"merhaba_sunucu_b\n")
            
            # Yanıtı oku
            response = tn.read_all().decode('ascii')
            print(f"-> Telnet Yaniti: {response.strip()}")
            
            tn.close()
        except Exception as e:
            print(f"Baglanti Hatasi: {e}")
        
        print("-" * 30)
        time.sleep(5)

if __name__ == '__main__':
    baslat()