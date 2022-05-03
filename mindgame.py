# █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
# █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█
#
#              © Copyright 2022
#
#          https://t.me/hikariatama
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://img.icons8.com/color/344/neural_connections.png
# meta developer: @hikariatama
# scope: hikka_only

from .. import loader, utils
from ..inline.types import InlineCall
from telethon.tl.types import Message
import logging
import random
import grapheme

logger = logging.getLogger(__name__)
EMOJIES = utils.chunks(
    list(
        grapheme.graphemes(
            "😌☺️😞😔🧑‍🏫👨‍🏫👨‍💻🧑‍💻"
            "🤵‍♂️🤵👩‍🚀🧑‍🚀👨‍🚒🧑‍🚒👨‍⚖️🧑‍⚖️"
            "🧟🧟‍♀️🦹🦹‍♀️🌇🌆🦸🦸‍♂️"
            "🧙🧙‍♀️🧚🧚‍♂️👯‍♀️👯👭👫"
            "👨‍👩‍👦👨‍👩‍👧👨‍🏭🧑‍🏭👳👳‍♂️🧑👨"
            "🕵️🕵️‍♂️🧑‍🌾👨‍🌾👨‍⚕️🧑‍⚕️🕵️🕵️‍♂️"
            "👨‍🍳🧑‍🍳🧑‍🔬👨‍🔬🧝‍♀️🧝‍♂️💏👨‍❤️‍💋‍👨"
        )
    ),
    2,
)


@loader.tds
class MindGameMod(loader.Module):
    """Train your brain and mind"""

    strings = {
        "name": "MindGame",
        "header": "🎮 <b>Find an emoji, that differs from others</b>\n<i>You've completed {} levels!</i>",
    }

    strings_ru = {
        "header": "🎮 <b>Найди эмодзи, который отличается от других</b>\n<i>Ты прошел {} уровней!</i>"
    }

    _ratelimit = []

    def _generate_markup(self, counter: int) -> list:
        fail_emoji, next_step_emoji = random.choice(EMOJIES)
        markup = [
            {"text": fail_emoji, "callback": self._incorrect} for _ in range(8**2 - 1)
        ] + [
            {
                "text": next_step_emoji,
                "callback": self._next_step_callback,
                "args": (counter + 1,),
            }
        ]
        random.shuffle(markup)
        return utils.chunks(markup, 8)

    async def mindgamecmd(self, message: Message):
        """Open a new mindgame"""
        await self.inline.form(
            message=message,
            text=self.strings("header").format(0),
            reply_markup=self._generate_markup(0),
            disable_security=True,
        )

    async def _next_step_callback(self, call: InlineCall, counter: int):
        if call.from_user.id != self._tg_id and call.from_user.id in self._ratelimit:
            await call.answer("You've spent your chance...")
            return

        await call.edit(
            self.strings("header").format(counter),
            self._generate_markup(counter),
        )

        await call.answer("Correct!")

        self._ratelimit = []

    async def _incorrect(self, call: InlineCall):
        if call.from_user.id != self._tg_id:
            if call.from_user.id in self._ratelimit:
                await call.answer("You've spent your chance...")
                return

            self._ratelimit += [call.from_user.id]

        await call.answer("NO!")