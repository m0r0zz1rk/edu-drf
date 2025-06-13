class ExtractScansException(Exception):
    """
    Исключение, вызываемое в случае возникновения ошибки в процессе распаковки сканов удостоверений из архива
    """
    traceback = None
