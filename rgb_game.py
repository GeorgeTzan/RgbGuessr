import tkinter as tk
import os
import ctypes

MAX_COLOR_DIFF = 255 * 0.1
MAX_TRIES = 5

path = os.getcwd()
utils = ctypes.CDLL(os.path.join(path, "utils.so"))


class getRGB(ctypes.Structure):
    _fields_ = [("r", ctypes.c_int), ("g", ctypes.c_int), ("b", ctypes.c_int)]


class rgbGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.title("RgbGeussr")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.developer_mode = tk.BooleanVar()
        self.developer_mode.trace_add("write", self.toggle_developer_mode)

        self.tries = 0
        self.setup_menu()
        self.setup_widgets()
        self.scores = []
        self.set_random_colour()

        self.root.mainloop()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_checkbutton(label="Developer Mode", variable=self.developer_mode)
        filemenu.add_command(label="New Game", command=self.new_game)
        menubar.add_cascade(label="Menu", menu=filemenu)
        self.root.config(menu=menubar)

    def setup_widgets(self):
        self.submitColour = tk.Button(
            self.root, text="Submit", command=self.run_on_submit
        )
        self.redSlider = tk.Scale(
            self.root, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color
        )
        self.greenSlider = tk.Scale(
            self.root, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color
        )
        self.blueSlider = tk.Scale(
            self.root, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color
        )

        self.redLabel = tk.Label(self.root, text="Red", fg="red")
        self.greenLabel = tk.Label(self.root, text="Green", fg="green")
        self.blueLabel = tk.Label(self.root, text="Blue", fg="blue")

        self.submitColour.place(relx=0.1, rely=0.35)
        self.redSlider.place(relx=0.40, rely=0)
        self.greenSlider.place(relx=0.4, rely=0.1)
        self.blueSlider.place(relx=0.4, rely=0.2)

        self.redLabel.place(relx=0.33, rely=0.05)
        self.greenLabel.place(relx=0.3, rely=0.15)
        self.blueLabel.place(relx=0.33, rely=0.25)

        self.triesLabel = tk.Label(self.root, text=f"Try: {self.tries}/5", fg="red")
        self.bestScoreLabel = tk.Label(self.root, text="Best Score: 0%", fg="green")
        self.distanceLabel = tk.Label(self.root, text="(0, 0, 0)", fg="blue")

        self.triesLabel.place(relx=0.25, rely=0.35)
        self.bestScoreLabel.place(relx=0.4, rely=0.35)
        self.distanceLabel.place(relx=0.65, rely=0.35)

        self.randomisedColour = tk.Canvas(self.root, width=200, height=200)
        self.rectangleRand = self.randomisedColour.create_rectangle(
            0, 0, 170, 200, fill="red"
        )
        self.randomisedColour.place(relx=0.01, rely=0.44)
        self.randomisedColourLabel = tk.Label(self.root, text="Color Goal", fg="black")
        self.randomisedColourLabel.place(relx=0.12, rely=0.949)

        self.userColour = tk.Canvas(self.root, width=200, height=200, bg="white")
        self.userRect = self.userColour.create_rectangle(0, 0, 170, 200, fill="white")
        self.userColour.place(relx=0.55, rely=0.44)
        self.userColourLabel = tk.Label(
            self.root, text="User's Color Selection:", fg="black"
        )
        self.userColourLabel.place(relx=0.63, rely=0.949)

    def on_closing(self):
        utils.free_memory(self.rgbAlloc)
        self.root.destroy()

    def toggle_developer_mode(self, *args):
        if self.developer_mode.get():
            print(self)

    def set_random_colour(self):
        utils.random_rgb.restype = ctypes.POINTER(getRGB)
        self.rgbAlloc = utils.random_rgb()
        self.rgb = (
            self.rgbAlloc.contents.r,
            self.rgbAlloc.contents.g,
            self.rgbAlloc.contents.b,
        )
        color = self.format_color(self.rgb)
        self.randomisedColour.itemconfig(self.rectangleRand, fill=color)

    def set_user_colour(self):
        rgb = (self.redSlider.get(), self.greenSlider.get(), self.blueSlider.get())
        color = self.format_color(rgb)
        self.userColour.itemconfig(self.userRect, fill=color)
        return rgb

    def format_color(self, rgb):
        return "#%02x%02x%02x" % rgb

    def run_on_submit(self):
        self.tries += 1
        userRGB = self.set_user_colour()
        userRGB_ctypes = getRGB(userRGB[0], userRGB[1], userRGB[2])
        otherRGB_ctypes = getRGB(self.rgb[0], self.rgb[1], self.rgb[2])
        otherRGB_ctypes.restype = ctypes.c_int
        self.difference = utils.getRGB_distance(userRGB_ctypes, otherRGB_ctypes)

        if self.developer_mode.get():
            print(self.__str__())

        max_difference = utils.getRGB_distance(getRGB(255, 255, 255), getRGB(0, 0, 0))
        percentage = 100 - ((self.difference / max_difference) * 100)
        self.scores.append(percentage)
        self.triesLabel.config(text=f"Try: {self.tries}/5")
        self.bestScoreLabel.config(text=f"Best Score: {max(self.scores):.1f}%")
        self.distanceLabel.config(
            text=f"({userRGB[0]-self.rgb[0]}, {userRGB[1]-self.rgb[1]}, {userRGB[2]-self.rgb[2]})"
        )
        self.check_win(self.difference)

    def new_game(self):
        self.tries = 0
        self.scores = []
        self.submitColour.place(relx=0.1, rely=0.35)
        self.set_random_colour()
        self.triesLabel.config(text=f"Try: {self.tries}/5")
        self.distanceLabel.config(bg=self.root.cget("bg"))
        self.submitColour.config(state="normal")

    def check_win(self, diff):
        if diff <= MAX_COLOR_DIFF and self.tries <= 5:
            self.distanceLabel.config(text="Congrats! You won!", bg="green")
            utils.free_memory(self.rgbAlloc)
            self.submitColour.config(state="disabled")
            self.root.after(3000, self.new_game)
        elif self.tries > MAX_TRIES:
            self.submitColour.config(state="disabled")
            utils.free_memory(self.rgbAlloc)
            self.distanceLabel.config(text="Damn it! You lost!", bg="red")
            self.root.after(3000, self.new_game)

    def update_color(self, *args):
        rgb = (self.redSlider.get(), self.greenSlider.get(), self.blueSlider.get())
        color = self.format_color(rgb)
        self.userColour.itemconfig(self.userRect, fill=color)

    def __str__(self):
        rgb_info = f"RGB Values: ({self.rgb[0]}, {self.rgb[1]}, {self.rgb[2]})"
        try:
            diff_info = (
                f"Is difference <= MAX_COLOR_DIFF: {self.difference <= MAX_COLOR_DIFF}"
            )
            diff_value_info = f"Difference: {self.difference}"
        except AttributeError:
            diff_info = "is Difference: Null"
            diff_value_info = "Difference: Null"
        return f"{rgb_info}\n{diff_info}\n{diff_value_info}"


rgbGUI()
