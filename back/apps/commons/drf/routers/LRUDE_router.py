from rest_framework.routers import SimpleRouter, Route


class ListRetrieveUpdateDeleteExportRouter(SimpleRouter):
    """
    Роутер для получения списка записей, конкретной записи,
    обновления, удаления записи, выгрузки в Excel
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
            url=r'^{prefix}/export/$',
            mapping={
                'get': 'export',
            },
            name='{basename}-export',
            detail=False,
            initkwargs={'suffix': 'Export'}
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
