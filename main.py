import os
import re
import subprocess


def extract_anime_info(filename):
    pattern = r'\[.*?\]\s*(?P<anime_name>.*?)\s*\[(?P<episode_number>\d{2})\]'
    match = re.search(pattern, filename)
    if match:
        anime_name = match.group('anime_name').strip()
        episode_number = match.group('episode_number').strip()
        return {
            "anime_name": anime_name,
            "episode_number": episode_number
        }
    else:
        return None


def capture_screenshots(video_path, output_dir):
    command = [
        'ffmpeg', '-i', video_path, '-vf', 'fps=1', '-q:v', '2',
        os.path.join(output_dir, 'frame_%06d.png')
    ]
    subprocess.run(command, check=True)


def process_videos(source_dir, capture_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(('.mkv', '.mp4')):
                video_path = os.path.join(root, file)
                info = extract_anime_info(file)
                if info:
                    anime_name = info['anime_name']
                    episode_number = info['episode_number']
                    episode_capture_dir = os.path.join(capture_dir, anime_name, episode_number)
                    os.makedirs(episode_capture_dir, exist_ok=True)
                    capture_screenshots(video_path, episode_capture_dir)


if __name__ == "__main__":
    source_dir = "source"
    capture_dir = "capture"
    process_videos(source_dir, capture_dir)
