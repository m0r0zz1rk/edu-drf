from rest_framework.routers import SimpleRouter, Route


class ListRetrieveUpdateDeleteRouter(SimpleRouter):
    """
    Роутер для получения списка записей, конкретной записи,
    обновления и удаления записи
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        )
    ]
