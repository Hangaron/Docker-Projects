import paho.mqtt.client as mqtt
import os

# Bu dosya 'server_api.py' adıyla kaydedilmelidir.
# Görevi: MQTT Broker'a bağlanıp mesajları dinlemek (Subscriber).

# Ayarlar
MQTT_BROKER = os.getenv("MQTT_BROKER", "host.docker.internal")
MQTT_PORT = 1883
TOPIC = "laboratuvar/mesajlar"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Broker'a bağlandı: {MQTT_BROKER}")
        # Mesajların geleceği konuya (topic) abone ol
        client.subscribe(TOPIC)
        print(f"📡 {TOPIC} konusu dinleniyor...")
    else:
        print(f"❌ Bağlantı hatası, kod: {rc}")

def on_message(client, userdata, msg):
    # Gelen mesajı yakalayıp ekrana basar
    gelen_veri = msg.payload.decode()
    print(f"📩 [MQTT TRAFİĞİ YAKALANDI] Konu: {msg.topic} | Mesaj: {gelen_veri}")

def mqtt_baslat():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        # Dinleme döngüsünü başlat
        client.loop_forever()
    except Exception as e:
        print(f"Bağlantı kurulamadı: {e}")

if __name__ == '__main__':
    mqtt_baslat()