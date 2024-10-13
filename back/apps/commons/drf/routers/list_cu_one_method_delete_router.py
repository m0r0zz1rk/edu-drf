from rest_framework import routers
from rest_framework.routers import Route


class ListCUOneMethodDeleteRouter(routers.SimpleRouter):
    """
        Роутер для получения списка записей, удаления записей и реализуюзий метод
        добавления и обновления записей одним методом
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create_update'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'delete': 'destroy'
            },
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        )
    ]
