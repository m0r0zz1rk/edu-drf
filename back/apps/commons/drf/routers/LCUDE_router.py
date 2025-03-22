from rest_framework.routers import SimpleRouter, Route


class ListCreateUpdateDeleteExportRouter(SimpleRouter):

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
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        )
    ]
