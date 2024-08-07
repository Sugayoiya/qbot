from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='帮我选',
    description='【选择困难症帮助器插件】\n'
                '是否还在为选择困难症发愁?\n'
                '让困难症帮助器解决你的烦恼!',
    usage='/帮我选 [选项1] [选项2]...',
    extra={'author': 'sugayoiya'},
)

from . import command as command

__all__ = []
