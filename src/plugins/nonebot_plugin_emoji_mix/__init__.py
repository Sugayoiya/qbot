from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='emoji合成',
    description='【emoji合成】\n'
                '😀+😀=?',
    usage='直接发送 emoji+emoji \n'
          '或使用 /emoji合成 随机合成一个emoji',
    extra={'author': 'sugayoiya'},
)

from . import command as command

__all__ = []
