import isAdministrator from "../permissions/is_administrator.js";
import isAuthenticated from "../permissions/is_authenticated.js";

import Journal from "../../../views/administrator/Journal.vue";
import Guides from "@/views/administrator/Guides.vue";
import Users from "@/views/administrator/Users.vue";
import Edu from "@/views/administrator/Edu.vue";

const centre_routes = [
    {
      path: '/centre/users',
      name: 'Users',
      component: Users,
      beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/centre/guides',
        name: 'Guides',
        component: Guides,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
      path: '/centre/edu',
      name: 'Edu',
      component: Edu,
      beforeEnter: [isAuthenticated, isAdministrator]
    },
    /*{
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
    },*/
    {
        path: '/centre/journal',
        name: 'Journal',
        component: Journal,
        beforeEnter: [isAuthenticated, isAdministrator]
    }
]

export default centre_routes
