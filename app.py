import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import json
import time
import random
from pathlib import Path
import technocore_agent

# Hacker Color Palette
BG_COLOR = "#050505"
FG_COLOR = "#00FF41"
FONT = ("Consolas", 10, "bold")
TITLE_FONT = ("Consolas", 12, "bold")

class HackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TECHNOCORE // SECURE AGENT TERMINAL")
        self.root.geometry("800x650")
        self.root.configure(bg=BG_COLOR, padx=15, pady=15)
        
        # Authentication Frame
        pass_frame = tk.LabelFrame(root, text=" [ AUTHENTICATION PROTOCOL ] ", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT, bd=2)
        pass_frame.pack(fill=tk.X, pady=(0, 15), ipady=5)

        tk.Label(pass_frame, text="> PASSPHRASE:", bg=BG_COLOR, fg=FG_COLOR, font=FONT).pack(side=tk.LEFT, padx=10)
        self.pass_var = tk.StringVar()
        self.pass_entry = tk.Entry(pass_frame, textvariable=self.pass_var, show="*", width=35, bg="#111", fg=FG_COLOR, font=FONT, insertbackground=FG_COLOR)
        self.pass_entry.pack(side=tk.LEFT, padx=10)

        self.show_pass_var = tk.BooleanVar()
        tk.Checkbutton(pass_frame, text="DECRYPT VIEW", variable=self.show_pass_var, command=self.toggle_pass_visibility, 
                       bg=BG_COLOR, fg=FG_COLOR, font=FONT, selectcolor="#111", activebackground=BG_COLOR, activeforeground=FG_COLOR).pack(side=tk.LEFT, padx=10)

        # Actions Frame
        action_frame = tk.LabelFrame(root, text=" [ COMMAND EXECUTION ] ", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT, bd=2)
        action_frame.pack(fill=tk.X, pady=10, ipady=5)

        # Buttons Helper
        def h_btn(parent, text, cmd):
            btn = tk.Button(parent, text=text, command=cmd, bg="#111", fg=FG_COLOR, font=FONT, activebackground=FG_COLOR, activeforeground=BG_COLOR, relief=tk.RAISED, bd=2)
            btn.pack(side=tk.LEFT, padx=8, pady=5)
            return btn

        btn_frame1 = tk.Frame(action_frame, bg=BG_COLOR)
        btn_frame1.pack(fill=tk.X, pady=5)
        
        h_btn(btn_frame1, "1. INIT_DID()", self.init_did)
        h_btn(btn_frame1, "VIEW_DID()", self.view_did)
        h_btn(btn_frame1, "2. INFILTRATE_LOBBY()", self.join_lobby)
        h_btn(btn_frame1, "INTERCEPT_LOBBY()", self.read_lobby)

        contribution_frame = tk.Frame(action_frame, bg=BG_COLOR)
        contribution_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(contribution_frame, text="> TARGET URL:", bg=BG_COLOR, fg=FG_COLOR, font=FONT).pack(side=tk.LEFT, padx=5)
        self.url_var = tk.StringVar()
        tk.Entry(contribution_frame, textvariable=self.url_var, width=25, bg="#111", fg=FG_COLOR, font=FONT, insertbackground=FG_COLOR).pack(side=tk.LEFT, padx=5)

        tk.Label(contribution_frame, text="> TOPIC:", bg=BG_COLOR, fg=FG_COLOR, font=FONT).pack(side=tk.LEFT, padx=5)
        self.topic_var = tk.StringVar()
        tk.Entry(contribution_frame, textvariable=self.topic_var, width=15, bg="#111", fg=FG_COLOR, font=FONT, insertbackground=FG_COLOR).pack(side=tk.LEFT, padx=5)

        h_btn(contribution_frame, "3. DEPLOY_PAYLOAD()", self.post_contribution)

        # Terminal Output Frame
        output_frame = tk.LabelFrame(root, text=" [ TERMINAL OUTPUT ] ", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT, bd=2)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=15)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=15, bg="#0A0A0A", fg=FG_COLOR, font=("Consolas", 11), insertbackground=FG_COLOR)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.key_path = Path("identity.pem")
        
        self.append_output("SYSTEM INITIALIZED. AWAITING COMMANDS...\n")

    def toggle_pass_visibility(self):
        if self.show_pass_var.get():
            self.pass_entry.config(show="")
        else:
            self.pass_entry.config(show="*")

    def append_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def hacking_animation(self):
        chars = "0123456789!@#$%^&*()_+-=[]{}|;:,.<>/?ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.append_output("> BYPASSING SECURITY MAINFRAME...")
        for _ in range(3):
            line = "".join(random.choice(chars) for _ in range(60))
            self.output_text.insert(tk.END, line + "\n")
            self.output_text.see(tk.END)
            self.root.update()
            time.sleep(0.1)
        self.output_text.insert(tk.END, "[ ACCESS GRANTED ]\n\n")
        self.output_text.see(tk.END)

    def get_passphrase(self):
        val = self.pass_var.get()
        if not val:
            messagebox.showwarning("WARNING", "ACCESS DENIED. PASSPHRASE REQUIRED.")
            return None
        return val
        
    def run_task(self, title, func, *args, **kwargs):
        def task():
            self.hacking_animation()
            self.append_output(f"> EXECUTING: {title}")
            time.sleep(0.5)
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    if isinstance(result, dict):
                        self.append_output(json.dumps(result, indent=2))
                    else:
                        self.append_output(str(result))
                self.append_output("\n[ OPERATION SUCCESSFUL ]\n")
            except Exception as e:
                self.append_output(f"\n[ FATAL ERROR ]: {e}\n")
        threading.Thread(target=task, daemon=True).start()

    def init_did(self):
        pwd = self.get_passphrase()
        if not pwd: return
        
        if len(pwd) < 12:
            messagebox.showwarning("WARNING", "PASSPHRASE TOO WEAK. MIN 12 CHARS.")
            return
            
        def do_init():
            if self.key_path.exists():
                return f"ERROR: SECURE KEY {self.key_path.resolve()} ALREADY EXISTS."
            did = technocore_agent.create_identity(self.key_path, pwd)
            return did
            
        self.run_task("INIT_DID", do_init)

    def view_did(self):
        pwd = self.get_passphrase()
        if not pwd: return
        
        def do_view():
            private_key = technocore_agent.load_identity(self.key_path, pwd.encode("utf-8"), allow_prompt=False)
            return technocore_agent.did_from_private_key(private_key)
            
        self.run_task("EXTRACT_DID", do_view)

    def join_lobby(self):
        pwd = self.get_passphrase()
        if not pwd: return
        msg = "Hello from a new Technocore contributor. I am preparing a useful public resource for agents and developers."
        
        def do_join():
            private_key = technocore_agent.load_identity(self.key_path, pwd.encode("utf-8"), allow_prompt=False)
            return technocore_agent.post_signed_message(private_key, "lobby", msg)
            
        self.run_task("INFILTRATE_LOBBY", do_join)

    def read_lobby(self):
        def do_read():
            return technocore_agent.read_room("lobby", limit=10)
        self.run_task("INTERCEPT_COMMS", do_read)

    def post_contribution(self):
        pwd = self.get_passphrase()
        if not pwd: return
        
        url = self.url_var.get().strip()
        topic = self.topic_var.get().strip()
        
        if not url or not topic:
            messagebox.showwarning("WARNING", "TARGET URL AND TOPIC REQUIRED FOR DEPLOYMENT.")
            return

        msg = f"I published a Technocore contribution: {url}. It helps people understand {topic}."
        
        def do_post():
            private_key = technocore_agent.load_identity(self.key_path, pwd.encode("utf-8"), allow_prompt=False)
            return technocore_agent.post_signed_message(private_key, "technocore", msg)
            
        self.run_task("DEPLOY_PAYLOAD", do_post)

if __name__ == "__main__":
    root = tk.Tk()
    app = HackerGUI(root)
    root.mainloop()
