import os
import re
import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def extract_anime_info(filename):
    pattern = r'\[.*?\]\s*(?P<name>.*?)\s*\[(?P<ep_number>\d{2})\]'
    match = re.search(pattern, filename)
    if match:
        name = match.group('name').strip()
        ep_number = match.group('ep_number').strip()
        return {
            "anime_name": name,
            "episode_number": ep_number
        }
    else:
        return None


def capture_screenshots(video_path, output_dir, frequency):
    fps_value = 1 / frequency
    command = [
        'ffmpeg', '-i', video_path, '-vf', f'fps={fps_value}', '-q:v', '2',
        os.path.join(output_dir, 'frame_%06d.png')
    ]
    subprocess.run(command, check=True)


def process_videos(source_dir, capture_dir, frequency):
    for path_root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(('.mkv', '.mp4')):
                video_path = os.path.join(path_root, file)
                info = extract_anime_info(file)
                if info:
                    anime_name = info['anime_name']
                    episode_number = info['episode_number']
                    episode_capture_dir = os.path.join(capture_dir, anime_name, episode_number)
                    os.makedirs(episode_capture_dir, exist_ok=True)
                    capture_screenshots(video_path, episode_capture_dir, frequency)


if __name__ == "__main__":
    DEFAULT_CAPTURE_DIR = "capture"
    root = Tk()
    root.withdraw()

    video_file = askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv")])

    while True:
        try:
            frequency_input = input("Enter screenshot frequency in seconds (positive integer, e.g., 1 for every 1 second): ")
            frequency_input = int(frequency_input)
            if frequency_input <= 0:
                print("Frequency must be a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    if video_file:
        picked_video_path = video_file
        picked_file = os.path.basename(picked_video_path)
        picked_info = extract_anime_info(picked_file)
        if picked_info:
            picked_anime_name = picked_info['anime_name']
            picked_episode_number = picked_info['episode_number']
            picked_episode_capture_dir = os.path.join(DEFAULT_CAPTURE_DIR, picked_anime_name, picked_episode_number)
            os.makedirs(picked_episode_capture_dir, exist_ok=True)
            capture_screenshots(picked_video_path, picked_episode_capture_dir, frequency_input)
        else:
            print("Could not extract anime info from the filename.")
    else:
        default_source_dir = "source"
        process_videos(default_source_dir, DEFAULT_CAPTURE_DIR, frequency_input)
