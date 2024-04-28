## RgbGuessr 🎨

Hey there! Welcome to RgbGuessr, my latest project that I worked on . I've used Python with Tkinter but also wrote some stuff in C level. I've cooked up a fun little game that's been a blast!

### Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How to Play](#how-to-play)
- [Features](#features)
- [License](#license)

### Installation

Getting RgbGuessr up and running is just as easy as counting from 1 to 5! Just follow these steps:

1. **Clone the Repository:**
   
   Fire up your terminal and run this command:
   ```bash
   git clone https://github.com/GeorgeTzan/RgbGuessr.git
   ```

2. Navigate to the project directory:

    ```bash
    cd rgbguessr
    ```
3. Compile the .so file:
    ```bash
    gcc -fPIC -shared -o utils.so utils.c
    ```
4. Run the game:

    ```bash
    python rgb_game.py
    ```

## Usage

After installing RgbGuessr, follow the following instructions to play the game.

## How to Play

1. Launch the game.
2. Adjust the sliders to select your desired RGB values.
3. Click the "Submit" button to submit your guess.
4. The game will provide feedback based on your guess.
5. Try to guess the correct RGB values within the given number of tries to win the game.
6. You only have a 10% RGB difference to guess the colour.

## Features

- Randomly generated color for guessing.
- Adjustable sliders for selecting RGB values.
- Developer mode for debugging.
- Score tracking and best score display.
- Responsive GUI design.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
