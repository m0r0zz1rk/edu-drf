from django.contrib.auth.models import User

from apps.commons.orm.base_orm import BaseORM

user_orm = BaseORM(model=User, prefetch_related=['groups'])
