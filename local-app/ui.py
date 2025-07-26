import tkinter as tk
from tkinter import messagebox, ttk
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
        self.root.title("Time Tracker Pro")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        
        # Configure colors and styles
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        self.light_bg = "#ecf0f1"
        self.text_color = "#2c3e50"
        
        # Configure root background
        self.root.configure(bg=self.light_bg)
        
        # Initialize variables
        self.employee = None
        self.task_id = None
        self.start_time = None
        self.screenshot_thread = None
        self.stop_screenshots = False
        self.elapsed_time = 0
        self.timer_running = False
        
        # Create StringVars
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.timer_display = tk.StringVar(value="00:00:00")
        
        # Configure styles
        self.configure_styles()
        
        # Create UI
        self.create_ui()
        
        # Start timer update
        self.update_timer_display()

    def configure_styles(self):
        """Configure custom styles for ttk widgets"""
        style = ttk.Style()
        
        # Configure entry styles (TTK entries work well)
        style.configure("Custom.TEntry",
                       padding=10,
                       font=("Arial", 10))
    
    def create_custom_button(self, parent, text, command, bg_color, fg_color="white", state=tk.NORMAL):
        """Create a custom styled button with guaranteed color control"""
        button = tk.Button(parent,
                          text=text,
                          command=command,
                          bg=bg_color,
                          fg=fg_color,
                          font=("Arial", 10, "bold"),
                          relief=tk.FLAT,
                          bd=0,
                          padx=20,
                          pady=10,
                          cursor="hand2",
                          state=state)
        
        # Add hover effects
        def on_enter(e):
            if button['state'] != tk.DISABLED:
                # Darken the color on hover
                darker_color = self.darken_color(bg_color)
                button.config(bg=darker_color)
        
        def on_leave(e):
            if button['state'] != tk.DISABLED:
                button.config(bg=bg_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def darken_color(self, hex_color, factor=0.8):
        """Darken a hex color by a factor"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(c * factor) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darker_rgb)

    def create_ui(self):
        """Create the main UI layout"""
        # Header
        self.create_header()
        
        # Login Section
        self.create_login_section()
        
        # Timer Section
        self.create_timer_section()
        
        # Status Section
        self.create_status_section()

    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="⏱️ Time Tracker Pro",
                              font=("Arial", 18, "bold"),
                              fg="white",
                              bg=self.primary_color)
        title_label.pack(expand=True)

    def create_login_section(self):
        """Create login form section"""
        # Login container
        self.login_frame = tk.Frame(self.root, bg=self.light_bg)
        self.login_frame.pack(padx=40, pady=20, fill=tk.X)
        
        # Login title
        login_title = tk.Label(self.login_frame,
                              text="Employee Login",
                              font=("Arial", 14, "bold"),
                              fg=self.text_color,
                              bg=self.light_bg)
        login_title.pack(pady=(0, 20))
        
        # Email field
        email_frame = tk.Frame(self.login_frame, bg=self.light_bg)
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(email_frame,
                text="Email Address",
                font=("Arial", 10, "bold"),
                fg=self.text_color,
                bg=self.light_bg).pack(anchor=tk.W)
        
        self.email_entry = ttk.Entry(email_frame,
                                    textvariable=self.email_var,
                                    style="Custom.TEntry",
                                    font=("Arial", 10))
        self.email_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Password field
        password_frame = tk.Frame(self.login_frame, bg=self.light_bg)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(password_frame,
                text="Password",
                font=("Arial", 10, "bold"),
                fg=self.text_color,
                bg=self.light_bg).pack(anchor=tk.W)
        
        self.password_entry = ttk.Entry(password_frame,
                                       textvariable=self.password_var,
                                       show="*",
                                       style="Custom.TEntry",
                                       font=("Arial", 10))
        self.password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Login button
        self.login_btn = self.create_custom_button(self.login_frame,
                                                  text="Login",
                                                  command=self.do_login,
                                                  bg_color=self.secondary_color,
                                                  fg_color="white")
        self.login_btn.pack(pady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.do_login())

    def create_timer_section(self):
        """Create timer section"""
        self.timer_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, bd=1)
        self.timer_frame.pack(padx=40, pady=20, fill=tk.X)
        
        # Timer display
        timer_display_frame = tk.Frame(self.timer_frame, bg="white")
        timer_display_frame.pack(pady=20)
        
        tk.Label(timer_display_frame,
                text="Time Elapsed",
                font=("Arial", 12, "bold"),
                fg=self.text_color,
                bg="white").pack()
        
        self.timer_label = tk.Label(timer_display_frame,
                                   textvariable=self.timer_display,
                                   font=("Arial", 24, "bold"),
                                   fg=self.secondary_color,
                                   bg="white")
        self.timer_label.pack(pady=(5, 0))
        
        # Timer button
        self.timer_btn = self.create_custom_button(self.timer_frame,
                                                  text="▶ Start Timer",
                                                  command=self.toggle_timer,
                                                  bg_color=self.success_color,
                                                  fg_color="white",
                                                  state=tk.DISABLED)
        self.timer_btn.pack(pady=(0, 20))

    def create_status_section(self):
        """Create status section"""
        status_frame = tk.Frame(self.root, bg=self.light_bg)
        status_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)
        
        # Welcome message
        self.welcome_label = tk.Label(status_frame,
                                     text="Please login to start tracking time",
                                     font=("Arial", 12),
                                     fg=self.text_color,
                                     bg=self.light_bg,
                                     wraplength=350)
        self.welcome_label.pack(pady=10)
        
        # Status indicator
        self.status_indicator = tk.Frame(status_frame, height=4, bg="#bdc3c7")
        self.status_indicator.pack(fill=tk.X, pady=10)
        
        # Additional info
        self.info_label = tk.Label(status_frame,
                                  text="Screenshots will be taken every 30 seconds while timer is active",
                                  font=("Arial", 9),
                                  fg="#95a5a6",
                                  bg=self.light_bg,
                                  wraplength=350)
        self.info_label.pack(pady=(20, 0))

    def do_login(self):
        """Handle login process"""
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password")
            return
        
        # Disable login button during authentication
        self.login_btn.config(state=tk.DISABLED, text="Logging in...", bg="#95a5a6")
        self.root.update()
        
        try:
            emp = login(email, password)
            if emp:
                self.employee = emp
                self.welcome_label.config(text=f"Welcome back, {emp['name']}!\nYou can now start tracking your time.",
                                        fg=self.success_color)
                self.timer_btn.config(state=tk.NORMAL, bg=self.success_color)
                self.status_indicator.config(bg=self.success_color)
                
                # Hide login form after successful login
                self.login_frame.pack_forget()
                
            else:
                messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")
                self.login_btn.config(state=tk.NORMAL, text="Login", bg=self.secondary_color)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {str(e)}")
            self.login_btn.config(state=tk.NORMAL, text="Login", bg=self.secondary_color)

    def toggle_timer(self):
        """Toggle timer start/stop"""
        if self.start_time is None:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        """Start the timer"""
        self.start_time = datetime.datetime.utcnow()
        self.timer_running = True
        self.elapsed_time = 0
        
        # Update UI
        self.timer_btn.config(text="⏹ Stop Timer", bg=self.danger_color)
        self.welcome_label.config(text=f"Timer is running for {self.employee['name']}\nScreenshots are being captured automatically",
                                 fg=self.secondary_color)
        self.status_indicator.config(bg=self.secondary_color)
        
        # Start periodic screenshots
        self.stop_screenshots = False
        self.screenshot_thread = threading.Thread(target=self.take_periodic_screenshots)
        self.screenshot_thread.daemon = True
        self.screenshot_thread.start()

    def stop_timer(self):
        """Stop the timer"""
        if not self.start_time:
            return
            
        # Stop screenshots
        self.stop_screenshots = True
        self.timer_running = False
        
        # Calculate time
        end_time = datetime.datetime.utcnow()
        
        try:
            # Log time
            ip = get_ip()
            mac = get_mac()
            log_time(self.employee['id'], 1, self.start_time.isoformat(), end_time.isoformat(), ip, mac)
            
            # Take final screenshot
            image_b64 = take_screenshot()
            upload_screenshot(self.employee['id'], image_b64, permission_flag=True)
            
            # Update UI
            self.start_time = None
            self.timer_btn.config(text="▶ Start Timer", bg=self.success_color)
            self.welcome_label.config(text=f"Time logged successfully!\nTotal time: {self.timer_display.get()}",
                                     fg=self.success_color)
            self.status_indicator.config(bg=self.success_color)
            
            messagebox.showinfo("Success", "Time has been logged successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log time: {str(e)}")
            # Reset UI even if logging failed
            self.start_time = None
            self.timer_btn.config(text="▶ Start Timer", bg=self.success_color)
            self.timer_running = False

    def update_timer_display(self):
        """Update the timer display every second"""
        if self.timer_running and self.start_time:
            current_time = datetime.datetime.utcnow()
            elapsed = current_time - self.start_time
            
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            seconds = int(elapsed.total_seconds() % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_display.set(time_str)
        
        # Schedule next update
        self.root.after(1000, self.update_timer_display)

    def take_periodic_screenshots(self):
        """Take screenshots every 30 seconds while timer is running"""
        screenshot_interval = 30  # 30 seconds
        
        while not self.stop_screenshots:
            time.sleep(screenshot_interval)
            if not self.stop_screenshots:
                try:
                    image_b64 = take_screenshot()
                    upload_screenshot(self.employee['id'], image_b64, permission_flag=True)
                    print(f"Screenshot taken at {datetime.datetime.now()}")
                except Exception as e:
                    print(f"Error taking screenshot: {e}")


