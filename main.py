# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Pixeldrain-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
import pixeldrain


Bot = Client(
    "Pixeldrain-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"Hello {update.from_user.mention}, Please send a media for pixeldrain.com stream link.\n\nMade by @FayasNoushad",
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    try:
        await message.edit_text(
            text="`📥 Baixando...`",
            disable_web_page_preview=True
        )
        media = await update.download()
        await message.edit_text(
            text="`📤 Upando o Arquivo...`",
            disable_web_page_preview=True
        )
        response = pixeldrain.upload_file(media)
        status_code = response.status_code
        data = response.json()
        try:
            os.remove(media)
        except:
            pass
        await message.edit_text(
            text="`Arquivo Upado com Sucesso! ✔️`",
            disable_web_page_preview=True
        )
        if data["success"] is False:
            await message.edit_text(
                text=f"**Error {status_code}:-** Não Consegui Buscar Informacções Sobre o Seu Arquivo, Desculpe...`",
                disable_web_page_preview=True
            )
            return
    except Exception as error:
        await message.edit_text(
            text=f"Error :- <code>{error}</code>",
            disable_web_page_preview=True
        )
        return
    text = f"**File Name:** `{data['name']}`" + "\n"
    text += f"**Download Page:** `https://pixeldrain.com/u/{data['id']}`" + "\n"
    text += f"**Direct Download Link:** `https://pixeldrain.com/api/file/{data['id']}`" + "\n"
    text += f"**Upload Date:** `{data['date_upload']}`" + "\n"
    text += f"**Last View Date:** `{data['date_last_view']}`" + "\n"
    text += f"**Size:** `{data['size']}`" + "\n"
    text += f"**Total Views:** `{data['views']}`" + "\n"
    text += f"**Bandwidth Used:** `{data['bandwidth_used']}`" + "\n"
    text += f"**Mime Type:** `{data['mime_type']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Abrir LInk",
                    url=f"https://pixeldrain.com/api/file/{data['id']}"
                ),
                InlineKeyboardButton(
                    text="Compartilhar Link",
                    url=f"https://telegram.me/share/url?url=https://pixeldrain.com/api/file/{data['id']}"
                )
            ],
            [
                InlineKeyboardButton(text="Canal de Atualizações", url="https://telegram.me/BotsTelegramBrasil")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
