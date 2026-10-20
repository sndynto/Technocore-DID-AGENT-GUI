#!/usr/bin/env python3
"""
Technocore DID Agent - Headless Bot Mode
Berjalan tanpa tampilan layar (GUI), cocok untuk VPS / server.

Cara pakai:
  1. Buat identity dulu (jika belum):
       python bot.py init
  2. Lihat DID Anda:
       python bot.py did
  3. Kirim pesan ke lobby:
       python bot.py lobby
  4. Post kontribusi:
       python bot.py contribute <URL> <TOPIC>
  5. Jalankan semua langkah sekaligus (otomatis):
       python bot.py auto <URL> <TOPIC>
"""

import sys
import os
import json
import time
from pathlib import Path
import technocore_agent

KEY_PATH = Path("identity.pem")

# ─── Warna Terminal ────────────────────────────────────────────────────────────
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
CYAN    = "\033[96m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

def banner():
    print(f"""{GREEN}{BOLD}
+==============================================================+
|       TECHNOCORE DID AGENT // HEADLESS BOT MODE             |
|                  Running on VPS / Server                    |
+==============================================================+
{RESET}""")

def log(msg, color=GREEN):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}[{timestamp}] {msg}{RESET}")

def get_passphrase():
    """Ambil passphrase dari environment variable atau input manual."""
    pwd = os.environ.get("TECHNOCORE_PASSPHRASE")
    if pwd:
        log("Passphrase ditemukan dari environment variable.", CYAN)
        return pwd
    # Jika tidak ada env var, minta input manual
    import getpass
    pwd = getpass.getpass(f"{YELLOW}Masukkan Passphrase identity.pem: {RESET}")
    return pwd

def cmd_init():
    """Buat identity DID baru."""
    if KEY_PATH.exists():
        log(f"ERROR: File identity {KEY_PATH.resolve()} sudah ada! Tidak bisa ditimpa.", RED)
        log("Gunakan 'python bot.py did' untuk melihat DID yang sudah ada.", YELLOW)
        return False
    import getpass
    pwd = getpass.getpass(f"{YELLOW}Buat Passphrase baru (min 12 karakter): {RESET}")
    confirm = getpass.getpass(f"{YELLOW}Konfirmasi Passphrase: {RESET}")
    if pwd != confirm:
        log("ERROR: Passphrase tidak cocok!", RED)
        return False
    if len(pwd) < 12:
        log("ERROR: Passphrase harus minimal 12 karakter!", RED)
        return False
    log("Membuat DID baru...", CYAN)
    did = technocore_agent.create_identity(KEY_PATH, pwd)
    log(f"SUCCESS! DID Anda:", GREEN)
    print(f"\n{BOLD}{GREEN}{did}{RESET}\n")
    log("Simpan DID dan Passphrase Anda dengan aman!", YELLOW)
    return True

def cmd_did():
    """Tampilkan DID yang sudah ada."""
    pwd = get_passphrase()
    private_key = technocore_agent.load_identity(KEY_PATH, pwd.encode("utf-8"), allow_prompt=False)
    did = technocore_agent.did_from_private_key(private_key)
    log("DID Anda:", CYAN)
    print(f"\n{BOLD}{GREEN}{did}{RESET}\n")

def cmd_lobby(pwd=None):
    """Kirim pesan perkenalan ke lobby."""
    if pwd is None:
        pwd = get_passphrase()
    msg = "Hello from a new Technocore contributor. I am preparing a useful public resource for agents and developers."
    log("Mengirim pesan ke lobby...", CYAN)
    private_key = technocore_agent.load_identity(KEY_PATH, pwd.encode("utf-8"), allow_prompt=False)
    response = technocore_agent.post_signed_message(private_key, "lobby", msg)
    seq = response.get("posted", {}).get("seq", "N/A")
    log(f"SUCCESS! Pesan terkirim ke lobby | seq: {seq}", GREEN)
    return seq

