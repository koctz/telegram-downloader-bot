from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil

def human_size(size: int | None) -> str:
    if not size:
        return "?"
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{ceil(size)} {unit}"
        size /= 1024
    return f"{ceil(size)} TB"

def youtube_formats_keyboard(formats, url: str) -> InlineKeyboardMarkup:
    rows = []
    for f in formats:
        height = f["height"]
        fps = f.get("fps") or "?"
        ext = f["ext"]
        size = human_size(f.get("filesize"))

        text = f"{height}p {fps}fps • {ext} • {size}"
        cb_data = f"yt:{f['format_id']}"

        rows.append([InlineKeyboardButton(text=text, callback_data=cb_data)])

    # можно сделать пагинацию позже, если форматов слишком много
    return InlineKeyboardMarkup(inline_keyboard=rows)

