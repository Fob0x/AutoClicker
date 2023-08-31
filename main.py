import threading
import pyautogui
import tkinter as tk
from pynput import keyboard

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")

        self.click_interval_label = tk.Label(root, text="Click interval:")
        self.click_interval_label.pack()

        self.interval_frame = tk.Frame(root)
        self.minutes_label = tk.Label(self.interval_frame, text="Minutes:")
        self.minutes_label.pack(side=tk.LEFT)
        self.minutes_entry = tk.Entry(self.interval_frame, width=5)
        self.minutes_entry.pack(side=tk.LEFT)
        self.seconds_label = tk.Label(self.interval_frame, text="Seconds:")
        self.seconds_label.pack(side=tk.LEFT)
        self.seconds_entry = tk.Entry(self.interval_frame, width=5)
        self.seconds_entry.pack(side=tk.LEFT)
        self.interval_frame.pack()

        self.mouse_button_frame = tk.Frame(root)
        self.mouse_button_label = tk.Label(self.mouse_button_frame, text="Mouse button:")
        self.mouse_button_label.pack(side=tk.LEFT)
        self.mouse_button_var = tk.StringVar()
        self.mouse_button_var.set("Left")
        self.mouse_button_left = tk.Radiobutton(self.mouse_button_frame, text="Left", variable=self.mouse_button_var, value="Left")
        self.mouse_button_left.pack(side=tk.LEFT)
        self.mouse_button_right = tk.Radiobutton(self.mouse_button_frame, text="Right", variable=self.mouse_button_var, value="Right")
        self.mouse_button_right.pack(side=tk.LEFT)
        self.mouse_button_frame.pack()

        self.click_type_frame = tk.Frame(root)
        self.click_type_label = tk.Label(self.click_type_frame, text="Click type:")
        self.click_type_label.pack(side=tk.LEFT)
        self.click_type_var = tk.StringVar()
        self.click_type_var.set("One")
        self.click_type_one = tk.Radiobutton(self.click_type_frame, text="One", variable=self.click_type_var, value="One")
        self.click_type_one.pack(side=tk.LEFT)
        self.click_type_double = tk.Radiobutton(self.click_type_frame, text="Double", variable=self.click_type_var, value="Double")
        self.click_type_double.pack(side=tk.LEFT)
        self.click_type_frame.pack()

        self.coord_frame = tk.Frame(root)
        self.coord_label = tk.Label(self.coord_frame, text="Mouse coordinates:")
        self.coord_label.pack(side=tk.LEFT)
        self.coord_x = tk.StringVar()
        self.coord_y = tk.StringVar()
        self.coord_x_label = tk.Label(self.coord_frame, textvariable=self.coord_x)
        self.coord_x_label.pack(side=tk.LEFT)
        self.coord_y_label = tk.Label(self.coord_frame, textvariable=self.coord_y)
        self.coord_y_label.pack(side=tk.LEFT)
        self.coord_frame.pack()

        self.pick_button = tk.Button(root, text="Pick Location (F2)", command=self.pick_location)
        self.pick_button.pack()

        self.start_button = tk.Button(root, text="Start (F3)", command=self.start_clicking)
        self.start_button.pack()
        self.stop_button = tk.Button(root, text="Stop (F4)", command=self.stop_clicking)
        self.stop_button.pack()

        self.is_clicking = False

        self.root.bind("<F3>", self.start_clicking)
        self.root.bind("<F4>", self.stop_clicking)
        self.root.bind("<F2>", self.pick_location)

        self.keyboard_listener = keyboard.Listener(on_release=self.on_key_release)
        self.keyboard_listener.start()

    def on_key_release(self, key):
        if key == keyboard.Key.f2:
            x, y = pyautogui.position()
            self.coord_x.set("X: {}".format(x))
            self.coord_y.set("Y: {}".format(y))

    def pick_location(self, event=None):
        x, y = pyautogui.position()
        self.coord_x.set("X: {}".format(x))
        self.coord_y.set("Y: {}".format(y))

    def start_clicking(self, event=None):
        if self.is_clicking:
            return

        interval_minutes = int(self.minutes_entry.get())
        interval_seconds = int(self.seconds_entry.get())
        interval = interval_minutes * 60 + interval_seconds

        button = self.mouse_button_var.get().lower()
        click_type = self.click_type_var.get().lower()
        click_count = 2 if click_type == "double" else 1

        x = int(self.coord_x.get().split(":")[1])
        y = int(self.coord_y.get().split(":")[1])

        self.is_clicking = True
        self.click_loop(interval, button, click_count, x, y)

    def stop_clicking(self, event=None):
        if not self.is_clicking:
            return

        self.is_clicking = False
        self.click_thread.join()

    def click_loop(self, interval, button, click_count, x, y):
        if self.is_clicking:
            pyautogui.click(x=x, y=y, button=button, clicks=click_count)
            self.root.after(interval * 1000, self.click_loop, interval, button, click_count, x, y)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()