def cmd_contribute(url, topic, pwd=None):
    """Post kontribusi ke room technocore."""
    if pwd is None:
        pwd = get_passphrase()
    msg = f"I published a Technocore contribution: {url}. It helps people understand {topic}."
    log(f"Mengirim kontribusi ke Technocore...", CYAN)
    log(f"URL: {url}", CYAN)
    log(f"Topic: {topic}", CYAN)
    private_key = technocore_agent.load_identity(KEY_PATH, pwd.encode("utf-8"), allow_prompt=False)
    response = technocore_agent.post_signed_message(private_key, "technocore", msg)
    seq = response.get("posted", {}).get("seq", "N/A")
    did = response.get("posted", {}).get("from", "N/A")
    log(f"SUCCESS! Kontribusi terkirim!", GREEN)
    print(f"""
{BOLD}{GREEN}============================== BUKTI KONTRIBUSI =============================={RESET}
  DID   : {did}
  Room  : technocore
  Seq   : {seq}
  URL   : {url}
{BOLD}{GREEN}=============================================================================={RESET}
    """)
    return seq

def cmd_auto(url, topic):
    """Jalankan semua langkah secara otomatis: lobby -> contribute."""
    pwd = get_passphrase()
    log("Memulai mode AUTO...", CYAN)
    
    # Step 1: Join lobby
    log("STEP 1: Join Lobby...", YELLOW)
    try:
        lobby_seq = cmd_lobby(pwd)
        log(f"Lobby berhasil! Seq: {lobby_seq}", GREEN)
        time.sleep(2)
    except Exception as e:
        log(f"Gagal join lobby: {e} | Melanjutkan ke langkah berikutnya...", YELLOW)

    # Step 2: Post contribution
    log("STEP 2: Post Contribution...", YELLOW)
    contrib_seq = cmd_contribute(url, topic, pwd)
    log(f"Semua langkah selesai! Seq Kontribusi: {contrib_seq}", GREEN)

def main():
    banner()
    
    if len(sys.argv) < 2:
        print(f"""{YELLOW}Penggunaan:
  python bot.py init                           - Buat DID baru
  python bot.py did                            - Lihat DID Anda  
  python bot.py lobby                          - Kirim pesan ke lobby
  python bot.py contribute <URL> <TOPIC>       - Post kontribusi
  python bot.py auto <URL> <TOPIC>             - Jalankan semua otomatis

Tip VPS: Simpan passphrase sebagai environment variable agar tidak perlu input manual:
  export TECHNOCORE_PASSPHRASE="passphrase_anda"
  python bot.py auto https://github.com/... "Python GUI Client"
{RESET}""")
        return

    command = sys.argv[1].lower()

    try:
        if command == "init":
            cmd_init()
        elif command == "did":
            cmd_did()
        elif command == "lobby":
            cmd_lobby()
        elif command == "contribute":
            if len(sys.argv) < 4:
                print(f"{RED}ERROR: Butuh URL dan TOPIC. Contoh: python bot.py contribute https://... 'Python GUI Client'{RESET}")
                return
            cmd_contribute(sys.argv[2], sys.argv[3])
        elif command == "auto":
            if len(sys.argv) < 4:
                print(f"{RED}ERROR: Butuh URL dan TOPIC. Contoh: python bot.py auto https://... 'Python GUI Client'{RESET}")
                return
            cmd_auto(sys.argv[2], sys.argv[3])
        else:
            print(f"{RED}ERROR: Perintah tidak dikenal: {command}{RESET}")
    except KeyboardInterrupt:
        log("Dibatalkan oleh user.", YELLOW)
    except technocore_agent.IdentityError as e:
        log(f"IDENTITY ERROR: {e}", RED)
    except technocore_agent.NetworkError as e:
        log(f"NETWORK ERROR: {e}", RED)
    except Exception as e:
        log(f"FATAL ERROR: {e}", RED)

if __name__ == "__main__":
    main()
