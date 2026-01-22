import asyncio
import os
import yt_dlp
from typing import Dict, Any, List

from bot.config import DOWNLOAD_DIR
from bot.services.base import BaseDownloaderService

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class YouTubeService(BaseDownloaderService):

    async def validate(self, url: str) -> bool:
        return any(x in url for x in ("youtube.com", "youtu.be"))

    async def get_info(self, url: str) -> Dict[str, Any]:
        def extract():
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get("title"),
                    "duration": info.get("duration"),
                    "thumbnail": info.get("thumbnail"),
                    "id": info.get("id"),
                }
        return await asyncio.to_thread(extract)

    async def get_formats(self, url: str) -> List[Dict[str, Any]]:
        def extract():
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = []
                for f in info["formats"]:
                    if not f.get("vcodec") or not f.get("acodec"):
                        continue
                    height = f.get("height")
                    if not height:
                        continue
                    formats.append({
                        "format_id": f["format_id"],
                        "height": height,
                        "ext": f.get("ext", "mp4"),
                        "fps": f.get("fps"),
                        "filesize": f.get("filesize") or f.get("filesize_approx"),
                    })
                formats.sort(key=lambda x: x["height"], reverse=True)
                return formats
        return await asyncio.to_thread(extract)

    async def download(self, url: str, format_id: str) -> str:
        def run():
            template = os.path.join(DOWNLOAD_DIR, "%(id)s_%(format_id)s.%(ext)s")
            opts = {
                "quiet": True,
                "format": format_id,
                "outtmpl": template,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        return await asyncio.to_thread(run)

    def format_duration(self, sec: int | None) -> str:
        if not sec:
            return "?"
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"
