# Her iki servis için ortak kullanılabilecek Dockerfile
FROM python:3.9-slim

# Python loglarının anlık olarak terminale düşmesini sağlar
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları kopyala
COPY . .

# Çalıştırma komutu docker-compose'da ezilecek
CMD ["python"]