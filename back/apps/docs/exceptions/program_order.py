class ProgramOrderFieldNotFound(Exception):
    """
    Исключение, вызываемое в случае отсутствия обязательного поля
    при работе с приказом ДПП
    """
    field_name = ''
