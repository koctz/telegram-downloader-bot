import asyncio
import os
from typing import List, Dict, Any

import yt_dlp

from bot.config import DOWNLOAD_DIR

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class YouTubeService:
    def __init__(self):
        self.base_opts = {
            "quiet": True,
            "no_warnings": True,
        }

    async def get_formats(self, url: str) -> List[Dict[str, Any]]:
        """
        Возвращает список форматов с видео+аудио.
        Подходит и для обычных видео, и для Shorts.
        """
        def extract():
            with yt_dlp.YoutubeDL(self.base_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = []
                for f in info.get("formats", []):
                    # фильтруем только форматы с видео+аудио
                    if not f.get("vcodec") or not f.get("acodec"):
                        continue

                    height = f.get("height")
                    if not height:
                        continue

                    formats.append({
                        "format_id": f["format_id"],
                        "ext": f.get("ext", "mp4"),
                        "height": height,
                        "width": f.get("width"),
                        "fps": f.get("fps"),
                        "filesize": f.get("filesize") or f.get("filesize_approx"),
                    })

                # сортируем по высоте (качество) по убыванию
                formats.sort(key=lambda x: x["height"], reverse=True)
                return formats

        return await asyncio.to_thread(extract)

    async def download(self, url: str, format_id: str) -> str:
        """
        Скачивает выбранный формат и возвращает путь к файлу.
        """
        def run():
            filename_template = os.path.join(DOWNLOAD_DIR, "%(id)s_%(format_id)s.%(ext)s")
            opts = {
                **self.base_opts,
                "format": format_id,
                "outtmpl": filename_template,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        return await asyncio.to_thread(run)

