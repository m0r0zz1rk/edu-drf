import os
import uuid

import docx
from django.core.mail import EmailMessage
from docxcompose.composer import Composer
from docxtpl import DocxTemplate, InlineImage

from apps.applications.services.course_application import course_application_service
from apps.applications.services.course_certificate import course_certificate_service
from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.data_types.date import date_utils
from apps.commons.utils.django.settings import settings_utils
from apps.commons.utils.ldap import ldap_utils
from apps.edu.services.student_group import student_group_service
from web_app.init_celery import app

# Путь к шаблону сертификата
template_path = os.path.join(
    settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
    'Шаблоны',
    'Файл печати',
    'шаблон.docx'
)

# Путь к пустому файлу-основе
main_path = os.path.join(
    settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
    'Шаблоны',
    'Файл печати',
    'основа.docx'
)

# Путь к папке с подписями
sings_path = os.path.join(
    settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
    'Шаблоны',
    'Подписи'
)

# Путь к папке с файлами на печать
print_path = os.path.join(
    settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
    'Печать'
)


@app.task
def email_print_file(group_id: uuid, admin_email: str, to_print_office: bool):
    """
        Задача Celery для формирования файла печати и отправка его получателям
        :param group_id: object_id учебной группы
        :param admin_email: Email администратора для отправки письма
        :param to_print_office: Параметр отправки письма в типографию
        :return:
    """

    @journal_celery_task(
        'Задача на получение файла печати успешно выполнена',
        'Задача на получение файла печати завершилась ошибкой'
    )
    def wrapper():
        group = student_group_service.get_student_group('object_id', group_id)

        # Создание папки (при необходимости) для файла печати
        group_path = os.path.join(print_path, group.code.strip())
        if not os.path.exists(group_path):
            os.makedirs(group_path)

        # Получение общих параметров по мероприятию
        date_start = group.ou.date_start
        date_end = group.ou.date_end
        all_centres = ldap_utils.get_departments_with_managers()
        manager_fio = all_centres.get(group.ou.program.department.display_name, '').split(' ')
        manager = f'{manager_fio[1][0]}.{manager_fio[2][0]}. {manager_fio[0]}'
        sign_descriptor = os.path.join(sings_path, f'{manager}.png')
        context = {
            'name_dpp': group.ou.program.name,
            'duration': group.ou.program.duration,
            'date_give': group.ou.date_end.strftime('%d.%m.%Y'),
            'day_start': date_start.strftime('%d'),
            'month_start': date_utils.get_month_genitive_case(date_start.strftime('%B')),
            'year_start': date_start.strftime('%Y'),
            'day_end': date_end.strftime('%d'),
            'month_end': date_utils.get_month_genitive_case(date_end.strftime('%B')),
            'year_end': date_end.strftime('%Y'),
            'manager': manager,
        }

        # Получение файла основы
        main = docx.Document(main_path)

        # Получение заявок, перебор по ним и создание файла на основе шаблона
        # с подстановкой общих параметров и данных об обучающемся
        # Далее добавление в файл основы созданного сертификата
        apps = course_application_service.get_group_apps(group_id)
        for app in apps:
            try:
                certificate = course_certificate_service.get_certificate('application_id', app.object_id)
                if not certificate:
                    continue
                doc = DocxTemplate(template_path)
                profile = app.profile
                context['fio'] = f'{profile.surname} {profile.name} {profile.patronymic}'
                context['reg_number'] = certificate.registration_number
                context['sign'] = InlineImage(doc, image_descriptor=sign_descriptor)
                # context['sign'] = InlineImage(doc, image_descriptor=sign_descriptor)
                doc.render(context)
                # Сохранение временного файла с данным о сертификате
                doc.save(os.path.join(group_path, "new_cert.docx"))
                # Объявление композера с основным файлом
                composer = Composer(main)
                # Открытие временного файла с данным о сертификате
                doc2 = docx.Document(os.path.join(group_path, "new_cert.docx"))
                # Вставка файла с данными о сертификате в основной файл
                composer.append(doc2)
                # Сохранение обновленного файла основы
                composer.save(os.path.join(group_path, 'Печать.docx'))
                # Удаление временного файла
                os.remove(os.path.join(group_path, "new_cert.docx"))
            except Exception:
                continue
        email_address = [admin_email, ]
        # email_address = [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ]
        if to_print_office:
            email_address.append(settings_utils.get_parameter_from_settings('PRINT_OFFICE_EMAIL'))
        email = EmailMessage(
            "АИС «Учебный центр»: Файл печати удостоверений",
            f"Во вложении находится сформированный файл для печати удостоверений группы {group.code}.",
            None,
            email_address
        )
        email.attach_file(os.path.join(group_path, 'Печать.docx'))
        email.send()
        return f'Файл печати {group.code} успешно отправлен'

    wrapper()
