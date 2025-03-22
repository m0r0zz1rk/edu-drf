from rest_framework.routers import SimpleRouter, Route


class ListRouter(SimpleRouter):
    """Роутер для получения списка записей"""
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
    ]
