import random
import time
import threading
from pyModbusTCP.server import ModbusServer

# Modbus Sunucu Ayarları
# Docker içerisinde 502 portu standarttır
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 502

# Sunucuyu başlat
server = ModbusServer(host=SERVER_HOST, port=SERVER_PORT, no_block=True)

def update_sensor_data():
    """
    Sürekli rastgele sıcaklık verisi üretir ve Modbus register'ına yazar.
    Modbus genellikle tamsayı (integer) tutar. 
    22.5 dereceyi 225 olarak kaydedeceğiz (x10 scaling).
    """
    print("Sıcaklık simülasyonu başlatıldı...")
    while True:
        # 20.0 ile 30.0 arasında rastgele bir sıcaklık
        temp = round(random.uniform(20.0, 30.0), 1)
        scaled_temp = int(temp * 10)
        
        # Holding Register 0'a yaz (Sıcaklık verisi)
        server.data_bank.set_holding_registers(0, [scaled_temp])
        
        print(f"[SENSOR] Yeni sıcaklık üretildi: {temp}°C (Register: {scaled_temp})")
        time.sleep(10) # 10 saniyede bir güncelle (izlemesi kolay olsun diye)

if __name__ == "__main__":
    try:
        server.start()
        print(f"Modbus Server {SERVER_HOST}:{SERVER_PORT} üzerinde çalışıyor.")
        
        # Veri güncelleme işlemini ayrı bir thread'de başlat
        data_thread = threading.Thread(target=update_sensor_data, daemon=True)
        data_thread.start()
        
        # Ana thread'i canlı tut
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Hata: {e}")
        server.stop()