from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.services.youtube_service import YouTubeService
from bot.utils.keyboards import youtube_formats_keyboard

router = Router()
yt = YouTubeService()


@router.message(F.text)
async def youtube_entry(message: Message):
    url = message.text.strip()

    if not await yt.validate(url):
        return

    info = await yt.get_info(url)
    formats = await yt.get_formats(url)

    caption = (
        f"<b>{info['title']}</b>\n"
        f"⏱ Длительность: {yt.format_duration(info['duration'])}\n\n"
        f"Выбери качество 👇"
    )

    kb = youtube_formats_keyboard(formats, url)

    await message.answer_photo(
        photo=info["thumbnail"],
        caption=caption,
        reply_markup=kb
    )


@router.callback_query(F.data.startswith("yt:"))
async def youtube_download(call: CallbackQuery):
    _, format_id, url = call.data.split(":", maxsplit=2)

    await call.answer("Скачиваю...")

    file_path = await yt.download(url, format_id)

    await call.message.answer_video(
        video=open(file_path, "rb"),
        caption="Готово 🎉"
    )
