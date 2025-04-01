from tkinter import *
from tkinter import messagebox
import sys
import os
import time
import queue
import multiprocessing as mp
import configparser
import json

# Default settings (used if no config file exists)
DEFAULT_SERVER_URL = "https://rwk2.racewarkingdoms.com/"
DEFAULT_USE_DEFAULT_PROFILE = 0
DEFAULT_NUM_GAME_WINDOWS = 4
DEFAULT_IGNORE_KEYS = {
    "Surzerker": ["c"],
    "Spongebob": ["a"]
}
DEFAULT_KEY_REBINDINGS = {}

# Current version of this script
VERSION = "1.4.3"

# GitHub raw URL for the latest version
GITHUB_URL = "https://raw.githubusercontent.com/surzerker/rwkmulti/main/rwkmulti-latest.pyw"

# Config file path
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "rwkmulti_settings.cfg")

# Check for required libraries
missing_libs = []
try:
    import requests
except ImportError:
    missing_libs.append("requests")
try:
    import selenium.webdriver as webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
except ImportError:
    missing_libs.append("selenium")
try:
    import keyboard
except ImportError:
    missing_libs.append("keyboard")

if missing_libs:
    error_msg = "The following required libraries are missing:\n\n"
    error_msg += "\n".join(f"- {lib}" for lib in missing_libs)
    error_msg += "\n\nPlease install them by running these commands in your terminal:\n"
    error_msg += "\n".join(f"pip3 install {lib}" for lib in missing_libs)
    error_msg += "\n\nAfter installing, restart the script."
    messagebox.showerror("Missing Dependencies", error_msg)
    sys.exit(1)

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        server_url = config.get("Settings", "server_url", fallback=DEFAULT_SERVER_URL)
        use_default_profile = config.getint("Settings", "use_default_profile", fallback=DEFAULT_USE_DEFAULT_PROFILE)
        num_game_windows = config.getint("Settings", "num_game_windows", fallback=DEFAULT_NUM_GAME_WINDOWS)
        ignore_keys = json.loads(config.get("Settings", "ignore_keys", fallback=json.dumps(DEFAULT_IGNORE_KEYS)))
        key_rebindings = json.loads(config.get("Settings", "key_rebindings", fallback=json.dumps(DEFAULT_KEY_REBINDINGS)))
    else:
        server_url = DEFAULT_SERVER_URL
        use_default_profile = DEFAULT_USE_DEFAULT_PROFILE
        num_game_windows = DEFAULT_NUM_GAME_WINDOWS
        ignore_keys = DEFAULT_IGNORE_KEYS
        key_rebindings = DEFAULT_KEY_REBINDINGS
        save_config(server_url, use_default_profile, num_game_windows, ignore_keys, key_rebindings)
    return server_url, use_default_profile, num_game_windows, ignore_keys, key_rebindings

def save_config(server_url, use_default_profile, num_game_windows, ignore_keys, key_rebindings):
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case in keys
    config["Settings"] = {
        "# Server URL to connect to": "",
        "server_url": server_url,
        "# Use default Firefox profile (0 = no, 1 = yes)": "",
        "use_default_profile": str(use_default_profile),
        "# Number of game windows to open": "",
        "num_game_windows": str(num_game_windows),
        "# Ignore keys by window title pattern (JSON format, e.g., {\"Pattern\": [\"key1\", \"key2\"]})": "",
        "ignore_keys": json.dumps(ignore_keys),
        "# Key rebinding (JSON format, e.g., {\"c\": \"s\", \"s\": \"c\"})": "",
        "key_rebindings": json.dumps(key_rebindings)
    }
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

def check_for_updates(log_queue):
    log_queue.put("MainProcess: Checking for updates...")
    try:
        timestamp = str(time.time())
        url_with_timestamp = f"{GITHUB_URL}?t={timestamp}"
        response = requests.get(url_with_timestamp, timeout=5)
        response.raise_for_status()
        remote_content = response.text
        log_queue.put("MainProcess: Successfully fetched remote file")

        remote_version = None
        for line in remote_content.splitlines():
            if line.strip().startswith('VERSION = "'):
                remote_version = line.strip().split('"')[1]
                log_queue.put(f"MainProcess: Found remote version: {remote_version}")
                break
        if not remote_version:
            log_queue.put("MainProcess: No VERSION found in remote file")
            return

        local_ver_tuple = tuple(map(int, VERSION.split(".")))
        remote_ver_tuple = tuple(map(int, remote_version.split(".")))
        log_queue.put(f"MainProcess: Local version: {VERSION}, Remote version: {remote_version}")
        if remote_ver_tuple > local_ver_tuple:
            log_queue.put("MainProcess: Newer version detected, prompting user")
            if messagebox.askyesno("Update Available",
                                   f"A new version ({remote_version}) is available!\n"
                                   f"Current version: {VERSION}\n"
                                   "Download and update now?"):
                log_queue.put("MainProcess: User chose to update")
                script_path = sys.argv[0]
                log_queue.put(f"MainProcess: Updating file at {script_path}")
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(remote_content)
                    f.flush()
                log_queue.put("MainProcess: New version downloaded")
                time.sleep(0.5)
                log_queue.put("MainProcess: Relaunching with new version")
                os.execv(sys.executable, [sys.executable] + sys.argv)
                sys.exit(0)
            else:
                log_queue.put("MainProcess: User declined update")
        else:
            log_queue.put("MainProcess: No update needed (remote <= local)")
    except requests.RequestException as e:
        log_queue.put(f"MainProcess: Failed to check for updates: {str(e)}")
    except Exception as e:
        log_queue.put(f"MainProcess: Update error: {str(e)}")

