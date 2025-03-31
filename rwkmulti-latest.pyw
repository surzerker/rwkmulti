from tkinter import *
from tkinter import messagebox
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import multiprocessing as mp
import keyboard
import queue
import time
import os
import requests
import sys

# Current version of this script
VERSION = "1.2.0"

# Toggle to use the default Firefox profile (1 = yes, 0 = no)
USE_DEFAULT_PROFILE = 0

# GitHub raw URL for the latest version
GITHUB_URL = "https://raw.githubusercontent.com/surzerker/rwkmulti/main/rwkmulti-latest.pyw"

def check_for_updates(log_queue):
    log_queue.put("MainProcess: Checking for updates...")
    try:
        # Fetch the remote file content
        response = requests.get(GITHUB_URL, timeout=5)
        response.raise_for_status()
        remote_content = response.text
        log_queue.put("MainProcess: Successfully fetched remote file")

        # Extract version from remote file (scan all lines)
        remote_version = None
        for line in remote_content.splitlines():
            if line.strip().startswith('VERSION = "'):
                remote_version = line.strip().split('"')[1]
                log_queue.put(f"MainProcess: Found remote version: {remote_version}")
                break
        if not remote_version:
            log_queue.put("MainProcess: No VERSION found in remote file")
            return

        # Compare versions
        local_ver_tuple = tuple(map(int, VERSION.split(".")))
        remote_ver_tuple = tuple(map(int, remote_version.split(".")))
        log_queue.put(f"MainProcess: Local version: {VERSION}, Remote version: {remote_version}")
        if remote_ver_tuple > local_ver_tuple:
            # Prompt user
            log_queue.put("MainProcess: Newer version detected, prompting user")
            if messagebox.askyesno("Update Available",
                                   f"A new version ({remote_version}) is available!\n"
                                   f"Current version: {VERSION}\n"
                                   "Download and update now?"):
                log_queue.put("MainProcess: User chose to update")
                # Download and overwrite
                script_path = sys.argv[0]
                log_queue.put(f"MainProcess: Updating file at {script_path}")
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(remote_content)
                    f.flush()  # Ensure write completes
                log_queue.put("MainProcess: New version downloaded")
                # Small delay to ensure file system sync
                time.sleep(0.5)
                # Relaunch
                log_queue.put("MainProcess: Relaunching with new version")
                os.execv(sys.executable, [sys.executable] + sys.argv)
                sys.exit(0)  # Shouldn’t reach here, but safety net
            else:
                log_queue.put("MainProcess: User declined update")
        else:
            log_queue.put("MainProcess: No update needed")
    except requests.RequestException as e:
        log_queue.put(f"MainProcess: Failed to check for updates: {str(e)}")
    except Exception as e:
        log_queue.put(f"MainProcess: Update error: {str(e)}")

def monitor_keyboard_process(key_queues, is_running_flag, is_paused_flag, log_queue):
    pressed_keys = {}
    log_queue.put("Process-1: Keyboard process started")
    while is_running_flag.value:
        if not is_paused_flag.value:
            event = keyboard.read_event(suppress=True)
            input_key = event.name
            if event.event_type == keyboard.KEY_DOWN:
                if input_key.lower() not in pressed_keys:
                    pressed_keys[input_key.lower()] = True
                    for i, q in enumerate(key_queues):
                        while q.qsize() >= 2:
                            try:
                                q.get_nowait()
                            except queue.Empty:
                                break
                        q.put(input_key)
                        log_queue.put(f"Process-1: Sent {input_key} to queue {i}")
            elif event.event_type == keyboard.KEY_UP:
                if input_key.lower() in pressed_keys:
                    del pressed_keys[input_key.lower()]
    log_queue.put("Process-1: Keyboard process exiting")

def window_process(key_queue, is_running_flag, is_paused_flag, window_id, ignore_keys, log_queue):
    special_keys_map = {
        'up': Keys.ARROW_UP, 'down': Keys.ARROW_DOWN,
        'left': Keys.ARROW_LEFT, 'right': Keys.ARROW_RIGHT,
    }
    log_queue.put(f"Process-{window_id+2}: Window {window_id} initializing Firefox")
    try:
        options = Options()
        if USE_DEFAULT_PROFILE:
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

    url = "https://r2p3.racewarkingdoms.com/"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    
    body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    driver.switch_to.window(driver.window_handles[0])
    ActionChains(driver).move_to_element(body).click().perform()
    driver.maximize_window()
    
    log_queue.put(f"Process-{window_id+2}: Window {window_id} process started")
    while is_running_flag.value:
        if not is_paused_flag.value:
            try:
                input_key = key_queue.get(timeout=0.05)
                log_queue.put(f"Process-{window_id+2}: Window {window_id} got key: {input_key}")
                selenium_key = special_keys_map.get(input_key, input_key)
                window_title = driver.title.lower()
                should_ignore = any(
                    input_key.lower() in [k.lower() for k in keys]
                    for pattern, keys in ignore_keys.items()
                    if pattern.lower() in window_title
                )
                if not should_ignore:
                    try:
                        body.send_keys(selenium_key)
                        log_queue.put(f"Process-{window_id+2}: Window {window_id} sending {input_key} to {window_title}")
                    except EC.StaleElementReferenceException:
                        log_queue.put(f"Process-{window_id+2}: Window {window_id} stale element detected, refreshing body")
                        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                        ActionChains(driver).move_to_element(body).click().perform()
                        body.send_keys(selenium_key)
                        log_queue.put(f"Process-{window_id+2}: Window {window_id} resent {input_key} to {window_title} after refresh")
            except queue.Empty:
                continue
            except Exception as e:
                log_queue.put(f"Process-{window_id+2}: Window {window_id} error sending keys: {str(e)}")
        time.sleep(0.01)
    driver.quit()
    log_queue.put(f"Process-{window_id+2}: Window {window_id} process exiting")

class RWKMultiClient:
    def __init__(self, master):
        self.master = master
        master.title("RWK Multibox Client")
        
        self.num_game_windows = 12
        self.is_running = False
        self.is_paused = True
        self.ignore_keys = {
            "Surzerker": ["c"],
            "Cid": ["c"],
            "Spongebob": ["a"],
            "Buu": ["a"]
        }
        
        self.log_queue = mp.Queue()
        self.processes = []
        
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.close_application)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        check_for_updates(self.log_queue)  # Check immediately on startup
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

        self.output_text = Text(self.master, width=50, wrap=WORD, bg="black", fg="white")
        self.output_text.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.scrollbar = Scrollbar(self.master, command=self.output_text.yview)
        self.scrollbar.grid(row=2, column=2, sticky='nsew')
        self.output_text['yscrollcommand'] = self.scrollbar.set

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
        
        keyboard_process = mp.Process(target=monitor_keyboard_process, args=(self.key_queues, self.is_running_flag, self.is_paused_flag, self.log_queue))
        keyboard_process.daemon = True
        keyboard_process.start()
        self.processes.append(keyboard_process)
        
        for i in range(self.num_game_windows):
            p = mp.Process(target=window_process, args=(self.key_queues[i], self.is_running_flag, self.is_paused_flag, i, self.ignore_keys, self.log_queue))
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
