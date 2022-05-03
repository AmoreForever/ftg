# █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
# █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█
#
#              © Copyright 2022
#
#          https://t.me/hikariatama
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://img.icons8.com/fluency/48/000000/dota.png
# meta developer: @hikariatama
# scope: inline
# scope: hikka_only
# scope: hikka_min 1.1.6

from .. import loader
from telethon.tl.types import Message


@loader.tds
class InlineGhoulMod(loader.Module):
    """Non-spammy ghoul module"""

    strings = {"name": "InlineGhoul", "tired": "😾 <b>Tired of counting!</b>"}

    strings_ru = {
        "tired": "😾 <b>Я устал считать!</b>",
        "_cmd_doc_ghoul": "Отправляет сообщение Гуля",
        "_cls_doc": "Неспамящий модуль Гуль",
    }

    async def ghoulcmd(self, message: Message):
        """Sends ghoul message"""
        await self.animate(
            message,
            [f"👊 <b>{x} - 7 = {x - 7}</b>" for x in range(1000, 900, -7)]
            + [self.strings("tired")],
            interval=1,
            inline=True,
        )
