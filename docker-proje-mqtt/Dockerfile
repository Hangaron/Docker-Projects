FROM python:3.9-slim

WORKDIR /app

# MQTT iletişimi için gerekli paho-mqtt kütüphanesini kuruyoruz
RUN pip install --no-cache-dir paho-mqtt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "server_api.py"]