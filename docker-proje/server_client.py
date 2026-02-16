mport requests
import time
import os
import random

# Trafiği Windows Wireshark'ın görebileceği 'host.docker.internal' adresine yönlendiriyoruz
API_URL = os.getenv("API_URL", "http://host.docker.internal:5000")

def baslat():
    print(f"--- ISTEMCI CALISIYOR (Hedef: {API_URL}) ---")
    time.sleep(5) 
    
    while True:
        try:
            print("-> GET isteği gönderiliyor...")
            res = requests.get(API_URL, timeout=5)
            print(f"-> Gelen Cevap: {res.json().get('mesaj')}")

            print("-> POST veri paketi gönderiliyor...")
            test_data = {"sensor_id": 1, "deger": random.randint(1, 100)}
            post_res = requests.post(f"{API_URL}/veri-gonder", json=test_data)
            print(f"-> Sunucu B Onayı: {post_res.json().get('durum')}")

        except Exception as e:
            print(f"Baglanti Hatası: Sunucu B'ye ulasilamadi.")
        
        print("-" * 30)
        time.sleep(5)

if __name__ == '__main__':
    baslat()