from rest_framework.routers import SimpleRouter, Route


class ListRetrieveUpdateRouter(SimpleRouter):
    """Роутер для получения списка записей, добавления и обновления записи"""
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update'
            },
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Update'}
        )
    ]
