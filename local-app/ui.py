import tkinter as tk
from tkinter import messagebox
from api import login, get_projects, log_time
from background import get_ip, get_mac
from screenshot import take_screenshot
from api import upload_screenshot
import datetime
import threading
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        self.employee = None
        self.task_id = None
        self.start_time = None
        self.screenshot_thread = None
        self.stop_screenshots = False

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(root, text="Email:").pack()
        tk.Entry(root, textvariable=self.email_var).pack()
        tk.Label(root, text="Password:").pack()
        tk.Entry(root, textvariable=self.password_var, show="*").pack()
        tk.Button(root, text="Login", command=self.do_login).pack()

        self.status = tk.Label(root, text="")
        self.status.pack()

        self.timer_btn = tk.Button(root, text="Start", command=self.toggle_timer, state=tk.DISABLED)
        self.timer_btn.pack()

    def do_login(self):
        email = self.email_var.get()
        password = self.password_var.get()
        emp = login(email, password)
        if emp:
            self.employee = emp
            self.status.config(text=f"Welcome, {emp['name']}")
            self.timer_btn.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    
    def toggle_timer(self):
        if self.start_time is None:
            # Start timer
            self.start_time = datetime.datetime.utcnow().isoformat()
            self.timer_btn.config(text="Stop")
            self.status.config(text="Timer started")
            
            # Start periodic screenshots
            self.stop_screenshots = False
            self.screenshot_thread = threading.Thread(target=self.take_periodic_screenshots)
            self.screenshot_thread.daemon = True
            self.screenshot_thread.start()
            
        else:
            # Stop timer
            self.stop_screenshots = True  # Stop screenshot thread
            end_time = datetime.datetime.utcnow().isoformat()
            ip = get_ip()
            mac = get_mac()
            log_time(self.employee['id'], 1, self.start_time, end_time, ip, mac)
            
            # Take final screenshot
            image_b64 = take_screenshot()
            upload_screenshot(self.employee['id'], image_b64, permission_flag=True)
            
            self.start_time = None
            self.timer_btn.config(text="Start")
            self.status.config(text="Timer stopped, time and screenshots logged")

    def take_periodic_screenshots(self):
        """Take screenshots every 5 minutes while timer is running"""
        screenshot_interval = 30  # 5 minutes in seconds
        
        while not self.stop_screenshots:
            time.sleep(screenshot_interval)
            if not self.stop_screenshots:  # Check again after sleep
                try:
                    image_b64 = take_screenshot()
                    upload_screenshot(self.employee['id'], image_b64, permission_flag=True)
                    print(f"Screenshot taken at {datetime.datetime.now()}")
                except Exception as e:
                    print(f"Error taking screenshot: {e}")


