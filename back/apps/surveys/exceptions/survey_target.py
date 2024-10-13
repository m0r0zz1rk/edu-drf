class TargetInfoNotCorrect(Exception):
    """
    Исключение, вызываемое при некорректной информации по назначению опроса
    """
    pass


class TargetNotExists(Exception):
    """
    Ислюкчение, вызываемое при попытке обращения к несуществующему таргетированию
    """
    pass
