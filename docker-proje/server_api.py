from flask import Flask, jsonify, request

app = Flask(__name__)

@app.before_request
def log_request():
    # Gelen her isteği terminalde detaylıca gösterir
    print(f"\n[TRAFİK YAKALANDI] {request.method} -> {request.path}")

@app.route('/')
def home():
    return jsonify({
        "durum": "basarili",
        "mesaj": "Merhaba Sunucu A! Iletisim hatti kuruldu."
    })

if __name__ == '__main__':
    # 0.0.0.0, Docker konteynerinin dış dünyadan erişim kabul etmesini sağlar
    app.run(host='0.0.0.0', port=5000)