import tkinter as tk
from tkinter import simpledialog, colorchooser, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import json
import os
import webbrowser

class CrosshairApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crossy v0.0.2")
        self.geometry("600x660")
        self.resizable(False, False)
        self.iconbitmap(r"C:\Users\ooz76\Desktop\fortnite-python\v-0.0.2\CROSSY-V-0.0.2.ico")
        self.bg_color = "#1A1A1A"
        self.fg_color = "#FF00FF"
        self.button_bg = "#3D3D3D"
        self.button_fg = "#FF00FF"
        self.crosshair_color = self.fg_color
        self.crosshair_size = 20
        self.screen_width = 1440
        self.screen_height = 1080
        self.crosshair_overlay = None
        self.custom_crosshair_path = None
        self.setup_styles()
        self.create_widgets()
        self.load_config()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background=self.button_bg, foreground=self.button_fg, font=("Consolas", 12), borderwidth=0, padding=6)
        style.map("TButton", background=[('active', "#FF00FF")], foreground=[('active', '#800080')])
        style.configure("TLabel", background=self.bg_color, foreground=self.button_fg, font=("Consolas", 12))

    def create_widgets(self):
        self.configure(bg=self.bg_color)
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(pady=10, padx=10)

        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.grid(row=0, column=0, padx=10)
        tk.Label(left_frame, text="↓IMPORTANT↓", bg=self.bg_color, fg="#FF00FF", font=("Consolas", 20)).pack(pady=10)
        self.left_image = Image.open("v0.0.2-crossOFFICIAL.png")
        self.left_image = self.left_image.resize((150, 150), Image.LANCZOS)
        self.left_image_tk = ImageTk.PhotoImage(self.left_image)
        tk.Label(left_frame, image=self.left_image_tk, bg=self.bg_color).pack()

        update_button = ttk.Button(left_frame, text="Check for updates!", command=self.open_github)
        update_button.pack(pady=5)

        kenney_button = ttk.Button(left_frame, text="Kenney's Crosshair Pack", command=self.open_kenney)
        kenney_button.pack(pady=5)
        tk.Label(left_frame, text="^ONLY GOOD CROSSHAIRS FOR CROSSY^", bg=self.bg_color, fg="#FF00FF", font=("Consolas", 9)).pack(pady=5)

        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.grid(row=0, column=1, padx=10)
        tk.Label(right_frame, text="Welcome to Crossy (v0.0.2)", font=("Consolas", 16, "bold"), bg=self.bg_color, fg="#FF00FF").pack(pady=10)

        self.preview_frame = tk.Frame(right_frame, width=150, height=150, bg="black", highlightthickness=1, highlightbackground="#FF00FF")
        self.preview_frame.pack(pady=5)

        self.preview_canvas = tk.Canvas(self.preview_frame, width=150, height=150, bg="black", highlightthickness=0)
        self.preview_canvas.pack()
        self.draw_preview()

        size_frame = tk.Frame(right_frame, bg=self.bg_color)
        size_frame.pack(pady=5)
        tk.Label(size_frame, text="Crosshair Size", bg=self.bg_color, fg=self.button_fg).pack(side="left", padx=5)

        self.size_slider = ttk.Scale(size_frame, from_=5, to=200, orient="horizontal", command=self.update_size)
        self.size_slider.set(self.crosshair_size)
        self.size_slider.pack(side="left")

        button_frame = tk.Frame(right_frame, bg=self.bg_color)
        button_frame.pack(pady=10)
        for text, command in [
            ("Color", self.change_color),
            ("Resolution", self.set_resolution),
            ("Set Crosshair", self.open_crosshair),
            ("Hide Crosshair", self.remove_crosshair),
            ("Custom Crosshair", self.load_custom_crosshair),
            ("Default Crosshair", self.reset_to_default),
            ("Save Config", self.save_config),
            ("Join our Discord", self.join_discord)
        ]:
            self.create_button(button_frame, text, command)

        self.note_label = tk.Label(self, text="CUSTOM CROSSHAIRS ARE A BIT GLITCHY! looking for a way to fix it! :D v0.0.2",
                                   font=("Consolas", 10), bg=self.bg_color, fg="#FF00FF", anchor="w")
        self.note_label.pack(anchor="w", padx=10, pady=(10, 0))

    def create_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(pady=5, padx=10, fill='x')

    def draw_preview(self):
        self.preview_canvas.delete("all")
        if self.custom_crosshair_path:
            custom_img = Image.open(self.custom_crosshair_path)
            custom_img = custom_img.resize((self.crosshair_size, self.crosshair_size), Image.LANCZOS)
            self.preview_canvas.image = ImageTk.PhotoImage(custom_img)
            self.preview_canvas.create_image(75, 75, image=self.preview_canvas.image)
        else:
            center_x, center_y = 75, 75
            half_size = self.crosshair_size // 2
            self.preview_canvas.create_line(center_x - half_size, center_y, center_x + half_size, center_y, fill=self.crosshair_color, width=2)
            self.preview_canvas.create_line(center_x, center_y - half_size, center_x, center_y + half_size, fill=self.crosshair_color, width=2)

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
        self.crosshair_overlay = CrosshairOverlay(self.crosshair_color, self.crosshair_size, self.screen_width, self.screen_height, self.custom_crosshair_path)

    def remove_crosshair(self):
        if self.crosshair_overlay:
            self.crosshair_overlay.destroy()
            self.crosshair_overlay = None

    def load_custom_crosshair(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.custom_crosshair_path = file_path
            self.draw_preview()

    def reset_to_default(self):
        self.custom_crosshair_path = None
        self.draw_preview()

    def save_config(self):
        config = {
            "color": self.crosshair_color,
            "size": self.crosshair_size,
            "screen_width": self.screen_width,
            "screen_height": self.screen_height,
            "custom_crosshair_path": self.custom_crosshair_path
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
                self.custom_crosshair_path = config.get("custom_crosshair_path", None)
                self.size_slider.set(self.crosshair_size)
                self.draw_preview()

    def join_discord(self):
        webbrowser.open("https://discord.gg/24ryn3rxGU")

    def open_github(self):
        webbrowser.open("https://github.com/semze/crossy/releases")

    def open_kenney(self):
        webbrowser.open("https://github.com/semze/crossy/releases/download/initial-release/kenney_crosshair-pack.zip")


class CrosshairOverlay(tk.Toplevel):
    def __init__(self, color, size, screen_width, screen_height, custom_crosshair_path=None):
        super().__init__()
        self.crosshair_color = color
        self.crosshair_size = size
        self.custom_crosshair_path = custom_crosshair_path
        initial_x = (screen_width - 150) // 2
        initial_y = (screen_height - 150) // 2
        self.geometry(f"150x150+{initial_x}+{initial_y}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 1.0)
        self.attributes("-transparentcolor", "black")
        self.canvas = tk.Canvas(self, width=150, height=150, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.draw_crosshair()

    def draw_crosshair(self):
        self.canvas.delete("all")
        if self.custom_crosshair_path:
            custom_img = Image.open(self.custom_crosshair_path)
            custom_img = custom_img.resize((self.crosshair_size, self.crosshair_size), Image.LANCZOS)
            self.crosshair_image = ImageTk.PhotoImage(custom_img)
            self.canvas.create_image(75, 75, image=self.crosshair_image)
        else:
            center_x, center_y = 75, 75
            half_size = self.crosshair_size // 2
            self.canvas.create_line(center_x - half_size, center_y, center_x + half_size, center_y, fill=self.crosshair_color, width=2)
            self.canvas.create_line(center_x, center_y - half_size, center_x, center_y + half_size, fill=self.crosshair_color, width=2)

if __name__ == "__main__":
    app = CrosshairApp()
    app.mainloop()