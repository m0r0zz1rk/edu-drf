from rest_framework.routers import SimpleRouter, Route


class ListRetrieveUpdateExportRouter(SimpleRouter):
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
            },
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        )
    ]
