from rest_framework.routers import Route, SimpleRouter


class ListRetrieveCreateUpdateRouter(SimpleRouter):
    """
    Роутер для получения списка записей, конкретной записи добавления,
    обновления записи
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
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
            initkwargs={'suffix': 'Instance'}
        )
    ]
