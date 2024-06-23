# BoxVideo

BoxVideo is a small application designed for Linux that allows you to play videos in a resizable and draggable window. It provides a convenient way to watch your favorite videos while performing other tasks on your computer.
# Features

  Resizable Window: You can resize the video window according to your preference.
  Draggable: The window is draggable, allowing you to move it around the screen as needed.
  Always-on-Top: The video window stays on top of other windows, ensuring that you can watch your video without interruption.
  Sound Support: Optionally play the video with sound.
  Easy Setup: Simply provide the path to your video file, and BoxVideo will handle the rest.

# Requirements

  Linux operating system
  Python 3.x
  Required Python packages (specified in requirements.txt)

# Installation

Clone this repository on your Linux computer
    
    git clone https://github.com/mesflit/boxvideo/

Open boxvideo directory and run setup.sh

    cd boxvideo
    chmod +x setup.sh
    ./setup.sh

# Usage

Once installed, you can launch BoxVideo using the terminal. Run the following commands:

Replace "/path/to/your/video.mp4" with the actual path to your video file.

    boxvideo /path/to/your/video.mp4

Optionally, you can specify the size of the video window in WIDTHxHEIGHT format:

    boxvideo /path/to/your/video.mp4 300x200

To play the video with sound, use the --sound flag:

    boxvideo /path/to/your/video.mp4 --sound
or
    
    boxvideo /path/to/your/video.mp4 300x200 --sound

# License 

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/mesflit/boxvideo/blob/main/LICENSE) file for details.
