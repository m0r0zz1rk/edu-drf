from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service
from apps.users.serializers.service import profile_service


def change_curator_groups(request, serialize_data: dict):
    """
    Изменение отображения только кураторских групп у сотрудников ЦОКО
    :param request: Объект запроса из DRF
    :param serialize_data: Полученные данные из сериализатора
    :return:
    """
    prof = profile_service.get_profile_or_info_by_attribute(
        'object_id',
        serialize_data['object_id'],
        'profile'
    )
    if not prof:
        journal_service.create_journal_rec(
            {
                'source': 'Внешний запрос',
                'module': GUIDES,
                'status': ERROR,
                'description': 'Ошибка при изменении кураторских групп - профиль не найден'
            },
            serialize_data,
            None
        )
        return response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')
    data = {}
    for key in ['surname', 'name', 'patronymic']:
        data[key] = getattr(prof, key)
    data['curator_groups'] = serialize_data['curator_groups']
    proc = profile_service.set_coko_profile_data(
        prof,
        data
    )
    if isinstance(proc, bool):
        if proc:
            journal_service.create_journal_rec(
                {
                    'source': profile_service.get_profile_or_info_by_attribute(
                        'django_user_id',
                        request.user.id,
                        'display_name'
                    ),
                    'module': GUIDES,
                    'status': SUCCESS,
                    'description': 'Параметр отображения кураторских групп успешно изменен'
                },
                repr(serialize_data),
                None
            )
            return response_utils.ok_response('Информация успешно обновлена')
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Процесс установки параметров профилю сотрудников',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при изменении кураторских групп - данные не прошли валидацию'
                },
                repr(data),
                None
            )
            return response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')
    else:
        journal_service.create_journal_rec(
            {
                'source': 'Процесс установки параметров профилю сотрудников',
                'module': GUIDES,
                'status': ERROR,
                'description': 'Ошибка при изменении кураторских групп - данные не прошли валидацию'
            },
            repr(data),
            None
        )
        return response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')
