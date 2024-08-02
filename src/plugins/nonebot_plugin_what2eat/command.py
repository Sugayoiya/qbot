from nonebot import logger as log
from nonebot import on_command, on_fullmatch
from nonebot.adapters.qq import Message, MessageEvent
from nonebot.params import CommandArg

from .helper import EatingManager

eating_manager = EatingManager()

eat = on_command('今天吃什么', priority=5, block=True)
drink = on_command('今天喝什么', priority=5, block=True)

eat_match = on_fullmatch('今天吃什么', priority=5, block=True)
drink_match = on_fullmatch('今天喝什么', priority=5, block=True)


@eat.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    log.info(f"event: {event}, args: {args}")
    msg = eating_manager.get2eat()
    await eat.finish(msg)


@drink.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    log.info(f"event: {event}, args: {args}")
    msg = eating_manager.get2drink()
    await eat.finish(msg)


@eat_match.handle()
async def _(event: MessageEvent):
    log.info(f"event: {event}")
    msg = eating_manager.get2eat()
    await eat.finish(msg)


@drink_match.handle()
async def _(event: MessageEvent):
    log.info(f"event: {event}")
    msg = eating_manager.get2drink()
    await eat.finish(msg)


__all__ = []