def monitor_keyboard_process(key_queues, is_running_flag, is_paused_flag, log_queue, key_rebindings):
    pressed_keys = {}
    log_queue.put("Process-1: Keyboard process started")
    while is_running_flag.value:
        if not is_paused_flag.value:
            event = keyboard.read_event(suppress=True)
            original_key = event.name
            if event.event_type == keyboard.KEY_DOWN:
                if original_key.lower() not in pressed_keys:
                    pressed_keys[original_key.lower()] = True
                    remapped_key = key_rebindings.get(original_key.lower(), original_key)
                    for i, q in enumerate(key_queues):
                        while q.qsize() >= 2:
                            try:
                                q.get_nowait()
                            except queue.Empty:
                                break
                        q.put((original_key, remapped_key))
                        if original_key.lower() != remapped_key.lower():
                            log_queue.put(f"Process-1: Sent {remapped_key} (rebound from {original_key}) to queue {i}")
                        else:
                            log_queue.put(f"Process-1: Sent {original_key} to queue {i}")
            elif event.event_type == keyboard.KEY_UP:
                if original_key.lower() in pressed_keys:
                    del pressed_keys[original_key.lower()]
    log_queue.put("Process-1: Keyboard process exiting")

def window_process(key_queue, is_running_flag, is_paused_flag, window_id, ignore_keys, log_queue, server_url, use_default_profile):
    special_keys_map = {
        'up': Keys.ARROW_UP, 'down': Keys.ARROW_DOWN,
        'left': Keys.ARROW_LEFT, 'right': Keys.ARROW_RIGHT,
    }
    log_queue.put(f"Process-{window_id+2}: Window {window_id} initializing Firefox")
    try:
        options = Options()
        if use_default_profile:
            profile_path = os.path.join(os.environ.get('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles')
            profile_dirs = [d for d in os.listdir(profile_path) if os.path.isdir(os.path.join(profile_path, d)) and 'default-release' in d]
            if not profile_dirs:
                log_queue.put(f"Process-{window_id+2}: Window {window_id} no default-release profile found, using temporary profile")
                firefox_profile = FirefoxProfile()
            else:
                default_profile = os.path.join(profile_path, profile_dirs[0])
                firefox_profile = FirefoxProfile(default_profile)
                firefox_profile.set_preference("signon.autofillForms", True)
                firefox_profile.set_preference("signon.rememberSignons", True)
                log_queue.put(f"Process-{window_id+2}: Window {window_id} using default profile copy from {default_profile}")
            options.profile = firefox_profile
        driver = webdriver.Firefox(options=options)
        log_queue.put(f"Process-{window_id+2}: Window {window_id} Firefox launched")
    except Exception as e:
        log_queue.put(f"Process-{window_id+2}: Window {window_id} Firefox failed: {str(e)}")
        return

    driver.get(server_url)
    wait = WebDriverWait(driver, 10)
    
    body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    driver.switch_to.window(driver.window_handles[0])
    ActionChains(driver).move_to_element(body).click().perform()
    driver.maximize_window()
    
    log_queue.put(f"Process-{window_id+2}: Window {window_id} process started")
    while is_running_flag.value:
        if not is_paused_flag.value:
            try:
                original_key, remapped_key = key_queue.get(timeout=0.05)
                log_queue.put(f"Process-{window_id+2}: Window {window_id} got key: {remapped_key} (from {original_key})")
                selenium_key = special_keys_map.get(remapped_key.lower(), remapped_key)
                window_title = driver.title.lower()
                should_ignore = any(
                    original_key.lower() in [k.lower() for k in keys]
                    for pattern, keys in ignore_keys.items()
                    if pattern.lower() in window_title
                )
                if not should_ignore:
                    try:
                        body.send_keys(selenium_key)
                        log_queue.put(f"Process-{window_id+2}: Window {window_id} sending {remapped_key} to {window_title}")
                    except EC.StaleElementReferenceException:
                        log_queue.put(f"Process-{window_id+2}: Window {window_id} stale element detected, refreshing body")
                        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                        ActionChains(driver).move_to_element(body).click().perform()
                        body.send_keys(selenium_key)
                        log_queue.put(f"Process-{window_id+2}: Window {window_id} resent {remapped_key} to {window_title} after refresh")
            except queue.Empty:
                continue
            except Exception as e:
                log_queue.put(f"Process-{window_id+2}: Window {window_id} error sending keys: {str(e)}")
        time.sleep(0.01)
    driver.quit()
    log_queue.put(f"Process-{window_id+2}: Window {window_id} process exiting")

class ConfigWindow:
    def __init__(self, parent, app):
        self.top = Toplevel(parent)
        self.top.title("RWK Multi Config")
        self.top.geometry("400x600")
        self.app = app
        
        # Load fresh config from file
        server_url, use_default_profile, num_game_windows, ignore_keys, key_rebindings = load_config()
        
        self.server_url = StringVar(value=server_url)
        self.use_default_profile = IntVar(value=use_default_profile)
        self.num_game_windows = StringVar(value=str(num_game_windows))
        self.ignore_keys = ignore_keys.copy()
        self.key_rebindings = key_rebindings.copy()
        
        Label(self.top, text="Server URL:").pack(pady=5)
        Entry(self.top, textvariable=self.server_url, width=40).pack()
        
        Checkbutton(self.top, text="Use Default Firefox Profile", variable=self.use_default_profile).pack(pady=5)
        
        Label(self.top, text="Number of Game Windows:").pack(pady=5)
        Entry(self.top, textvariable=self.num_game_windows, width=10).pack()
        
        Label(self.top, text="Key Ignore Settings (JSON, e.g., {\"Pattern\": [\"key1\", \"key2\"]})").pack(pady=5)
        self.ignore_text = Text(self.top, height=10, width=40, wrap=WORD)
        self.ignore_text.insert(END, json.dumps(self.ignore_keys, indent=2))
        self.ignore_text.pack()

        Label(self.top, text="Key Rebindings (JSON, e.g., {\"c\": \"s\", \"s\": \"c\"})").pack(pady=5)
        self.rebind_text = Text(self.top, height=10, width=40, wrap=WORD)
        self.rebind_text.insert(END, json.dumps(self.key_rebindings, indent=2))
        self.rebind_text.pack()

        # Right-click context menu for both text fields
        self.context_menu = Menu(self.top, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut)
        self.context_menu.add_command(label="Copy", command=self.copy)
        self.context_menu.add_command(label="Paste", command=self.paste)
        self.ignore_text.bind("<Button-3>", self.show_context_menu)
        self.rebind_text.bind("<Button-3>", self.show_context_menu)

        Button(self.top, text="Save and Close", command=self.save).pack(pady=10)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def cut(self):
        if self.top.focus_get() == self.ignore_text:
            self.ignore_text.event_generate("<<Cut>>")
        elif self.top.focus_get() == self.rebind_text:
            self.rebind_text.event_generate("<<Cut>>")

    def copy(self):
        if self.top.focus_get() == self.ignore_text:
            self.ignore_text.event_generate("<<Copy>>")
        elif self.top.focus_get() == self.rebind_text:
            self.rebind_text.event_generate("<<Copy>>")

    def paste(self):
        if self.top.focus_get() == self.ignore_text:
            self.ignore_text.event_generate("<<Paste>>")
        elif self.top.focus_get() == self.rebind_text:
            self.rebind_text.event_generate("<<Paste>>")

    def save(self):
        try:
            new_ignore_keys = json.loads(self.ignore_text.get("1.0", END).strip())
            new_key_rebindings = json.loads(self.rebind_text.get("1.0", END).strip())
            new_num_windows = int(self.num_game_windows.get())
            if new_num_windows <= 0:
                raise ValueError("Number of windows must be positive")
            for from_key, to_key in new_key_rebindings.items():
                if not isinstance(from_key, str) or not isinstance(to_key, str) or len(from_key) != 1 or len(to_key) != 1:
                    raise ValueError("Key rebinding must map single keys (e.g., 'c' to 's')")
            save_config(self.server_url.get(), self.use_default_profile.get(), new_num_windows, new_ignore_keys, new_key_rebindings)
            self.app.server_url = self.server_url.get()
            self.app.use_default_profile = self.use_default_profile.get()
            self.app.num_game_windows = new_num_windows
            self.app.ignore_keys = new_ignore_keys
            self.app.key_rebindings = new_key_rebindings
            self.app.num_window_entry.delete(0, END)
            self.app.num_window_entry.insert(END, str(new_num_windows))
            self.app.log_queue.put("MainProcess: Configuration updated successfully")
            self.top.destroy()
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON format: {str(e)}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class RWKMultiClient:
    def __init__(self, master):
        self.master = master
        master.title("RWK Multibox Client")
        
        self.is_running = False
        self.is_paused = True
        
        self.server_url, self.use_default_profile, self.num_game_windows, self.ignore_keys, self.key_rebindings = load_config()
        
        self.log_queue = mp.Queue()
        self.processes = []
        
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.close_application)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        check_for_updates(self.log_queue)
        self.update_gui()

    def create_widgets(self):
        self.num_window_label = Label(self.master, text="Number of Game Windows:")
        self.num_window_label.grid(row=0, column=0)

        self.num_window_entry = Entry(self.master)
        self.num_window_entry.insert(END, self.num_game_windows)
        self.num_window_entry.grid(row=0, column=1)

        self.start_stop_button = Button(self.master, text="Start", command=self.start_stop)
        self.start_stop_button.grid(row=1, column=0)

        self.copy_logs_button = Button(self.master, text="Copy Logs", command=self.copy_logs)
        self.copy_logs_button.grid(row=1, column=1)

        self.config_button = Button(self.master, text="Config", command=self.open_config)
        self.config_button.grid(row=1, column=2)

        self.output_text = Text(self.master, width=50, wrap=WORD, bg="black", fg="white")
        self.output_text.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.scrollbar = Scrollbar(self.master, command=self.output_text.yview)
        self.scrollbar.grid(row=2, column=3, sticky='nsew')
        self.output_text['yscrollcommand'] = self.scrollbar.set

    def open_config(self):
        ConfigWindow(self.master, self)

    def copy_logs(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.output_text.get("1.0", END))
        self.output_text.insert(END, "MainProcess: Logs copied to clipboard!\n")
        self.output_text.see(END)

    def start_stop(self):
        if self.is_running:
            if self.is_paused:
                self.resume()
            else:
                self.pause()
        else:
            self.start()

    def start(self):
        try:
            self.num_game_windows = int(self.num_window_entry.get())
        except ValueError:
            self.log_queue.put("MainProcess: Please enter a valid number for game windows.\n")
            return

        self.log_queue.put("MainProcess: \nRWK Multibox Client started...\n"
                          "(Wait for all browser windows to open before taking any action.)\n\n")
        self.is_running = True
        self.update_start_stop_button_text()

        self.key_queues = [mp.Queue(maxsize=2) for _ in range(self.num_game_windows)]
        self.is_running_flag = mp.Value('b', True)
        self.is_paused_flag = mp.Value('b', True)
        
        keyboard_process = mp.Process(target=monitor_keyboard_process, args=(self.key_queues, self.is_running_flag, self.is_paused_flag, self.log_queue, self.key_rebindings))
        keyboard_process.daemon = True
        keyboard_process.start()
        self.processes.append(keyboard_process)
        
        for i in range(self.num_game_windows):
            p = mp.Process(target=window_process, args=(self.key_queues[i], self.is_running_flag, self.is_paused_flag, i, self.ignore_keys, self.log_queue, self.server_url, self.use_default_profile))
            p.daemon = True
            p.start()
            self.processes.append(p)
            time.sleep(0.5)
        self.log_queue.put(f"MainProcess: Started {self.num_game_windows} window processes")

    def pause(self):
        self.is_paused = True
        self.is_paused_flag.value = True
        self.update_start_stop_button_text()

    def resume(self):
        self.is_paused = False
        self.is_paused_flag.value = False
        self.update_start_stop_button_text()

    def update_start_stop_button_text(self):
        self.start_stop_button.config(text="Resume" if self.is_paused else "Pause")

    def update_gui(self):
        try:
            while not self.log_queue.empty():
                msg = self.log_queue.get_nowait()
                self.output_text.insert(END, msg + "\n")
                self.output_text.see(END)
        except queue.Empty:
            pass
        self.master.after(100, self.update_gui)

    def close_application(self):
        self.is_running = False
        if hasattr(self, 'is_running_flag'):
            self.is_running_flag.value = False
            
            for p in self.processes:
                p.join(timeout=2)
            
            for p in self.processes:
                if p.is_alive():
                    p.terminate()
                    self.log_queue.put(f"MainProcess: Force terminated process {p.pid}")
        
        self.master.destroy()
        os._exit(0)

if __name__ == "__main__":
    root = Tk()
    app = RWKMultiClient(root)
    root.mainloop()
