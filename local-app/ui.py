import tkinter as tk
from tkinter import messagebox, ttk
from api import login, get_projects, get_tasks, get_tasks_by_project, log_time, create_test_project, create_test_task
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
        self.root.geometry("450x800")  # Increased height to accommodate all sections
        self.root.resizable(True, True)  # Allow resizing so users can adjust if needed
        
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
        self.projects = []
        self.tasks = []
        self.selected_project = None
        self.selected_task = None
        self.task_id = None
        self.start_time = None
        self.screenshot_thread = None
        self.stop_screenshots = False
        self.elapsed_time = 0
        self.timer_running = False
        self.is_logged_in = False
        
        # Create StringVars
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.timer_display = tk.StringVar(value="00:00:00")
        self.projects_var = tk.StringVar()
        self.tasks_var = tk.StringVar()
        
        # Configure styles
        self.configure_styles()
        
        # Create UI
        self.create_ui()
        
        # Start timer update
        self.update_timer_display()

    def configure_styles(self):
        """Configure custom styles for ttk widgets"""
        style = ttk.Style()
        style.configure("Custom.TEntry", padding=10, font=("Arial", 10))
        style.configure("Custom.TCombobox", padding=10, font=("Arial", 10))
    
    def create_custom_button(self, parent, text, command, bg_color, fg_color="white", state=tk.NORMAL):
        """Create a custom styled button with guaranteed color control"""
        button = tk.Button(
            parent,
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
            state=state
        )
        
        # Add hover effects
        def on_enter(e):
            if button['state'] != tk.DISABLED:
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
        
        # Projects and Tasks Selection Section (initially hidden)
        self.create_projects_tasks_section()
        
        # Timer Section (always visible but initially disabled)
        self.create_timer_section()
        
        # Status Section
        self.create_status_section()
        
        # Initially hide sections that should only appear after login
        self.hide_post_login_sections()

    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="⏱️ Time Tracker Pro",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=self.primary_color
        )
        title_label.pack(expand=True)

    def create_login_section(self):
        """Create login form section"""
        # Login container
        self.login_frame = tk.Frame(self.root, bg=self.light_bg)
        self.login_frame.pack(padx=40, pady=20, fill=tk.X)
        
        # Login title
        login_title = tk.Label(
            self.login_frame,
            text="Employee Login",
            font=("Arial", 14, "bold"),
            fg=self.text_color,
            bg=self.light_bg
        )
        login_title.pack(pady=(0, 20))
        
        # Email field
        email_frame = tk.Frame(self.login_frame, bg=self.light_bg)
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            email_frame,
            text="Email Address",
            font=("Arial", 10, "bold"),
            fg=self.text_color,
            bg=self.light_bg
        ).pack(anchor=tk.W)
        
        self.email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            style="Custom.TEntry",
            font=("Arial", 10)
        )
        self.email_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Password field
        password_frame = tk.Frame(self.login_frame, bg=self.light_bg)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            password_frame,
            text="Password",
            font=("Arial", 10, "bold"),
            fg=self.text_color,
            bg=self.light_bg
        ).pack(anchor=tk.W)
        
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            style="Custom.TEntry",
            font=("Arial", 10)
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Login button
        self.login_btn = self.create_custom_button(
            self.login_frame,
            text="Login",
            command=self.do_login,
            bg_color=self.secondary_color,
            fg_color="white"
        )
        self.login_btn.pack(pady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.do_login())

    def create_projects_tasks_section(self):
        """Create projects and tasks selection section"""
        self.projects_tasks_frame = tk.Frame(self.root, bg=self.light_bg)
        # Don't pack initially - will be shown after login
        
        # Projects title
        projects_title = tk.Label(
            self.projects_tasks_frame,
            text="Select Project and Task",
            font=("Arial", 14, "bold"),
            fg=self.text_color,
            bg=self.light_bg
        )
        projects_title.pack(pady=(0, 15))
        
        # Project selection frame
        project_frame = tk.Frame(self.projects_tasks_frame, bg=self.light_bg)
        project_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            project_frame,
            text="Project",
            font=("Arial", 10, "bold"),
            fg=self.text_color,
            bg=self.light_bg
        ).pack(anchor=tk.W)
        
        # Projects dropdown
        self.projects_dropdown = ttk.Combobox(
            project_frame,
            textvariable=self.projects_var,
            state="readonly",
            style="Custom.TCombobox",
            font=("Arial", 10)
        )
        self.projects_dropdown.pack(fill=tk.X, pady=(5, 0))
        self.projects_dropdown.bind('<<ComboboxSelected>>', self.on_project_selected)
        
        # Task selection frame
        task_frame = tk.Frame(self.projects_tasks_frame, bg=self.light_bg)
        task_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            task_frame,
            text="Task",
            font=("Arial", 10, "bold"),
            fg=self.text_color,
            bg=self.light_bg
        ).pack(anchor=tk.W)
        
        # Tasks dropdown
        self.tasks_dropdown = ttk.Combobox(
            task_frame,
            textvariable=self.tasks_var,
            state="readonly",
            style="Custom.TCombobox",
            font=("Arial", 10)
        )
        self.tasks_dropdown.pack(fill=tk.X, pady=(5, 0))
        self.tasks_dropdown.bind('<<ComboboxSelected>>', self.on_task_selected)
        
        # Test data button (only shown after login for development)
        self.test_data_btn = self.create_custom_button(
            self.projects_tasks_frame,
            text="Create Test Data",
            command=self.create_test_data,
            bg_color="#f39c12",
            fg_color="white"
        )
        self.test_data_btn.pack(pady=(15, 0))

    def create_timer_section(self):
        """Create timer section"""
        self.timer_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, bd=1)
        self.timer_frame.pack(padx=40, pady=(0, 20), fill=tk.X)  # Reduced top padding
        
        # Timer display
        timer_display_frame = tk.Frame(self.timer_frame, bg="white")
        timer_display_frame.pack(pady=15)  # Reduced padding
        
        tk.Label(
            timer_display_frame,
            text="Time Elapsed",
            font=("Arial", 11, "bold"),  # Slightly smaller font
            fg=self.text_color,
            bg="white"
        ).pack()
        
        self.timer_label = tk.Label(
            timer_display_frame,
            textvariable=self.timer_display,
            font=("Arial", 20, "bold"),  # Reduced font size
            fg=self.secondary_color,
            bg="white"
        )
        self.timer_label.pack(pady=(5, 0))
        
        # Timer button
        self.timer_btn = self.create_custom_button(
            self.timer_frame,
            text="▶ Start Timer",
            command=self.toggle_timer,
            bg_color=self.success_color,
            fg_color="white",
            state=tk.DISABLED
        )
        self.timer_btn.pack(pady=(0, 15))  # Reduced bottom padding

    def create_status_section(self):
        """Create status section"""
        status_frame = tk.Frame(self.root, bg=self.light_bg)
        status_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)
        
        # Welcome message
        self.welcome_label = tk.Label(
            status_frame,
            text="Please login to start tracking time",
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.light_bg,
            wraplength=350
        )
        self.welcome_label.pack(pady=10)
        
        # Status indicator
        self.status_indicator = tk.Frame(status_frame, height=4, bg="#bdc3c7")
        self.status_indicator.pack(fill=tk.X, pady=10)
        
        # Additional info
        self.info_label = tk.Label(
            status_frame,
            text="Screenshots will be taken every 30 seconds while timer is active",
            font=("Arial", 9),
            fg="#95a5a6",
            bg=self.light_bg,
            wraplength=350
        )
        self.info_label.pack(pady=(20, 0))

    def hide_post_login_sections(self):
        """Hide sections that should only appear after login"""
        self.projects_tasks_frame.pack_forget()
        # Timer section should always be visible, just disabled

    def show_post_login_sections(self):
        """Show sections after successful login"""
        self.projects_tasks_frame.pack(padx=40, pady=(0, 20), fill=tk.X)  # Pack between login and timer
        # Timer section is already packed, just need to enable it when task is selected

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
                self.is_logged_in = True
                
                # Update welcome message
                self.welcome_label.config(
                    text=f"Welcome back, {emp['name']}!\nSelect a project and task to start tracking.",
                    fg=self.success_color
                )
                
                # Hide login form
                self.login_frame.pack_forget()
                
                # Show post-login sections
                self.show_post_login_sections()
                
                # Load projects and tasks
                self.load_projects_and_tasks()
                
            else:
                messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")
                self.login_btn.config(state=tk.NORMAL, text="Login", bg=self.secondary_color)
                
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {str(e)}")
            self.login_btn.config(state=tk.NORMAL, text="Login", bg=self.secondary_color)

    def load_projects_and_tasks(self):
        """Load projects and tasks from the API"""
        try:
            print("Loading projects...")
            projects = get_projects()
            print(f"Fetched projects: {projects}")
            
            if projects:
                self.projects = projects
                project_names = [f"{p['name']} (ID: {p['id']})" for p in projects]
                self.projects_dropdown['values'] = project_names
                self.projects_dropdown.set("Select a project...")
                
                # Clear tasks dropdown
                self.tasks_dropdown['values'] = []
                self.tasks_dropdown.set("Select a project first...")
                self.tasks = []
                self.selected_project = None
                self.selected_task = None
                self.task_id = None
                
                # Disable timer until task is selected
                self.timer_btn.config(state=tk.DISABLED, bg="#95a5a6")
                
            else:
                messagebox.showinfo("No Projects", "No projects available. You can create test data to get started.")
                self.projects_dropdown['values'] = ["No projects available"]
                self.projects_dropdown.set("No projects available")
                
        except Exception as e:
            print(f"Error loading projects: {e}")
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")

    def on_project_selected(self, event):
        """Handle project selection and load tasks"""
        try:
            selected = self.projects_var.get()
            print(f"Project selected: {selected}")
            
            if selected and selected != "Select a project..." and selected != "No projects available":
                # Extract project ID from selection - format is "Name (ID: X)"
                project_id = int(selected.split("(ID: ")[1].rstrip(")"))
                self.selected_project = next((p for p in self.projects if p['id'] == project_id), None)
                
                print(f"Selected project: {self.selected_project}")
                
                if self.selected_project:
                    # Reset task selection
                    self.selected_task = None
                    self.task_id = None
                    self.timer_btn.config(state=tk.DISABLED, bg="#95a5a6")
                    
                    # Fetch tasks for selected project
                    self.tasks_dropdown.set("Loading tasks...")
                    self.root.update()
                    
                    tasks = get_tasks_by_project(project_id)
                    print(f"Fetched tasks: {tasks}")
                    
                    if tasks:
                        self.tasks = tasks
                        task_names = [f"{t['name']} (ID: {t['id']})" for t in tasks]
                        self.tasks_dropdown['values'] = task_names
                        self.tasks_dropdown.set("Select a task...")
                        
                        print(f"Task names: {task_names}")
                    else:
                        self.tasks_dropdown['values'] = ["No tasks available"]
                        self.tasks_dropdown.set("No tasks available")
                        self.tasks = []
                        
        except Exception as e:
            print(f"Error in project selection: {e}")
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            self.tasks_dropdown.set("Error loading tasks")

    def on_task_selected(self, event):
        """Handle task selection and enable timer"""
        try:
            selected = self.tasks_var.get()
            print(f"Task selected: {selected}")
            
            if selected and selected not in ["Select a task...", "No tasks available", "Select a project first...", "Loading tasks...", "Error loading tasks"]:
                # Extract task ID from selection - format is "Name (ID: X)"
                task_id = int(selected.split("(ID: ")[1].rstrip(")"))
                self.selected_task = next((t for t in self.tasks if t['id'] == task_id), None)
                
                print(f"Selected task: {self.selected_task}")
                
                if self.selected_task:
                    self.task_id = task_id
                    
                    # Enable timer button
                    self.timer_btn.config(state=tk.NORMAL, bg=self.success_color)
                    self.status_indicator.config(bg=self.success_color)
                    
                    print(f"Timer button enabled. Task ID: {self.task_id}")
                    
                    # Update welcome message
                    self.welcome_label.config(
                        text=f"Ready to track time!\nProject: {self.selected_project['name']}\nTask: {self.selected_task['name']}",
                        fg=self.success_color
                    )
                    
        except Exception as e:
            print(f"Error in task selection: {e}")
            messagebox.showerror("Error", f"Failed to select task: {str(e)}")

    def toggle_timer(self):
        """Toggle timer start/stop"""
        print(f"Toggle timer called. Timer running: {self.timer_running}")
        print(f"Selected task: {self.selected_task}")
        print(f"Task ID: {self.task_id}")
        
        if not self.selected_task or not self.task_id:
            messagebox.showwarning("No Task Selected", "Please select a project and task first.")
            return
            
        if not self.timer_running:
            print("Starting timer...")
            self.start_timer()
        else:
            print("Stopping timer...")
            self.stop_timer()

    def start_timer(self):
        """Start the timer"""
        print(f"Start timer called. Selected task: {self.selected_task}")
        
        if not self.selected_task or not self.task_id:
            messagebox.showwarning("No Task Selected", "Please select a project and task first.")
            return
            
        self.start_time = datetime.datetime.utcnow()
        self.timer_running = True
        self.elapsed_time = 0
        
        print(f"Timer started at: {self.start_time}")
        
        # Update UI
        self.timer_btn.config(text="⏹ Stop Timer", bg=self.danger_color)
        self.projects_dropdown.config(state="disabled")
        self.tasks_dropdown.config(state="disabled")
        
        self.welcome_label.config(
            text=f"Timer is running!\nProject: {self.selected_project['name']}\nTask: {self.selected_task['name']}\n\nScreenshots are being captured automatically every 30 seconds.",
            fg=self.secondary_color
        )
        self.status_indicator.config(bg=self.secondary_color)
        
        # Start periodic screenshots
        self.stop_screenshots = False
        self.screenshot_thread = threading.Thread(target=self.take_periodic_screenshots)
        self.screenshot_thread.daemon = True
        self.screenshot_thread.start()

    def stop_timer(self):
        """Stop the timer"""
        if not self.start_time or not self.timer_running:
            return
            
        # Stop screenshots first
        self.stop_screenshots = True
        self.timer_running = False
        
        # Calculate time
        end_time = datetime.datetime.utcnow()
        elapsed_seconds = (end_time - self.start_time).total_seconds()
        
        try:
            # Log time with selected task
            ip = get_ip()
            mac = get_mac()
            log_time(self.employee['id'], self.task_id, self.start_time.isoformat(), end_time.isoformat(), ip, mac)
            
            # Take final screenshot
            image_b64 = take_screenshot()
            upload_screenshot(self.employee['id'], image_b64, permission_flag=True)
            
            # Format elapsed time for display
            hours = int(elapsed_seconds // 3600)
            minutes = int((elapsed_seconds % 3600) // 60)
            seconds = int(elapsed_seconds % 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Reset timer state
            self.start_time = None
            self.timer_display.set("00:00:00")
            
            # Update UI
            self.timer_btn.config(text="▶ Start Timer", bg=self.success_color)
            self.projects_dropdown.config(state="readonly")
            self.tasks_dropdown.config(state="readonly")
            
            self.welcome_label.config(
                text=f"Time logged successfully!\nTotal time: {time_str}\nProject: {self.selected_project['name']}\nTask: {self.selected_task['name']}",
                fg=self.success_color
            )
            self.status_indicator.config(bg=self.success_color)
            
            messagebox.showinfo("Success", f"Time has been logged successfully!\n\nTotal time tracked: {time_str}")
            
        except Exception as e:
            print(f"Error logging time: {e}")
            messagebox.showerror("Error", f"Failed to log time: {str(e)}")
            
            # Reset UI even if logging failed
            self.start_time = None
            self.timer_display.set("00:00:00")
            self.timer_running = False
            self.timer_btn.config(text="▶ Start Timer", bg=self.success_color)
            self.projects_dropdown.config(state="readonly")
            self.tasks_dropdown.config(state="readonly")

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
        next_screenshot_time = time.time() + screenshot_interval
        
        while not self.stop_screenshots and self.timer_running:
            current_time = time.time()
            if current_time >= next_screenshot_time:
                try:
                    print(f"Taking screenshot at {datetime.datetime.now()}")
                    image_b64 = take_screenshot()
                    upload_screenshot(self.employee['id'], image_b64, permission_flag=True)
                    print("Screenshot uploaded successfully")
                    next_screenshot_time = current_time + screenshot_interval
                except Exception as e:
                    print(f"Error taking screenshot: {e}")
                    next_screenshot_time = current_time + screenshot_interval
            
            # Sleep for a short time to avoid busy waiting
            time.sleep(1)

    def create_test_data(self):
        """Create test projects and tasks for development"""
        if not self.is_logged_in:
            messagebox.showwarning("Not Logged In", "Please login first before creating test data.")
            return
            
        try:
            print("Creating test data...")
            
            # Create test project
            project = create_test_project("Test Project - " + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            if project:
                print(f"Created project: {project}")
                
                # Create test task
                task = create_test_task("Test Task - " + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), project['id'])
                if task:
                    print(f"Created task: {task}")
                    messagebox.showinfo("Success", "Test data created successfully!\nRefreshing project list...")
                    
                    # Refresh the projects list
                    self.load_projects_and_tasks()
                else:
                    messagebox.showerror("Error", "Failed to create test task")
            else:
                messagebox.showerror("Error", "Failed to create test project")
                
        except Exception as e:
            print(f"Error creating test data: {e}")
            messagebox.showerror("Error", f"Failed to create test data: {str(e)}")
