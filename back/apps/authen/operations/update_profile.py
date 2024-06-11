from apps.authen.operations.base_operation_profile import BaseOperationProfile
from apps.commons.processes.db.add_update_database_record import AddUpdateDataBaseRecord
from apps.guides.services.state import StateService


class UpdateProfile(BaseOperationProfile):
    """Обновление профиля пользователя"""

    update_profile_complete = False

    def action(self):
        profile_data = {}
        for k, v in self.object_data.items():
            if k != 'email':
                if k == 'state':
                    state = StateService().get_state_by_name(v)
                    profile_data[k] = state
                else:
                    profile_data[k] = v
        profile_process_data = {
            'source': self.source,
            'module': self.module,
            'process_data': {
                'model_info': {
                    'app': 'authen',
                    'model_name': self.model_name
                },
                'object': profile_data
            }
        }
        proc = AddUpdateDataBaseRecord(profile_process_data)
        if proc.process_completed:
            user_process_data = {
                'source': self.source,
                'module': self.module,
                'process_data': {
                    'model_info': {
                        'app': 'django',
                        'model_name': 'user'
                    },
                    'object': {
                        'id': self.object_data['django_user'].id,
                        'email': self.object_data['email']
                    }
                }
            }
            proc = AddUpdateDataBaseRecord(user_process_data)
            if proc.process_completed:
                self.update_profile_complete = True
                return True
        self.update_profile_complete = False
