FROM python:3.9-slim

WORKDIR /app

# AES şifreleme için gerekli kütüphaneyi kuruyoruz
RUN pip install --no-cache-dir pycryptodome

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "server_api.py"]