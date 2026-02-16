# 🐳 Docker Security & Protocol Laboratory

Bu depo, modern şifreleme algoritmalarının (AES, RSA, ECC) ve endüstriyel/ağ protokollerinin (MQTT, Modbus, SSH, Telnet) Docker konteynerleri içerisinde izole edilmiş uygulamalarını içerir. 

## 🚀 Proje İçeriği

### 🔐 Şifreleme Algoritmaları (Cryptography)
* **AES (Advanced Encryption Standard):** 128, 192 ve 256-bit anahtar uzunluklarıyla simetrik şifreleme uygulamaları.
* **RSA (Rivest-Shamir-Adleman):** 1024, 2048 ve 4096-bit uzunluklarında asimetrik şifreleme ve anahtar üretimi.
* **ECC (Elliptic Curve Cryptography):** Modern ve düşük kaynak tüketen eliptik eğri şifreleme modülleri.

### 📡 Protokoller ve Ağ Servisleri
* **MQTT:** IoT cihazları için hafif mesajlaşma kuyruğu uygulaması.
* **Modbus:** Endüstriyel otomasyon sistemleri için veri iletim simülasyonu.
* **SSH & Telnet:** Güvenli ve güvensiz uzak bağlantı protokollerinin Dockerize edilmiş versiyonları.
* **Sıcaklık Projesi:** Docker üzerinde çalışan sensör verisi işleme simülasyonu.

## 🛠 Kurulum ve Çalıştırma

Tüm projeler Docker ve Docker Compose ile uyumludur. Herhangi bir modülü çalıştırmak için ilgili klasöre gidip şu komutu kullanabilirsiniz:

```bash
cd docker-proje-rsa4096
docker-compose up --build
