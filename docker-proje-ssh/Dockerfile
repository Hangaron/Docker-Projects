FROM python:3.9-slim

WORKDIR /app

# Telnet ve Socket işlemleri Python'ın standart kütüphanesinde olduğu için 
# harici bir pip install (paramiko gibi) yapmamıza gerek kalmadı.
# Bu imajı daha hafif ve hızlı hale getirir.

COPY . .

ENV PYTHONUNBUFFERED=1

# Varsayılan başlangıç komutu
CMD ["python", "server_api.py"]