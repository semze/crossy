import tkinter as tk
from tkinter import simpledialog, colorchooser
from tkinter import ttk
import json
import os
class CrosshairApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("crossy - semodge")
        self.geometry("500x500")
        self.resizable(False, False)
        self.configure(bg="#1E1E2F")
        self.crosshair_color = "#A020F0"
        self.crosshair_size = 20
        self.screen_width = 1440
        self.screen_height = 1080
        self.crosshair_overlay = None
        self.load_config()
        tk.Label(self, text="Crosshair Options", font=("Helvetica", 14), fg="white", bg="#1E1E2F").pack(pady=10)
        self.preview_frame = tk.Frame(self, width=150, height=150, bg="black", highlightthickness=1, highlightbackground="#A020F0")
        self.preview_frame.pack(pady=5)
        self.preview_canvas = tk.Canvas(self.preview_frame, width=150, height=150, bg="black", highlightthickness=0)
        self.preview_canvas.pack()
        self.draw_preview()
        size_frame = tk.Frame(self, bg="#1E1E2F")
        size_frame.pack(pady=5)
        tk.Label(size_frame, text="Crosshair Size", font=("Helvetica", 10), fg="white", bg="#1E1E2F").pack(side="left", padx=5)
        self.size_slider = ttk.Scale(size_frame, from_=5, to=50, orient="horizontal", command=self.update_size)
        self.size_slider.set(self.crosshair_size)
        self.size_slider.pack(side="left")
        tk.Button(self, text="Change Color", command=self.change_color, bg="#1E1E2F", fg="white", activebackground="#2D2D3C").pack(pady=5)
        tk.Button(self, text="Choose Resolution", command=self.set_resolution, bg="#1E1E2F", fg="white", activebackground="#2D2D3C").pack(pady=5)
        tk.Button(self, text="Set Crosshair", command=self.open_crosshair, bg="#1E1E2F", fg="white", activebackground="#2D2D3C").pack(pady=5)
        tk.Button(self, text="Remove Crosshair", command=self.remove_crosshair, bg="#1E1E2F", fg="white", activebackground="#2D2D3C").pack(pady=5)
        tk.Button(self, text="Replace Crosshair", command=self.replace_crosshair, bg="#1E1E2F", fg="white", activebackground="#2D2D3C").pack(pady=5)
        tk.Button(self, text="Save Config", command=self.save_config, bg="#1E1E2F", fg="white", activebackground="#2D2D3C").pack(pady=5)
    def draw_preview(self):
        self.preview_canvas.delete("all")
        center_x, center_y = 75, 75
        half_size = self.crosshair_size // 2
        self.preview_canvas.create_line(
            center_x - half_size, center_y, center_x + half_size, center_y,
            fill=self.crosshair_color, width=2
        )
        self.preview_canvas.create_line(
            center_x, center_y - half_size, center_x, center_y + half_size,
            fill=self.crosshair_color, width=2
        )
    def update_size(self, event=None):
        self.crosshair_size = int(self.size_slider.get())
        self.draw_preview()
    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.crosshair_color = color
            self.draw_preview()
    def set_resolution(self):
        width = simpledialog.askinteger("Screen Width", "Enter screen width:", initialvalue=self.screen_width)
        height = simpledialog.askinteger("Screen Height", "Enter screen height:", initialvalue=self.screen_height)
        if width and height:
            self.screen_width = width
            self.screen_height = height
    def open_crosshair(self):
        if self.crosshair_overlay:
            self.crosshair_overlay.destroy()
        self.crosshair_overlay = CrosshairOverlay(self.crosshair_color, self.crosshair_size, self.screen_width, self.screen_height)
    def remove_crosshair(self):
        if self.crosshair_overlay:
            self.crosshair_overlay.destroy()
            self.crosshair_overlay = None
    def replace_crosshair(self):
        if self.crosshair_overlay:
            self.crosshair_overlay.destroy()
        self.open_crosshair()
    def save_config(self):
        config = {
            "color": self.crosshair_color,
            "size": self.crosshair_size,
            "screen_width": self.screen_width,
            "screen_height": self.screen_height
        }
        with open("config.json", "w") as config_file:
            json.dump(config, config_file)
    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.crosshair_color = config.get("color", self.crosshair_color)
                self.crosshair_size = config.get("size", self.crosshair_size)
                self.screen_width = config.get("screen_width", self.screen_width)
                self.screen_height = config.get("screen_height", self.screen_height)
class CrosshairOverlay(tk.Toplevel):
    def __init__(self, color, size, screen_width, screen_height):
        super().__init__()
        self.crosshair_color = color
        self.crosshair_size = size
        initial_x = (screen_width - 150) // 2
        initial_y = (screen_height - 150) // 2
        self.geometry(f"150x150+{initial_x}+{initial_y}")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.canvas = tk.Canvas(self, width=150, height=150, bg='black', highlightthickness=0)
        self.canvas.pack()
        self.draw_crosshair()
        self.wm_attributes('-transparentcolor', 'black')
    def draw_crosshair(self):
        self.canvas.delete("all")
        center_x, center_y = 75, 75
        half_size = self.crosshair_size // 2
        self.canvas.create_line(
            center_x - half_size, center_y, center_x + half_size, center_y,
            fill=self.crosshair_color, width=2
        )
        self.canvas.create_line(
            center_x, center_y - half_size, center_x, center_y + half_size,
            fill=self.crosshair_color, width=2
        )
if __name__ == "__main__":
    app = CrosshairApp()
    app.mainloop()
