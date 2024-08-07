from dataclasses import dataclass

from nonebot import logger
from pydantic import ValidationError

from src.resource import StaticResource

sources = {
    "gitlab": {
        "custom": "https://gitlab.com/infinitefusion/sprites/-/raw/master/CustomBattlers/{n}/",
        "autogen": "https://gitlab.com/infinitefusion/sprites/-/raw/master/Battlers/",
        "count": 420
    },
    "expansion": {
        "custom": "https://gitlab.com/pokemoninfinitefusion/customsprites/-/raw/master/CustomBattlers/",
        "autogen": "https://gitlab.com/pokemoninfinitefusion/autogen-fusion-sprites/-/raw/master/Battlers/",
        "count": 470
    }
}

configs = {"enable_transparent": False,
           "source": "expansion"}


@dataclass
class PokemonLocalResourceConfig:
    """宝可梦文件配置"""

    # 默认内置的静态资源文件路径
    pokemons: StaticResource = StaticResource('doc', 'pokemon', 'pokemons.json')


try:
    pokemon_local_resource_config = PokemonLocalResourceConfig()
except ValidationError as e:
    import sys

    logger.opt(colors=True).critical(f'<r> pokemon 插件配置格式验证失败</r>, 错误信息:\n{e}')
    sys.exit(f'pokemon 插件配置格式验证失败, {e}')

__all__ = [
    'pokemon_local_resource_config',
    'sources',
    'configs'
]
