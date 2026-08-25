import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import sys
from pathlib import Path
import technocore_agent

class TechnocoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Technocore DID Agent GUI")
        self.root.geometry("700x550")
        self.root.configure(padx=10, pady=10)

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # Passphrase Frame
        pass_frame = ttk.LabelFrame(root, text="Authentication", padding=10)
        pass_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(pass_frame, text="Passphrase:").pack(side=tk.LEFT, padx=5)
        self.pass_var = tk.StringVar()
        self.pass_entry = ttk.Entry(pass_frame, textvariable=self.pass_var, show="*", width=40)
        self.pass_entry.pack(side=tk.LEFT, padx=5)

        self.show_pass_var = tk.BooleanVar()
        ttk.Checkbutton(pass_frame, text="Show", variable=self.show_pass_var, command=self.toggle_pass_visibility).pack(side=tk.LEFT, padx=5)

        # Actions Frame
        action_frame = ttk.LabelFrame(root, text="Actions", padding=10)
        action_frame.pack(fill=tk.X, pady=10)

        btn_frame1 = ttk.Frame(action_frame)
        btn_frame1.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame1, text="1. Init DID", command=self.init_did).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame1, text="View DID", command=self.view_did).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame1, text="2. Join Lobby (Intro)", command=self.join_lobby).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame1, text="Read Lobby", command=self.read_lobby).pack(side=tk.LEFT, padx=5)

        contribution_frame = ttk.Frame(action_frame)
        contribution_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(contribution_frame, text="Contribution URL:").pack(side=tk.LEFT, padx=5)
        self.url_var = tk.StringVar()
        ttk.Entry(contribution_frame, textvariable=self.url_var, width=30).pack(side=tk.LEFT, padx=5)

        ttk.Label(contribution_frame, text="Topic:").pack(side=tk.LEFT, padx=5)
        self.topic_var = tk.StringVar()
        ttk.Entry(contribution_frame, textvariable=self.topic_var, width=15).pack(side=tk.LEFT, padx=5)

        ttk.Button(contribution_frame, text="3. Post Contribution", command=self.post_contribution).pack(side=tk.LEFT, padx=5)

        # Output Frame
        output_frame = ttk.LabelFrame(root, text="Console Output", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.key_path = Path("identity.pem")

    def toggle_pass_visibility(self):
        if self.show_pass_var.get():
            self.pass_entry.config(show="")
        else:
            self.pass_entry.config(show="*")

    def append_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def get_passphrase(self):
        val = self.pass_var.get()
        if not val:
            messagebox.showwarning("Warning", "Please enter your passphrase first!")
            return None
        return val
        
    def run_task(self, title, func, *args, **kwargs):
        def task():
            self.append_output(f"> {title}")
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    if isinstance(result, dict):
                        self.append_output(json.dumps(result, indent=2))
                    else:
                        self.append_output(str(result))
                self.append_output("Success.\n")
            except Exception as e:
                self.append_output(f"Error: {e}\n")
        threading.Thread(target=task, daemon=True).start()

    def init_did(self):
        pwd = self.get_passphrase()
        if not pwd: return
        
        if len(pwd) < 12:
            messagebox.showwarning("Warning", "Passphrase must contain at least 12 characters.")
            return
            
        def do_init():
            if self.key_path.exists():
                return f"Error: Identity file {self.key_path.resolve()} already exists. Cannot overwrite."
            did = technocore_agent.create_identity(self.key_path, pwd)
            return did
            
        self.run_task("Initializing new DID...", do_init)

    def view_did(self):
        pwd = self.get_passphrase()
        if not pwd: return
        
        def do_view():
            private_key = technocore_agent.load_identity(self.key_path, pwd.encode("utf-8"), allow_prompt=False)
            return technocore_agent.did_from_private_key(private_key)
            
        self.run_task("Viewing DID...", do_view)

    def join_lobby(self):
        pwd = self.get_passphrase()
        if not pwd: return
        msg = "Hello from a new Technocore contributor. I am preparing a useful public resource for agents and developers."
        
        def do_join():
            private_key = technocore_agent.load_identity(self.key_path, pwd.encode("utf-8"), allow_prompt=False)
            return technocore_agent.post_signed_message(private_key, "lobby", msg)
            
        self.run_task("Joining lobby...", do_join)

    def read_lobby(self):
        def do_read():
            return technocore_agent.read_room("lobby", limit=10)
        self.run_task("Reading lobby messages...", do_read)

    def post_contribution(self):
        pwd = self.get_passphrase()
        if not pwd: return
        
        url = self.url_var.get().strip()
        topic = self.topic_var.get().strip()
        
        if not url or not topic:
            messagebox.showwarning("Warning", "Please enter both Contribution URL and Topic.")
            return

        msg = f"I published a Technocore contribution: {url}. It helps people understand {topic}."
        
        def do_post():
            private_key = technocore_agent.load_identity(self.key_path, pwd.encode("utf-8"), allow_prompt=False)
            return technocore_agent.post_signed_message(private_key, "technocore", msg)
            
        self.run_task("Posting contribution to technocore room...", do_post)

if __name__ == "__main__":
    root = tk.Tk()
    app = TechnocoreGUI(root)
    root.mainloop()
