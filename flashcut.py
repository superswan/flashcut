import cv2
import os
import sys
import numpy as np
import random
from moviepy.editor import VideoFileClip, AudioFileClip
import yt_dlp as youtube_dl

def convert_mm_ss_to_seconds(time_str):
    """Converts a time string of the format MM:SS to seconds."""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def download_audio(url, output_name="downloaded_audio"):
    initial_opts = {
        'quiet': True,
        'noplaylist': True
    }

    with youtube_dl.YoutubeDL(initial_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        if video_title:
            # Clean and prepare the filename
            safe_title = "".join([c if c.isalnum() or c in " _-." else "_" for c in video_title.replace(" ", "_")])
            max_title_length = 255 - len(output_name) - 4  # Account for ".mp3"
            if len(safe_title) > max_title_length:
                safe_title = safe_title[:max_title_length]
            full_output_name = f"{output_name}_{safe_title}"
        else:
            full_output_name = f"{output_name}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': full_output_name + '.%(ext)s',
        'quiet': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return os.path.join(os.getcwd(), full_output_name + '.mp3')

def create_video(image_folder, video_name, duration, delay_ms, format_type='square', randomize=False, audio_url=None, audio_time_start=0):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images.sort()  
    num_images = len(images)

    if not images:
        raise ValueError("No images found in the directory.")
    
    if randomize:
        random.shuffle(images)

    print(f"Loaded {num_images} image files...")

    if audio_url:
        print(f"Registered Audio URL: {audio_url}")

    # video formatting stuff (square 4:3 res, and "HD" (lol) 720p supported)
    if format_type == 'square':
        width, height = 640, 480  # Standard 4:3 aspect ratio
    elif format_type == 'hd':
        width, height = 1280, 720  # HD resolution, 16:9 aspect ratio

    video_length_seconds = 30 if duration == "short" else 60  
    max_fps = 30
    base_frame_duration = 1.0 / max_fps  
    total_frame_duration = base_frame_duration + (delay_ms / 1000.0)  

    # if there aren't enough images adjust delay or hoard more
    num_images_needed = int(video_length_seconds / total_frame_duration)
    if len(images) > num_images_needed:
        images = images[:num_images_needed]  
        print(f"Using {num_images_needed} images out of the available ones to match the video length with delay.")

    fps = 1.0 / total_frame_duration  
    print(f"Calculated FPS considering delay: {fps}")

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        img = cv2.imread(os.path.join(image_folder, image))
        if img is None:
            continue  

        h, w = img.shape[:2]
        scale = min(width / w, height / h)
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        x_offset = (width - new_w) // 2
        y_offset = (height - new_h) // 2
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        video.write(canvas)

    video.release()

    if audio_url:
        audio_file = download_audio(audio_url)
        video_clip = VideoFileClip(video_name)
        audio_time_end = int(audio_time_start) + int(video_length_seconds)
        audio_clip = AudioFileClip(audio_file).subclip(audio_time_start, audio_time_end)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile("final_" + video_name, codec='libx264')
    
    audio_clip.close()
    video_clip.close()
    final_clip.close()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python flashcut.py <image_directory> <output_video.mp4> <long|short>")
        sys.exit(1)

    dir_path = sys.argv[1]
    output_path = sys.argv[2]
    video_length = sys.argv[3].lower()
    delay_ms = int(sys.argv[4])
    format_type = sys.argv[5].lower() if len(sys.argv) > 5 and sys.argv[5].lower() in ['square', 'hd'] else 'square'
    randomize = 'randomize' in sys.argv
    audio_url = sys.argv[7] if len(sys.argv) >= 8 else None
    audio_time_start = convert_mm_ss_to_seconds(sys.argv[8]) if audio_url else None
    create_video(dir_path, output_path, video_length, delay_ms, format_type, randomize, audio_url, audio_time_start)
