from django.apps import apps
from django.contrib.auth.models import User

from apps.commons.services.ad.ad_centre import AdCentreService
from apps.commons.utils.ldap import ldap_utils

ad_centre_coko_user_model = apps.get_model('commons', 'AdCentreCokoUser')


class AdCentreCokoUserUtils:
    """Класс методов для работы с моделью AdCentreCokoUser"""

    @staticmethod
    def is_ad_centre_coko_user_exists(user: User):
        """
        Проверка на существующую для полученного пользователя запись
        :param user: Пользователь Django
        :return:
        """
        return ad_centre_coko_user_model.objects.filter(coko_user=user).exists()

    def add_rec(self, user: User, display_name: str):
        """
        Добавление записи в таблицу
        :param user: Пользователь Django
        :param display_name: Наименование подразделения-центра из AD
        :return:
        """
        if not self.is_ad_centre_coko_user_exists(user):
            acu = AdCentreService()
            ad_centre = acu.get_ad_centre(
                'display_name',
                display_name
            )
            if ad_centre is not None:
                ad_centre_coko_user_model.objects.update_or_create(
                    coko_user=user,
                    ad_centre=ad_centre
                )

    def get_user_centre_display_name(self, user: User) -> str:
        """
        Получение пользовательского подразделения-центра из AD
        :param user: Пользователь Django
        :return: Наименование подразделения, "-" - если не найдено
        """
        if self.is_ad_centre_coko_user_exists(user):
            rec = ad_centre_coko_user_model.objects.get(coko_user=user)
            if rec.ad_centre is not None:
                return rec.ad_centre.display_name
        return '-'

    @staticmethod
    def get_centre_user_ids_by_display_name(display_name: str) -> list:
        return ad_centre_coko_user_model.objects.filter(
            ad_centre__display_name__icontains=display_name
        ).values_list('coko_user_id', flat=True)

    def refresh_rec(self, user: User):
        """
        Обновление информации о подразделении пользователя
        :param user: Пользователь Django
        :return:
        """
        if self.is_ad_centre_coko_user_exists(user):
            ad_centre_coko_user_model.objects.get(coko_user=user).delete()
            self.add_rec(
                user,
                ldap_utils.get_ad_user_centre(user)
            )


ad_centre_coko_user_utils = AdCentreCokoUserUtils()
