# FlashCut Video Generator

## Overview

FlashCut is a Python script that automates the creation of video slideshows from a folder of images. It supports adding background audio from a YouTube or Soundcloud URL, customizing video resolution and duration (limited options), and the ability to randomize the order of images.

## Features

- **Generate videos** from a folder containing `.jpg` or `.png` images.
- **Customize video format** to either a standard 4:3 aspect ratio or a 16:9 HD resolution.
- **Set video duration** as either short (30 seconds) or long (60 seconds).
- **Include background audio** by providing a YouTube URL.
- **Randomize image order** in the video if desired.

## Requirements

- Python 3.7 or higher
- Libraries: `opencv-python`, `numpy`, `moviepy`, `yt-dlp`
- Additional tools: `ffmpeg` (required by `moviepy` and `yt-dlp` for video and audio processing)

## Installation

1. **Install Python dependencies**: Run the following command to install the required Python libraries:

    ```bash
    pip install opencv-python numpy moviepy yt-dlp
    ```

2. **Install FFmpeg**: Ensure FFmpeg is installed on your system. Visit the [FFmpeg download page](https://ffmpeg.org/download.html) for installation instructions.

## Usage

To use FlashCut, navigate to the directory containing `flashcut.py` and run the script with the following command format:

```bash
python flashcut.py <image_directory> <output_video_name.mp4> <long|short> <delay_ms> <format_type> [randomize] [<audio_url>] [timestamp (mm:ss)]
```
The paramater parsing is bad, so recommended to include every argument. 

### Parameters:

- `<image_directory>`: Path to the directory containing your image files (.jpg or .png).
- `<output_video_name.mp4>`: Desired output filename for the video.
- `<long|short>`: Duration of the video - 'long' for 60 seconds, 'short' for 30 seconds.
- `<delay_ms>`: Delay in milliseconds between each frame. Adjust this value to change speed of video and number of images used.
- `<format_type>`: 'square' for 640x480, 'hd' for 1280x720. Defaults to 'square' if not specified.
- `randomize`: Optional. Include this flag to randomize the order of the images.
- `<audio_url>`: Optional. YouTube URL to download background audio. The audio will be trimmed to the video length.
- `<mm:ss>`: Optional. Timestamp for audio start point.

### Examples

- **Create a short video with randomized images and HD format**:

    ```bash
    python flashcut.py ./images myvideo.mp4 short 35 hd randomize
    ```

- **Create a long video with background audio**:

    ```bash
    python flashcut.py ./images myvideo.mp4 long 60 square https://youtu.be/YOUTUBE_VIDEO_ID 1:15
    ```

## Troubleshooting

- Ensure all image files are accessible and have the correct file extensions (.jpg, .png).
- Verify that `ffmpeg` is correctly installed and accessible from your command line or terminal.

For further issues or contributions, please refer to the project repository.
