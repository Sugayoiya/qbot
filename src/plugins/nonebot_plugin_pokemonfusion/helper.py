import difflib
import random
from io import BytesIO
from typing import Any, Optional
from typing import Dict

import ujson as json
from PIL import Image
from nonebot import logger

from src.resource import TemporaryResource
from src.utils.request_utils.requests import Requests
from .config import pokemon_local_resource_config, sources, configs


def _load_config(file: TemporaryResource) -> Optional[Dict[str, Any]]:
    """从文件读取求签事件"""
    if file.is_file:
        logger.debug(f'loading fortune event form {file}')
        with file.open('r', encoding='utf8') as f:
            eat_config = json.loads(f.read())
        return eat_config
    else:
        return None


pokemon_json = _load_config(pokemon_local_resource_config.pokemons)


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def get_3_similar_names(mylist, name):
    new_list = mylist.copy()
    similarity_list = [string_similar(i, name) for i in new_list]
    sorted_list = sorted(similarity_list, reverse=True)
    result_list = []
    for i in range(3):
        result_list.append(new_list[similarity_list.index(sorted_list[0])])
        similarity_list.remove(sorted_list[0])
        sorted_list.pop(0)
        new_list.remove(result_list[i])
    return result_list


def res2_bytes_io(res):
    if configs["enable_transparent"]:
        return BytesIO(res.content)
    else:
        im = Image.open(BytesIO(res.content)).convert("RGBA")
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0), mask=im)
        new_im = BytesIO()
        p.save(new_im, format="png")
        return new_im


async def get_image(fusion_id):
    head_id = fusion_id.split(".")[0]
    fusion_url = sources[configs["source"]]["custom"].format(n=head_id) + fusion_id
    logger.info(fusion_url)
    res = await Requests(timeout=10).get(url=fusion_url)
    if res.status_code != 404:
        return res2_bytes_io(res)
    else:
        fallback_fusion_url = sources[configs["source"]]["autogen"] + head_id + "/" + fusion_id
        res = await Requests(timeout=10).get(url=fallback_fusion_url)
        if res.status_code != 404:
            return res2_bytes_io(res)
        else:
            res_finally = await Requests(timeout=10).get(
                url="https://infinitefusion.gitlab.io/pokemon/question.png")
            return res2_bytes_io(res_finally)


async def get_image_url(fusion_id):
    head_id = fusion_id.split(".")[0]
    fusion_url = sources[configs["source"]]["custom"].format(n=head_id) + fusion_id
    logger.info(fusion_url)
    res = await Requests(timeout=10).get(url=fusion_url)
    if res.status_code != 404:
        return fusion_url
    else:
        fallback_fusion_url = sources[configs["source"]]["autogen"] + head_id + "/" + fusion_id
        res = await Requests(timeout=10).get(url=fallback_fusion_url)
        if res.status_code != 404:
            return fallback_fusion_url
        else:
            question_url = "https://infinitefusion.gitlab.io/pokemon/question.png"
            res_finally = await Requests(timeout=10).get(
                url=question_url)
            return question_url


def handle_pokemon_id(pokemon_id: str):
    pid = pokemon_json[pokemon_id]
    return pid if isinstance(pid, int) else random.choice(pid)


def pokemon_prompt_handle(pokemons: str):
    msgs = []
    fusion_ids = []
    pokemon_list = pokemons.split("+")
    count = sources[configs["source"]]["count"]
    if len(pokemon_list) == 2:
        for pokemon in pokemon_list:
            if pokemon not in pokemon_json:
                msgs.append(
                    f"未找到 {pokemon}！尝试以下结果：{'、'.join(get_3_similar_names(list(pokemon_list), pokemon))} ")
        if False not in [name in pokemon_json for name in pokemon_list]:
            f_id_1 = handle_pokemon_id(pokemon_list[0])
            f_id_2 = handle_pokemon_id(pokemon_list[1])
            fusion_ids = [f"{f_id_1}.{f_id_2}.png",
                          f"{f_id_2}.{f_id_1}.png"]
    elif len(pokemon_list) == 1 and pokemon_list != ['']:
        pokemon = pokemon_list[0]
        if pokemon not in pokemon_json:
            msgs = f"未找到 {pokemon}！尝试以下结果：{'、'.join(get_3_similar_names(list(pokemon_list), pokemon))} "
        else:
            a = random.randint(1, count)
            b = handle_pokemon_id(pokemon)
            fusion_ids = [f"{b}.{a}.png", f"{a}.{b}.png"]
    elif pokemon_list == ['']:
        a = random.randint(1, count)
        b = random.randint(1, count)
        fusion_ids = [f"{b}.{a}.png", f"{a}.{b}.png"]
    try:
        msgs = [fusion_id for fusion_id in set(fusion_ids)]
    except:
        pass
    return msgs


__all__ = [
    get_image,
    pokemon_prompt_handle
]
