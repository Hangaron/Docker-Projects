import socket
import threading

# Bu dosya 'server_api.py' adıyla kaydedilmelidir.
# Görevi: Telnet üzerinden gelen bağlantıları kabul etmek.

def handle_client(client_socket):
    try:
        # Telnet protokolünde basit bir karşılama mesajı
        # Türkçe karakterler (ı, ş, ğ, ü, ö, ç) byte dizilerinde kullanılmamalıdır.
        client_socket.send(b"Kullanici Adi: ")
        username = client_socket.recv(1024).decode().strip()
        
        client_socket.send(b"Sifre: ")
        password = client_socket.recv(1024).decode().strip()
        
        print(f"📡 [TELNET GIRISI] Deneme -> Kullanici: {username}, Sifre: {password}")
        
        if username == "admin" and password == "secret123":
            client_socket.send(b"Giris Basarili! Komut Bekleniyor...\n> ")
            command = client_socket.recv(1024).decode().strip()
            print(f"📡 [TELNET KOMUTU] Yakalandi: {command}")
            
            if command == "merhaba_sunucu_b":
                client_socket.send(b"Merhaba Sunucu A! Telnet ile guvenli olmayan baglanti kuruldu.\n")
        else:
            # HATA DÜZELTİLDİ: "Hatalı" yerine "Hatali" yazıldı.
            client_socket.send(b"Hatali Giris!\n")
            
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        client_socket.close()

def telnet_calistir():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 2323))
    server.listen(5)
    
    print("--- TELNET SUNUCUSU AKTIF: Port 2323 Dinleniyor ---")
    
    while True:
        client, addr = server.accept()
        print(f"\n[YENI BAGLANTI] {addr[0]} adresinden Telnet istegi geldi.")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == '__main__':
    telnet_calistir()