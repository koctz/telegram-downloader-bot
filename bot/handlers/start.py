from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(commands={"start"})
async def cmd_start(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Отправь ссылку на YouTube видео или Shorts, "
        "и я предложу варианты качества для скачивания."
    )

