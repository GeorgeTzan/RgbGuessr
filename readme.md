# RGB Guesser

RGB Guesser is a simple game built using Python and Tkinter, with some functions running at the C level. Players try to guess the RGB values of a randomly generated color. This document provides an overview of the project, installation instructions, usage guidelines, features, and license information.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How to Play](#how-to-play)
- [Features](#features)
- [License](#license)

## Installation

To install RGB Guesser, follow these steps:

1. Clone the repository:

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

After installing RGB Guesser, follow the on-screen instructions to play the game.

## How to Play

1. Launch the game.
2. Adjust the sliders to select your desired RGB values.
3. Click the "Submit" button to submit your guess.
4. The game will provide feedback on your guess.
5. Try to guess the correct RGB values within the given number of tries to win the game.

## Features

- Randomly generated color for guessing.
- Adjustable sliders for selecting RGB values.
- Developer mode for debugging.
- Score tracking and best score display.
- Responsive GUI design.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
