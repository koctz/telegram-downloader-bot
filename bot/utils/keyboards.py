from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil


def human_size(size):
    if not size:
        return "?"
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{ceil(size)} {unit}"
        size /= 1024
    return f"{ceil(size)} TB"


def youtube_formats_keyboard(formats):
    rows = []
    for f in formats:
        text = (
            f"🎞 {f['height']}p"
            f" • {f['fps'] or '?'}fps"
            f" • {f['ext']}"
            f" • {human_size(f['filesize'])}"
        )
        rows.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"yt:{f['format_id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)
