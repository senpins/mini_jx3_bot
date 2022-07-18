from nonebot import on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.params import Depends, RegexDict
from nonebot.plugin import PluginMetadata

from src.params import PluginConfig, cost_gold
from src.utils.log import logger

from .data_source import get_weather

__plugin_meta__ = PluginMetadata(
    name="天气查询",
    description="查询天气，使用和风天气",
    usage="XX天气 | 天气 XX",
    config=PluginConfig(cost_gold=10),
)


def get_city(regex_dict: dict = RegexDict()):
    """获取命令中城市名"""
    return regex_dict["vlue1"] if regex_dict["value1"] else regex_dict["value2"]


weather_regex = r"^(?P<value1>[\u4e00-\u9fa5]+)天气$|^天气 (?P<value2>[\u4e00-\u9fa5]+$)"
weather = on_regex(pattern=weather_regex, permission=GROUP, priority=5, block=True)


@weather.handle(parameterless=[cost_gold(gold=10)])
async def _(event: GroupMessageEvent, city: str = Depends(get_city)):
    """查询天气"""
    logger.info(f"<y>群{event.group_id}</> | <g>{event.user_id}</g> | 请求：{city}")
    msg = await get_weather(city)
    await weather.finish(msg)
