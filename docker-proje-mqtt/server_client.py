import paho.mqtt.client as mqtt
import time
import os
import random

# Bu dosya 'server_client.py' adıyla kaydedilmelidir.
# Görevi: MQTT Broker'a belirli aralıklarla mesaj göndermek (Publisher).

MQTT_BROKER = os.getenv("MQTT_BROKER", "host.docker.internal")
MQTT_PORT = 1883
TOPIC = "laboratuvar/mesajlar"

def baslat():
    print(f"--- MQTT YAYINCI BASLATILDI (Hedef Broker: {MQTT_BROKER}) ---")
    time.sleep(7) # Broker'ın ayağa kalkması için bekleme süresi
    
    client = mqtt.Client()
    
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            
            # Gönderilecek veri paketi
            mesaj = f"Merhaba Sunucu B! Rastgele Sayı: {random.randint(100, 999)}"
            
            print(f"-> Yayınlanıyor: {mesaj}")
            client.publish(TOPIC, mesaj)
            
            client.disconnect()
        except Exception as e:
            print(f"Broker'a ulasilamadi: {e}")
        
        print("-" * 30)
        time.sleep(5)

if __name__ == '__main__':
    baslat()