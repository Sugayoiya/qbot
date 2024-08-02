class BotException(Exception):
    """所有 Omega 异常的基类"""


class DatabaseException(BotException):
    """数据库异常"""


class LocalSourceException(BotException):
    """本地资源异常"""


class WebSourceException(BotException):
    """网络资源异常"""


class BotApiException(BotException):
    """[Deactivated]OneBot API 异常"""


class PlatformException(BotException):
    """平台中间件异常"""


class PluginException(BotException):
    """由插件自定义的异常"""


__all__ = [
    'BotException',
    'DatabaseException',
    'LocalSourceException',
    'WebSourceException',
    'BotApiException',
    'PlatformException',
    'PluginException'
]
