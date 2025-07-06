import psutil
import time
import tkinter as tk
import threading
import win32gui
import win32con
import win32api

class SpeedMeterApp:
    def __init__(self):
        self.last_upload = 0
        self.last_download = 0
        self.last_time = 0
        self.running = True
        self.show_upload = True
        self.show_download = True
        self.update_interval = 1  # seconds
        # New variable to track position
        self.last_valid_position = None

        # Create main window
        self.root = tk.Tk()
        self.root.title("Network Speed Meter")
        
        # Window styling to match taskbar
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        self.root.attributes('-transparentcolor', '#2D2D2D')  # Match your bg color
        self.root.configure(bg='#2D2D2D')  # Dark gray similar to taskbar
        
        # Create speed display label
        self.speed_label = tk.Label(
            self.root,
            text="↓ 0.0 KB/s\n↑ 0.0 KB/s",
            fg='white',
            bg=self.root.cget('bg'),
            font=('Segoe UI', 9),
            padx=0,
            pady=0
        )
        self.speed_label.pack()

        # Right-click menu
        self.create_context_menu()
        
        # Initial positioning
        self.position_window()
        
        # Start monitoring
        self.start_monitoring()
        
        # Start periodic position refresh
        self.root.after(1000, self.refresh_position)
        
        # Main loop
        self.root.mainloop()

    def create_context_menu(self):
        """Create right-click context menu"""
        self.menu = tk.Menu(self.root, tearoff=0, bg='#2D2D2D', fg='white')
        self.menu.add_command(label="Exit", command=self.exit_app)
        self.root.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        """Show context menu on right-click"""
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def find_taskbar_apps(self):
        """Find existing taskbar apps and return their leftmost position"""
        try:
            # Get taskbar handle
            h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            if not h_taskbar:
                return None
                
            # Find the tray toolbar containing apps
            h_tray_toolbar = None
            h_child = win32gui.GetWindow(h_taskbar, win32con.GW_CHILD)
            while h_child:
                class_name = win32gui.GetClassName(h_child)
                if class_name == "TrayToolbarWindow32":
                    h_tray_toolbar = h_child
                    break
                h_child = win32gui.GetWindow(h_child, win32con.GW_HWNDNEXT)
                
            if not h_tray_toolbar:
                return None
                
            # Get position of the first taskbar app
            rect = win32gui.GetWindowRect(h_tray_toolbar)
            return rect[0]  # Left edge of apps area
            
        except Exception as e:
            print(f"Error finding taskbar apps: {e}")
            return None

    def position_window(self):
        """Position window to the left of other taskbar widgets"""
        try:
            self.root.update_idletasks()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # Get taskbar info
            h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            if not h_taskbar:
                self.position_fallback()
                return
                
            taskbar_rect = win32gui.GetWindowRect(h_taskbar)
            taskbar_height = taskbar_rect[3] - taskbar_rect[1]
            
            # Find where widgets start
            widgets_start = self.find_taskbar_widgets_area()
            
            if widgets_start:
                # Position to the left of widgets with 0px gap
                margin = 0
                x = widgets_start - window_width - margin
                self.last_valid_position = (x, taskbar_rect[1] + (taskbar_height - window_height) // 2)
            else:
                # Fallback to right of system tray
                h_systray = win32gui.FindWindowEx(h_taskbar, 0, "TrayNotifyWnd", None)
                if h_systray:
                    systray_rect = win32gui.GetWindowRect(h_systray)
                    x = systray_rect[0] - window_width - margin
                    self.last_valid_position = (x, taskbar_rect[1] + (taskbar_height - window_height) // 2)
                else:
                    self.position_fallback()
                    return
            
            # Adjust for different taskbar positions
            screen_width = win32api.GetSystemMetrics(0)
            if taskbar_rect[1] > 0:  # Taskbar at top
                self.last_valid_position = (self.last_valid_position[0], taskbar_rect[3] - window_height - 2)
            elif taskbar_rect[0] > 0 and taskbar_rect[2] < screen_width // 2:  # Left
                self.last_valid_position = (taskbar_rect[2] + 2, taskbar_rect[3] - window_height - 2)
            elif taskbar_rect[2] == screen_width:  # Right
                self.last_valid_position = (taskbar_rect[0] - window_width - 2, taskbar_rect[3] - window_height - 2)
            
            self.root.geometry(f"+{self.last_valid_position[0]}+{self.last_valid_position[1]}")
            
            # Ensure proper z-order
            self.root.after(100, lambda: [
                self.root.lift(),
                self.root.attributes('-topmost', True)
            ])
            
        except Exception as e:
            print(f"Positioning error: {e}")
            self.position_fallback()

    def position_fallback(self):
        """Fallback positioning using last known good position or default"""
        self.root.update_idletasks()
        if self.last_valid_position:
            self.root.geometry(f"+{self.last_valid_position[0]}+{self.last_valid_position[1]}")
        else:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            x = screen_width - window_width - 100
            y = screen_height - window_height - 40
            self.root.geometry(f"+{x}+{y}")

    def refresh_position(self):
        """Periodically refresh window position"""
        if self.running:
            self.position_window()
            self.root.after(5000, self.refresh_position)

    def start_monitoring(self):
        """Start network monitoring thread"""
        self.monitor_thread = threading.Thread(target=self.monitor_network)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def monitor_network(self):
        """Monitor network speeds"""
        while self.running:
            net_io = psutil.net_io_counters()
            current_time = time.time()

            if self.last_time > 0:
                time_elapsed = current_time - self.last_time
                if time_elapsed > 0:
                    upload_speed = (net_io.bytes_sent - self.last_upload) / time_elapsed
                    download_speed = (net_io.bytes_recv - self.last_download) / time_elapsed
                    self.update_display(download_speed, upload_speed)

            self.last_upload = net_io.bytes_sent
            self.last_download = net_io.bytes_recv
            self.last_time = current_time
            time.sleep(self.update_interval)

    def update_display(self, download_speed, upload_speed):
        """Update the speed display"""
        def format_speed(speed):
            if speed < 1024:
                return "0.0 B/s"
            elif speed < 1024 * 1024:
                return f"{speed/1024:.1f} KB/s"
            else:
                return f"{speed/(1024*1024):.1f} MB/s"

        download_text = f"↓ {format_speed(download_speed)}" if self.show_download else ""
        upload_text = f"↑ {format_speed(upload_speed)}" if self.show_upload else ""
        separator = "\n" if self.show_download and self.show_upload else ""
        text = f"{download_text}{separator}{upload_text}"

        self.speed_label.config(text=text)
        self.position_window()

    def exit_app(self):
        """Clean exit"""
        self.running = False
        self.root.quit()
        self.root.destroy()
        
    def find_taskbar_widgets_area(self):
        """Find the area where taskbar widgets are located"""
        try:
            h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            if not h_taskbar:
                return None
                
            # Find the Widgets window (Windows 11)
            h_widgets = win32gui.FindWindow("Windows.UI.Core.CoreWindow", "Widgets")
            if h_widgets:
                widgets_rect = win32gui.GetWindowRect(h_widgets)
                return widgets_rect[0]  # Return left edge of widgets area
                
            # For Windows 10 or when Widgets window isn't found
            h_rebar = win32gui.FindWindowEx(h_taskbar, 0, "ReBarWindow32", None)
            if not h_rebar:
                return None
                
            # Find the MSTaskSwWClass (task items)
            h_tasklist = win32gui.FindWindowEx(h_rebar, 0, "MSTaskSwWClass", None)
            if not h_tasklist:
                return None
                
            # Find the right edge of the task items
            tasklist_rect = win32gui.GetWindowRect(h_tasklist)
            return tasklist_rect[2]  # Right edge of task items
            
        except Exception as e:
            print(f"Error finding widgets area: {e}")
            return None

if __name__ == "__main__":
    app = SpeedMeterApp()