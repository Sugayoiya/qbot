import random
from typing import Annotated

from nonebot.params import ArgStr
from nonebot.plugin import on_command

from src.utils.params.handler import get_command_str_single_arg_parser_handler

choice_helper = on_command(
    'choice_helper',
    aliases={'帮我选', '选择困难症'},
    priority=10,
    block=True,
    handlers=[get_command_str_single_arg_parser_handler('choices')]
)


@choice_helper.got('choices', prompt='有啥选项, 发来我帮你选~', )
async def handle_help_choices(choices: Annotated[str, ArgStr('choices')]):
    choices = choices.strip().split()

    if not choices:
        await choice_helper.finish('你什么选项都没告诉我, 怎么帮你选OwO')

    result = random.choice(choices)
    result_text = f'''帮你从“{'”，“'.join(choices)}”中选择了：\n\n“{result}”'''

    await choice_helper.finish(result_text)


__all__ = []
