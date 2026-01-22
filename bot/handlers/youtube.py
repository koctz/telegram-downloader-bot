from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.services.youtube_service import YouTubeService
from bot.utils.keyboards import youtube_formats_keyboard

router = Router()
yt_service = YouTubeService()

# простая проверка, потом можно вынести в validators
def is_youtube_url(text: str) -> bool:
    if not text:
        return False
    return any(x in text for x in ("youtube.com", "youtu.be"))

@router.message(F.text)
async def youtube_entry(message: Message):
    url = message.text.strip()

    if not is_youtube_url(url):
        # можно молча игнорировать или отвечать
        return

    await message.answer("Получаю доступные форматы... ⏳")

    try:
        formats = await yt_service.get_formats(url)
    except Exception:
        await message.answer("Не удалось получить форматы видео. Попробуй другую ссылку.")
        return

    if not formats:
        await message.answer("Не нашёл подходящих форматов для скачивания.")
        return

    kb = youtube_formats_keyboard(formats, url)
    # сохраняем URL в message, чтобы не тащить его в callback_data
    await message.answer(
        "Выбери качество видео 👇",
        reply_markup=kb
    )

    # можно сохранить url в state/БД, но для простоты — в отдельном хендлере ниже


# Простой вариант: URL берём из reply_to_message
@router.callback_query(F.data.startswith("yt:"))
async def youtube_download(call: CallbackQuery):
    format_id = call.data.split(":", maxsplit=1)[1]

    # ищем URL в сообщении, на которое бот ответил
    replied = call.message.reply_to_message if call.message else None
    if not replied or not replied.text or not is_youtube_url(replied.text.strip()):
        await call.answer("Не удалось определить ссылку на видео.", show_alert=True)
        return

    url = replied.text.strip()

    await call.answer("Скачиваю видео... ⏳", show_alert=False)

    try:
        file_path = await yt_service.download(url, format_id)
    except Exception:
        await call.message.answer("Ошибка при скачивании видео.")
        return

    try:
        await call.message.answer_video(
            video=open(file_path, "rb"),
            caption="Готово! 🎬"
        )
    except Exception:
        await call.message.answer_document(
            document=open(file_path, "rb"),
            caption="Готово! 🎬 (отправлено как файл)"
        )

