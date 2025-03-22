from docxtpl import DocxTemplate


def generate_word_file(template_path: str, context: dict) -> DocxTemplate:
    """
    Генерация вордовского файла
    :param template_path: Путь к шаблону файла
    :param context: Словарь с данными (ключ - тэг в шаблоне, значение - значение для подстановки)
    :return: файл Word
    """
    doc = DocxTemplate(template_path)
    doc.render(context)
    return doc
