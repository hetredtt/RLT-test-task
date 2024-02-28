import json
from aiogram import types
from aiogram.filters.command import Command
from aiogram import Router, F
from service import send_json_to_api
from utils.logger import ModuleLogger

router = Router()

logger = ModuleLogger(__name__).get_logger()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.reply(f"Hi, {user_name}!")

@router.message(F.text)
async def message_json(message: types.Message):
    if message.content_type == "text":
        try:
            json_data = json.loads(message.text)
            logger.info(f"User {message.chat.id} JSON {json_data}")
            api_response = await send_json_to_api(json_data)
            await message.reply(f"{api_response}")
        except json.JSONDecodeError:
            await message.reply("Ошибка: Неверный формат JSON.")
    else:
        await message.reply("Этот бот, примает только JSON, в текстовом формате.")
