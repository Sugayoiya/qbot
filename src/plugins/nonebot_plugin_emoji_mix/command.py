import re

import emoji
from nonebot import logger as log
from nonebot import on_regex
from nonebot.adapters.qq import Message, MessageEvent, MessageSegment
from nonebot.params import CommandArg
from nonebot.params import RegexDict
from nonebot.plugin import on_command

from .helper import EmojiMixManager

emojis = emoji.EMOJI_DATA.keys()
pattern = "(" + "|".join(re.escape(e) for e in emojis) + ")"
emoji_mix_manager = EmojiMixManager()

emoji_mix = on_regex(rf"^\s*(?P<code1>{pattern})\s*\+\s*(?P<code2>{pattern})\s*$", priority=5, block=True)

emoji_mix_random = on_command('emoji合成', priority=5, block=True)


@emoji_mix.handle()
async def handle_emoji_mix(event: MessageEvent, msg: dict = RegexDict()):
    e1 = msg['code1']
    e2 = msg['code2']
    url = None
    try:
        url = emoji_mix_manager.get_combination_url(e1, e2)
    except Exception as e:
        await emoji_mix.finish(f'{e}')

    if not url:
        await emoji_mix.finish(f'不支持的emoji组合:{e1}+{e2}')

    # res = await Requests(timeout=10).get(url=url)
    # if res.status_code != 200:
    #     await emoji_mix.send('emoji合成出错，请稍后再试')
    #     return

    await emoji_mix.send(MessageSegment.image(url))


@emoji_mix_random.handle()
async def handle_guess(event: MessageEvent, args: Message = CommandArg()):
    log.info(f"event: {event}, args: {args}")
    combination = emoji_mix_manager.get_random_combination()

    e1 = combination['leftEmoji']
    e2 = combination['rightEmoji']
    url = combination['gStaticUrl']

    # res = await Requests(timeout=10).get(url=url)
    # if res.status_code != 200:
    #     await emoji_mix_random.finish('emoji融合出错，请稍后再试')

    await emoji_mix_random.send(MessageSegment.image(url) + f'\n随机融合by{e1} + {e2}')
