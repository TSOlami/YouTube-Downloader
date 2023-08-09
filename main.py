import re
import os
from pytube import YouTube
from tqdm import tqdm
from pytube.exceptions import RegexMatchError


def extract(youtube_url):
    """
    Extracts video information and available formats from a YouTube URL.

    Args:
        youtube_url (str): The URL of the YouTube video.

    Returns:
        dict: A dictionary containing video information and available formats.
            Keys: 'title', 'thumbnail', 'video_formats', 'audio_formats'
    """
    try:
        yt = YouTube(youtube_url)
        video_info = {
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'video_formats': yt.streams.filter(file_extension='mp4').all(),
            'audio_formats': yt.streams.filter(only_audio=True).all()
        }
        return video_info
    except RegexMatchError:
        raise ValueError("Invalid YouTube URL")


def download_media(stream, save_path, show_progress=True):
    """
    Downloads a media stream (video or audio) from YouTube.

    Args:
        stream (Stream): The media stream to download.
        save_path (str): The path to save the downloaded media file.
        show_progress (bool): Whether to show a progress bar during download.
        
    Returns:
        None
    """
    if show_progress:
        progress_bar = tqdm(
            total=stream.filesize,
            unit='B',
            unit_scale=True,
            ncols=100)
        stream.download(
            output_path=save_path,
            filename=stream.default_filename,
            filename_prefix='tmp')
        progress_bar.update(stream.filesize - progress_bar.n)
        progress_bar.close()
    else:
        stream.download(
            output_path=save_path,
            filename=stream.default_filename)


def main():
    """
    Main function to interact with the user and execute the YouTube video download process.

    This function prompts the user for a YouTube URL, extracts video information, and offers options
    to download media (video or audio) streams. The user can choose whether to show a progress bar
    during download.

    Returns:
        None  
    """
    print("Welcome to YouTube Media Downloader!")

    try:
        youtube_url = input("Enter the YouTube URL: ").strip()
      
        video_info = extract(youtube_url)

        print("\nVideo Title:", video_info['title'])
        print("Available Formats:")
        for index, stream in enumerate(video_info['video_formats'], start=1):
            print(f"{index}. {stream.resolution} - {stream.mime_type}")

        selected_option = int(
            input("\nEnter the option number to download video: "))
        selected_stream = video_info['video_formats'][selected_option - 1]

        save_path = input("Enter the directory to save the media: ")
        download_option = input(
            "Show progress bar during download? (yes/no): ").lower()
        show_progress = download_option == "yes"

        download_media(selected_stream, save_path, show_progress)
        print("Download completed!")

    except ValueError as ve:
        print("Input validation error:", ve)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()