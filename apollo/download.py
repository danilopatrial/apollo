# download.py
# Download files from url

from __future__ import annotations

import os
import urllib.error
import pytube
import yt_dlp
import re
import urllib
import colorama
import click

from typing import Literal
from .config import get as config_get

def get_unique_filename(output_path: str, base: str, ext: str) -> str:
    i = 0
    filename = os.path.join(output_path, f"{base}{ext}")

    while os.path.exists(filename):
        i += 1
        suffix = f" (copy{f' {i}' if i > 1 else ''})"
        filename = os.path.join(output_path, f"{base}{suffix}{ext}")

    return filename


def download_via_ytdlt(url: str, filename: str, output_path: str, res: Literal['best', 'worst']) -> None:
    yt_cls: pytube.YouTube = pytube.YouTube(url)
    if res == 'best':
        video = yt_cls.streams.get_highest_resolution()
    elif res == 'worst':
        video = yt_cls.streams.get_lowest_resolution()
    video.download(output_path=output_path, filename=filename)


def download_via_pytube(url: str, filename: str, output_path: str, res: Literal['best', 'worst']) -> None:
    format_expr = {
        'best': 'bestvideo+bestaudio/best',
        'worst': 'worstvideo+worstaudio/worst'
    }[res]

    ydl_opts: dict = {
        'format': format_expr,
        'outtmpl': os.path.join(output_path, filename),
        'merge_output_format': 'mp4'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download(url: str, output_path: str | None, res: Literal['best', 'worst'], open: bool) -> str:

    colorama.init()

    pattern = r'^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}$'

    if not re.match(pattern, url):
        raise ValueError('Given URL is not a valid youtube link.')

    output_path = output_path if output_path is not None else config_get('download-output-path')
    if output_path in [None, 'None', '']:  # Handle any form of unset
        raise click.UsageError(
            "Download output path is not set.\n"
            "Use the following command to set it:\n"
            "  apollo config --set download-output-path /your/path/here"
        )

    filename: str = get_unique_filename(output_path, 'yt-download', ext='.mp4')

    try:
        print('Downloading YouTube video via pytube...')
        download_via_pytube(url, filename, output_path, res)
    except urllib.error.HTTPError:
        print('Failed to download via pytube')
        print('Downloading YouTube video via yt-dlp...')
        download_via_ytdlt(url, filename, output_path, res)

    except yt_dlp.DownloadError:
        print(f'Could not download given youtube video: {url}')
        return

    print(f'\033[1;32mDownload complete: {filename}\033[0m')

    output_path: str = os.path.join(output_path, filename)
    if open: os.startfile(output_path)
    return output_path