#!/usr/bin/env python3

import os
import sys
import subprocess
import re
import base64
import platform
from urllib.parse import urlparse, parse_qs
import random
import json

class SkipBot:
    def __init__(self):
        self.os_info = self.detect_platform()
        self.setup_env()
        self.try_setup_deps()
        
        self.db = {
            'bit.ly': 'follow', 'tinyurl.com': 'follow', 'ow.ly': 'follow', 'is.gd': 'follow',
            'tpi.li': 'base64', 'oii.la': 'base64', 'oii.io': 'base64', 'tii.la': 'base64',
            'oei.la': 'base64', 'iir.la': 'base64', 'tvi.la': 'base64', 'lnbz.la': 'base64',
            'insfly.pw': 'query', 'freecrypto.top': 'query', 'freeltc.top': 'query',
            'ay.live': 'query', 'linksfly.link': 'query', 'revly.click': 'query',
            'shortox.com': 'query', 'timeforearn.com': 'query', 'urlstox.com': 'query',
            'lollty.com': 'query', 'adnews.me': 'query', 'terafly.me': 'query',
            'adf.ly': 'follow', 'adfly.io': 'follow', 'linkvertise.com': 'follow',
            'blogmystt.com': 'follow', 'cety.app': 'follow', 'fc-lc.xyz': 'follow',
            'gamezizo.com': 'follow', 'forex-trnd.com': 'follow', 'v.gd': 'follow',
            'tiny.cc': 'follow', 'buff.ly': 'follow', 'goo.gl': 'follow', 'short.cm': 'follow',
            'bc.vc': 'follow', 'cl.ly': 'follow', 'short.link': 'follow', 'link.ax': 'follow',
            'shortened.me': 'follow', 'tly.click': 'follow', 'rebrandly.com': 'follow',
            'bl.ink': 'follow', 'short.io': 'follow', 'dub.co': 'follow', 't2m.io': 'follow',
            'replug.io': 'follow', 'sniply.com': 'follow', 'branch.io': 'follow',
            'falpus.com': 'follow', 'wp2hostt.com': 'follow', 'expertvn.com': 'follow',
            'top10cafe.se': 'follow', 'mitly.us': 'follow', 'autodime.com': 'follow',
            'linx.cc': 'follow', 'surflink.tech': 'follow', 'coincroco.com': 'follow',
            'sox.link': 'follow', 'themezon.net': 'follow', 'tmail.io': 'follow',
            'linksly.co': 'follow', 'fx4ever.com': 'follow', 'fx-22.com': 'follow',
            'gold-24.net': 'follow', 'forexrw7.com': 'follow', 'linkjust.com': 'follow',
            'carewave.xyz': 'follow', 'pubprofit.in': 'follow', 'worldnewsestate.com': 'follow',
            'sabarpratham.in': 'follow', 'tlin.me': 'follow', 'bioinflu.com': 'follow',
            'cryptosparatodos.com': 'follow', 'tfly.link': 'follow', 'solarchaine.com': 'follow',
            'sclick.crazyblog.in': 'follow', 'ser7.crazyblog.in': 'follow',
        }
        self.requests = None
        self.urllib3 = None
    
    def detect_platform(self):
        info = {
            'os': platform.system(),
            'platform': '',
            'distro': '',
        }
        
        if os.path.exists('/data/data/com.termux'):
            info['platform'] = 'termux'
        elif info['os'] == 'Linux':
            info['platform'] = 'linux'
            try:
                with open('/etc/os-release') as f:
                    for line in f:
                        if line.startswith('ID='):
                            info['distro'] = line.split('=')[1].strip().strip('"')
                            break
            except:
                info['distro'] = 'unknown'
        elif info['os'] == 'Windows':
            info['platform'] = 'windows'
        elif info['os'] == 'Darwin':
            info['platform'] = 'macos'
        
        return info
    
    def setup_env(self):
        if self.os_info['platform'] == 'termux':
            os.environ['TERMUX_MODE'] = '1'
        elif self.os_info['platform'] == 'windows':
            os.environ['WINDOWS_MODE'] = '1'
    
    def try_setup_deps(self):
        if self.os_info['platform'] == 'termux':
            self.setup_termux()
        elif self.os_info['platform'] == 'windows':
            self.setup_windows()
        else:
            self.setup_linux()
    
    def setup_termux(self):
        print("[*] Termux detected - minimal setup")
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            print("[*] Installing requests...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'requests'])
                import requests
                self.requests = requests
            except:
                print("[-] requests failed, using fallback")
    
    def setup_linux(self):
        print("[*] Linux detected - full setup")
        
        # Install curl jika ada
        if subprocess.run(['which', 'curl'], capture_output=True).returncode != 0:
            distro = self.os_info['distro']
            if distro in ['ubuntu', 'debian']:
                print("[*] Installing curl...")
                subprocess.run(['sudo', 'apt', 'install', '-y', 'curl'], 
                             capture_output=True)
            elif distro in ['fedora', 'rhel', 'centos']:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'curl'], 
                             capture_output=True)
            elif distro == 'arch':
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'curl'], 
                             capture_output=True)
        
        # Try requests
        try:
            import requests
            self.requests = requests
        except ImportError:
            print("[*] Installing requests...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'requests'])
            import requests
            self.requests = requests
    
    def setup_windows(self):
        print("[*] Windows detected - Windows mode")
        
        # Cek curl built-in Windows
        curl_available = subprocess.run(['where', 'curl'], 
                                       capture_output=True).returncode == 0
        
        if not curl_available:
            print("[!] curl recommended: https://curl.se/download.html")
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            print("[*] Installing requests...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'requests'])
            import requests
            self.requests = requests
        
        # Try urllib3 untuk Windows
        try:
            import urllib3
            self.urllib3 = urllib3
        except ImportError:
            pass
    
    def bypass_curl(self, url):
        try:
            result = subprocess.run(
                ['curl', '-sL', '-w', '%{redirect_url}', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout:
                final = result.stdout.strip()
                if final.startswith('http'):
                    return final
        except:
            pass
        return None
    
    def bypass_requests(self, url):
        if not self.requests:
            return None
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' if self.os_info['platform'] == 'windows' 
                             else 'Mozilla/5.0 (Linux; Android 11)',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            r = self.requests.head(url, allow_redirects=True, timeout=10, headers=headers)
            return r.url
        except:
            pass
        return None
    
    def bypass_follow(self, url):
        # Platform-specific order
        if self.os_info['platform'] == 'windows':
            result = self.bypass_requests(url)
            if result:
                return result
            result = self.bypass_curl(url)
            if result:
                return result
        else:
            result = self.bypass_curl(url)
            if result:
                return result
            result = self.bypass_requests(url)
            if result:
                return result
        
        return f"[!] Failed: {url}"
    
    def bypass_base64(self, url):
        try:
            if self.os_info['platform'] == 'windows':
                if self.requests:
                    r = self.requests.get(url, timeout=10)
                    html = r.text
                else:
                    html = subprocess.run(['curl', '-s', url], 
                                        capture_output=True, text=True).stdout
            else:
                html = subprocess.run(['curl', '-s', url], 
                                    capture_output=True, text=True).stdout
            
            matches = re.findall(r'aHR0c[^"&<>]{50,}', html)
            for match in matches:
                try:
                    decoded = base64.b64decode(match).decode('utf-8')
                    if decoded.startswith('http'):
                        return decoded
                except:
                    pass
            
            return self.bypass_follow(url)
        except Exception as e:
            return f"Error: {e}"
    
    def bypass_query(self, url):
        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for key in ['url', 'link', 'target', 'goto', 'redirect', 'r', 'dest']:
                if key in params and params[key]:
                    found = params[key][0]
                    if found.startswith('http'):
                        return found
            
            return self.bypass_follow(url)
        except:
            return self.bypass_follow(url)
    
    def get_method(self, url):
        try:
            domain = urlparse(url).netloc.replace('www.', '')
            for service, method in self.db.items():
                if service in domain:
                    return method
        except:
            pass
        return 'follow'
    
    def skip(self, url):
        method = self.get_method(url)
        
        if method == 'base64':
            return self.bypass_base64(url)
        elif method == 'query':
            return self.bypass_query(url)
        else:
            return self.bypass_follow(url)
    
    def copy(self, text):
        try:
            if self.os_info['platform'] == 'termux':
                subprocess.run(['termux-clipboard-set'], input=text.encode(), check=True)
                return True
            elif self.os_info['platform'] == 'windows':
                subprocess.run(['clip'], input=text.encode(), check=True)
                return True
            elif self.os_info['platform'] == 'macos':
                subprocess.run(['pbcopy'], input=text.encode(), check=True)
                return True
            else:
                subprocess.run(['xclip', '-selection', 'clipboard'], 
                             input=text.encode(), check=True)
                return True
        except:
            return False
    
    def clear_screen(self):
        os.system('cls' if self.os_info['platform'] == 'windows' else 'clear')
    
    def get_title(self):
        titles = {
            'termux': 'Skip Bot • Termux',
            'windows': 'Skip Bot • Windows',
            'linux': f'Skip Bot • {self.os_info["distro"].capitalize()}',
            'macos': 'Skip Bot • macOS',
        }
        return titles.get(self.os_info['platform'], 'Skip Bot')
    
    def menu(self):
        while True:
            self.clear_screen()
            title = self.get_title()
            print(f"\n  {title}")
            print("  " + "─" * (len(title)-2))
            print("\n  [1] Skip")
            print("  [2] Database")
            print("  [3] Batch")
            print("  [0] Exit\n")
            
            c = input("  > ").strip()
            
            if c == '1':
                self.single()
            elif c == '2':
                self.view_db()
            elif c == '3':
                self.batch()
            elif c == '0':
                print("\n  [+] Bye!\n")
                sys.exit(0)
    
    def single(self):
        self.clear_screen()
        print(f"\n  {self.get_title()}\n")
        url = input("  Paste: ").strip()
        
        if not url:
            print("  [-] Empty")
            input("  Press Enter...")
            return
        
        print("\n  [*] Processing...")
        result = self.skip(url)
        
        print(f"\n  [+] Result:\n  {result}\n")
        
        if self.copy(result):
            print("  [+] Copied!\n")
        
        input("  Press Enter...")
    
    def view_db(self):
        self.clear_screen()
        print(f"\n  Database ({len(self.db)} services)\n")
        for i, (service, method) in enumerate(self.db.items(), 1):
            if i % 2 == 0:
                print(f"    {service:30}")
            else:
                print(f"    {service:30}", end=" ")
        print()
        input("\n  Press Enter...")
    
    def batch(self):
        self.clear_screen()
        print(f"\n  {self.get_title()} • Batch\n")
        print("  Enter URLs (empty line to finish):\n")
        
        urls = []
        while True:
            url = input("  > ").strip()
            if not url:
                if urls:
                    break
            else:
                urls.append(url)
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"  [{i}/{len(urls)}] Processing...", end='\r')
            result = self.skip(url)
            results.append(f"{url}\n  → {result}")
        
        output = "\n".join(results)
        print("\n" + "─" * 50)
        print(output)
        print("─" * 50)
        
        if self.copy(output):
            print("\n  [+] Copied!\n")
        
        input("  Press Enter...")

def main():
    try:
        bot = SkipBot()
        bot.menu()
    except KeyboardInterrupt:
        print("\n  [!] Interrupted\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
