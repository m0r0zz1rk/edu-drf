import isAuthenticated from "../permissions/is_authenticated.js";
import Events from "../../../views/users/Events.vue";
import AppView from "../../../views/users/apps/AppView.vue";
import UserApps from "../../../views/users/apps/UserApps.vue";
import UserSchedule from "../../../views/users/UserSchedule.vue";


const users_routes = [
    {
        path: '/events',
        name: 'Events',
        component: Events,
        beforeEnter: [isAuthenticated, ]
    },
    {
      path: '/user_apps',
      name: 'UserApps',
      component: UserApps,
    beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/apps/app_detail/:eventId',
        name: 'AppView',
        component: AppView,
        beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/user_schedule',
        name: 'UserSchedule',
        component: UserSchedule,
        beforeEnter: [isAuthenticated, ]
    }
]

export default users_routes