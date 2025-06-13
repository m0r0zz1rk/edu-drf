import uuid
from typing import Optional

from apps.applications.exceptions.course_certificate import DuplicateCertificateInfo
from apps.applications.selectors.course_certificate import course_certificate_orm, course_certificate_model
from apps.applications.services.course_application import course_application_service


class CourseCertificateService:
    """
    Класс методов для работы с удостоверениями по заявкам на курсе
    """

    @staticmethod
    def is_certificate_exists(
        registration_number: str,
        blank_serial: str,
        blank_number: str
    ) -> bool:
        """
        Проверка на существующее удостоверение с полученными данными
        :param registration_number: Порядковый регистрационный номер
        :param blank_serial: Серия бланка удостоверения
        :param blank_number: Номер бланка удостоверения
        :return: True если удостоверение найдено в БД, иначе False
        """
        return course_certificate_orm.get_filter_records(
            filter_by=dict(
                registration_number=registration_number,
                blank_number=blank_number,
                blank_serial=blank_serial
            )).count() > 0

    @staticmethod
    def get_certificate_by_all_parameters(
            registration_number: str,
            blank_serial: str,
            blank_number: str
    ) -> Optional[course_certificate_model]:
        """
        Получение сертификата по трем параметрам
        :param registration_number: Порядковый регистрационный номер
        :param blank_serial: Серия бланка удостоверения
        :param blank_number: Номер бланка удостоверения
        :return: Запись из БД или None если запись не найдена
        """
        return course_certificate_orm.get_one_record_or_none(dict(
            registration_number=registration_number,
            blank_serial=blank_serial,
            blank_number=blank_number
        ))

    @staticmethod
    def get_certificate(attribute_name: str, value) -> Optional[course_certificate_model]:
        """
        Получение записи об удостоверении обучающегося
        :param attribute_name: наименование атрибута поиска
        :param value: значение атрибута
        :return: Запись из БД или None если запись не найдена
        """
        return course_certificate_orm.get_one_record_or_none({attribute_name: value})

    def save_certificate(self, certificate_id: uuid, certificate_data: dict):
        """
        Сохранение информации об удостоверении
        :param certificate_id: object_id удостоверения в базе
        :param certificate_data: словарь с данными об удостоверении
        :return:
        """
        if self.is_certificate_exists(
            registration_number=certificate_data.get('registration_number'),
            blank_serial=certificate_data.get('blank_serial'),
            blank_number=certificate_data.get('blank_number')
        ):
            raise DuplicateCertificateInfo
        course_certificate_orm.update_record(
            filter_by=dict(object_id=certificate_id),
            update_object=certificate_data
        )

    def generate_certificates_data(self, certificate_data: dict):
        """
        Генерация данных об удостоверениях на основе полученных данных
        :param group_id: object_id учебной группы
        :param certificate_data: словарь с данными первого удостоверения
        :return:
        """
        initial_values = {
            'registration_number': certificate_data.get('registration_number'),
            'blank_serial': certificate_data.get('blank_serial'),
            'blank_number': certificate_data.get('blank_number'),
        }
        apps = course_application_service.get_group_apps(
            certificate_data.get('group_id')
        )
        for index, app in enumerate(apps, start=0):
            if self.is_certificate_exists(
                registration_number=str(int(initial_values['registration_number'])+index),
                blank_serial=initial_values['blank_serial'],
                blank_number=str(int(initial_values['blank_number'])+index)
            ):
                raise DuplicateCertificateInfo
            cert = course_certificate_orm.get_one_record_or_none(dict(application_id=app.object_id))
            if cert:
                course_certificate_orm.update_record(
                    filter_by=dict(application_id=app.object_id),
                    update_object=dict(
                        registration_number=str(int(initial_values['registration_number']) + index),
                        blank_serial=initial_values['blank_serial'],
                        blank_number=str(int(initial_values['blank_number']) + index)
                    )
                )
            else:
                course_certificate_orm.create_record(
                    dict(
                        application_id=app.object_id,
                        registration_number=str(int(initial_values['registration_number']) + index),
                        blank_serial=initial_values['blank_serial'],
                        blank_number=str(int(initial_values['blank_number']) + index)
                    )
                )


course_certificate_service = CourseCertificateService()
