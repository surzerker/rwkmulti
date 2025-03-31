from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing as mp
import keyboard
import queue
import time
import os

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
                        q.put(input_key)
                        log_queue.put(f"Process-1: Sent {input_key} to queue {i}")
            elif event.event_type == keyboard.KEY_UP:
                if input_key.lower() in pressed_keys:
                    del pressed_keys[input_key.lower()]
        else:
            time.sleep(0.01)
    log_queue.put("Process-1: Keyboard process exiting")

def window_process(key_queue, is_running_flag, is_paused_flag, window_id, ignore_keys, log_queue):
    special_keys_map = {
        'up': Keys.ARROW_UP, 'down': Keys.ARROW_DOWN,
        'left': Keys.ARROW_LEFT, 'right': Keys.ARROW_RIGHT,
    }
    driver = webdriver.Firefox()
    url = "https://r2p3.racewarkingdoms.com/"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    
    # Initial body fetch
    body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    driver.switch_to.window(driver.window_handles[0])
    ActionChains(driver).move_to_element(body).click().perform()
    driver.maximize_window()
    
    log_queue.put(f"Process-{window_id+2}: Window {window_id} process started")
    while is_running_flag.value:
        if not is_paused_flag.value:
            try:
                input_key = key_queue.get(timeout=0.01)
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
        time.sleep(0.01)  # Small delay to reduce CPU load
    driver.quit()
    log_queue.put(f"Process-{window_id+2}: Window {window_id} process exiting")

class RWKMultiClient:
    def __init__(self, master):
        self.master = master
        master.title("RWK Multibox Client")
        
        self.num_game_windows = 4
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

        self.key_queues = [mp.Queue() for _ in range(self.num_game_windows)]
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
