import time
from pyModbusTCP.client import ModbusClient

# Docker Compose servis ismini (sensor) host olarak kullanıyoruz
# Docker ağı sayesinde bu isimle birbirlerini bulabilirler
SENSOR_HOST = "host.docker.internal"
SENSOR_PORT = 5020

# Client yapılandırması
client = ModbusClient(host=SENSOR_HOST, port=SENSOR_PORT, auto_open=True, auto_close=True)

def collect_data():
    print("Veri toplayıcı başlatıldı. Ölçüm alınıyor...")
    
    while True:
        # Register 0'dan 1 adet veri oku (Sıcaklık)
        # Sensör veriyi x10 ölçeğinde gönderiyor (22.5 derece -> 225)
        regs = client.read_holding_registers(0, 1)
        
        if regs:
            raw_temp = regs[0]
            actual_temp = raw_temp / 10.0
            print(f"[COLLECTOR] Sunucudan alınan anlamlı veri -> Sıcaklık: {actual_temp}°C")
        else:
            print("[COLLECTOR] Hata: Sensöre bağlanılamadı veya veri okunamadı.")
        
        # Her dakika bir ölçüm (Test için 10 saniyeye de düşürebilirsin)
        print("Bir sonraki ölçüm için 60 saniye bekleniyor...")
        time.sleep(60)

if __name__ == "__main__":
    # Sensörün tam olarak ayağa kalkması için kısa bir süre bekle
    time.sleep(5)
    collect_data()