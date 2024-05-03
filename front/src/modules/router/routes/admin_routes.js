import isAdministrator from "../permissions/is_administrator.js";
import isAuthenticated from "../permissions/is_authenticated.js";

import Guides from "../../../views/admins/Guides.vue";
import Users from "../../../views/admins/Users.vue";
import Journal from "../../../views/admins/Journal.vue";
import AdminEventsView from "../../../views/admins/events/AdminEventsView.vue";
import AdminEventsManage from "../../../views/admins/events/AdminEventsManage.vue";
import AdminApps from "../../../views/admins/apps/AdminApps.vue";
import AdminAppView from "../../../views/admins/apps/AdminAppView.vue";
import Reports from "../../../views/admins/Reports.vue";

const admin_routes = [
    {
        path: '/guides',
        name: 'Guides',
        component: Guides,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/users',
        name: 'Users',
        component: Users,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/admin_events/view',
        name: 'AdminEventsView',
        component: AdminEventsView,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/admin_events/manage',
        name: 'AdminEventsManage',
        component: AdminEventsManage,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/admin_apps/',
        name: 'AdminApps',
        component: AdminApps,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/apps/admin_app_detail/:appId',
        name: 'AdminAppView',
        component: AdminAppView,
        beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/reports',
        name: 'Reports',
        component: Reports,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/journal',
        name: 'Journal',
        component: Journal,
        beforeEnter: [isAuthenticated, isAdministrator]
    }
]

export default admin_routes