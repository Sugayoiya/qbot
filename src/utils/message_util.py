from typing import List, Union

from nonebot_plugin_saa import MessageSegmentFactory, Text, Image  # noqa: E402


def is_image(msg: str) -> bool:
    return msg[-4:].lower() in [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        "jfif",
        "webp",
    ]


def flatten(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            yield from flatten(i)
        else:
            yield i


def format_msg(msg_list: List[Union[List[str], str]], is_plain_text: bool = False):
    flatten_msg_list = list(flatten(msg_list))
    if is_plain_text:
        return "".join([i for i in flatten_msg_list if not is_image(i)])

    msg: List[MessageSegmentFactory] = []

    for i in flatten_msg_list:
        if not i:
            continue
        elif is_image(i):
            msg.append(Image(i))
        else:
            msg.append(Text(i))
    return msg
