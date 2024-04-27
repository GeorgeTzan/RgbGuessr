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
        self.root.title("RgbGeusser")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.menubar = tk.Menu(self.root)
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New Game", command=self.new_game)
        self.menubar.add_cascade(label="Menu", menu=filemenu)
        self.root.config(menu=self.menubar)
        self.scores = []
        self.tries = 0
        self.submitColour = tk.Button(
            self.root, text="Submit", command=self.runOnSubmit
        )
        self.redSlider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.greenSlider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.blueSlider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)

        self.redLabel = tk.Label(self.root, text="Red", fg="red")
        self.greenLabel = tk.Label(self.root, text="Green", fg="green")
        self.blueLabel = tk.Label(self.root, text="Blue", fg="blue")

        self.submitColour.place(relx=0.1, rely=0.35)
        self.redSlider.place(relx=0.3, rely=0)
        self.greenSlider.place(relx=0.3, rely=0.1)
        self.blueSlider.place(relx=0.3, rely=0.2)
        self.redLabel.place(relx=0.23, rely=0.05)
        self.greenLabel.place(relx=0.2, rely=0.15)
        self.blueLabel.place(relx=0.23, rely=0.25)

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
        self.randomisedColour.place(relx=0.01, rely=0.45)

        self.userColour = tk.Canvas(self.root, width=200, height=200)
        self.userRect = self.userColour.create_rectangle(0, 0, 170, 200, fill="blue")
        self.userColour.place(relx=0.55, rely=0.45)

        self.setRandomColour()
        self.root.mainloop()

    def on_closing(self):
        utils.free_memory(self.rgbAlloc)
        self.root.destroy()

    def setRandomColour(self):
        utils.random_rgb.restype = ctypes.POINTER(getRGB)
        self.rgbAlloc = utils.random_rgb()
        self.rgb = (
            self.rgbAlloc.contents.r,
            self.rgbAlloc.contents.g,
            self.rgbAlloc.contents.b,
        )
        color = self.format_color(self.rgb)
        self.randomisedColour.itemconfig(self.rectangleRand, fill=color)

    def setUserColour(self):
        rgb = (self.redSlider.get(), self.greenSlider.get(), self.blueSlider.get())
        color = self.format_color(rgb)
        self.userColour.itemconfig(self.userRect, fill=color)
        return rgb

    def format_color(self, rgb):
        return "#%02x%02x%02x" % rgb

    def runOnSubmit(self):
        self.tries += 1
        userRGB = self.setUserColour()
        userRGB_ctypes = getRGB(userRGB[0], userRGB[1], userRGB[2])
        otherRGB_ctypes = getRGB(self.rgb[0], self.rgb[1], self.rgb[2])
        utils.getRGB_distance.restype = ctypes.c_int
        difference = utils.getRGB_distance(userRGB_ctypes, otherRGB_ctypes)
        print(self.rgb[0], self.rgb[1], self.rgb[2])
        print((difference <= MAX_COLOR_DIFF))
        print(difference)
        max_difference = utils.getRGB_distance(getRGB(255, 255, 255), getRGB(0, 0, 0))
        percentage = (difference / max_difference) * 100
        self.scores.append(percentage)
        self.triesLabel.config(text=f"Try: {self.tries}/5")
        self.bestScoreLabel.config(text=f"Best Score: {max(self.scores):.1f}%")
        self.distanceLabel.config(
            text=f"({userRGB[0]-self.rgb[0]}, {userRGB[1]-self.rgb[1]}, {userRGB[2]-self.rgb[2]})"
        )
        self.checkWin(difference)

    def new_game(self):
        self.tries = 0
        self.scores = [0]
        self.submitColour.place(relx=0.1, rely=0.35)
        self.setRandomColour()
        self.triesLabel.config(text=f"Try: {self.tries}/5")
        self.bestScoreLabel.config(text=f"Best Score: {max(self.scores):.1f}%")

    def checkWin(self, diff):
        if diff <= MAX_COLOR_DIFF and self.tries <= 5:
            print("Winner Winner chicken dinner")
            utils.free_memory(self.rgbAlloc)
        elif self.tries > MAX_TRIES:
            self.submitColour.place_forget()
            utils.free_memory(self.rgbAlloc)
            print("You've lost")


rgbGUI()
