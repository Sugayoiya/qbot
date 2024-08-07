from typing import Annotated

from nonebot.adapters.qq import Message
from nonebot.log import logger
from nonebot.params import ArgStr
from nonebot.plugin import on_command
from nonebot_plugin_saa import MessageFactory, Image

from src.utils.params.handler import get_command_str_single_arg_parser_handler
from .helper import pokemon_prompt_handle, get_image_url

pokemon = on_command(
    '宝可梦融合',
    aliases={'pokemon_fusion'},
    handlers=[get_command_str_single_arg_parser_handler('pokemons')],
    priority=10,
    block=True
)


@pokemon.got('pokemons', prompt='想要融合什么宝可梦? 发来给你看看:')
async def handle_guess(pokemons: Annotated[str, ArgStr('pokemons')]):
    pokemons_list = pokemons.strip()
    try:
        pokemon_ids = pokemon_prompt_handle(pokemons_list)
        try:
            if isinstance(pokemon_ids, list):
                msgs = [(await get_image_url(pokemon_id)) for pokemon_id in pokemon_ids]
                # await MessageFactory(format_msg(msgs)).finish()
                [await MessageFactory(Image(msg)).send() for msg in msgs]
            elif isinstance(pokemon_ids, str):
                await pokemon.finish(Message(pokemon_ids))
        except:
            pass
    except Exception as e:
        logger.error(f'pokemon fusion结果失败, {e!r}')
        await pokemon.send('发生了意外的错误, 请稍后再试')
