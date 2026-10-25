#!/usr/bin/env python3
"""
Playlist Downloader (Windows)
Downloads videos from a YouTube playlist you are authorized to download.
MP3 extraction requires FFmpeg installed and available on PATH.
"""

from pathlib import Path
import sys

try:
    import yt_dlp
except ImportError:
    print("Missing dependency: yt-dlp")
    print("Install it with: py -m pip install -U yt-dlp")
    input("\nPress Enter to exit...")
    sys.exit(1)


def main():
    print("=" * 58)
    print("       YouTube Playlist Downloader")
    print("=" * 58)
    url = input("\nPaste the YouTube playlist URL: ").strip()
    if not url:
        print("No URL provided.")
        input("\nPress Enter to exit...")
        return

    print("\nChoose download type:")
    print("  1. MP3 audio files")
    print("  2. MP4 video files")
    choice = input("Enter 1 or 2 [default 1]: ").strip() or "1"
    if choice not in ("1", "2"):
        print("Invalid choice.")
        input("\nPress Enter to exit...")
        return

    default_folder = Path.home() / "Downloads" / "YouTube Playlist"
    folder_text = input(f"\nSave folder [{default_folder}]: ").strip()
    folder = Path(folder_text).expanduser() if folder_text else default_folder
    folder.mkdir(parents=True, exist_ok=True)

    archive_file = folder / "downloaded_archive.txt"
    common = {
        "outtmpl": str(folder / "%(playlist_index)03d - %(title).180B.%(ext)s"),
        "noplaylist": False,
        "ignoreerrors": True,
        "continuedl": True,
        "retries": 5,
        "fragment_retries": 5,
        "download_archive": str(archive_file),
        "windowsfilenames": True,
        "trim_file_name": 180,
        "quiet": False,
        "no_warnings": False,
    }

    if choice == "1":
        common.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
        print("\nDownloading playlist audio as MP3...")
        print("Note: FFmpeg must be installed and available on PATH.")
    else:
        common.update({
            "format": "bestvideo*+bestaudio/best",
            "merge_output_format": "mp4",
        })
        print("\nDownloading playlist videos as MP4 where supported...")

    print(f"Save location: {folder}\n")
    try:
        with yt_dlp.YoutubeDL(common) as downloader:
            downloader.download([url])
        print("\nFinished processing the playlist.")
        print(f"Files are in: {folder}")
        print("Items listed in downloaded_archive.txt are skipped on future runs.")
        print("If some videos failed, check the messages above and try again later.")
    except Exception as exc:
        print(f"\nThe download could not be completed: {exc}")
        print("Check the playlist URL, internet connection, and yt-dlp/FFmpeg installation.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
