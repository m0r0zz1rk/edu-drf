import isAuthenticated from "../permissions/is_authenticated.js";
import Courses from "@/views/users/Courses.vue";
import Events from "@/views/users/Events.vue";
import DetailApp from "@/views/users/apps/DetailApp.vue";
import ActiveApps from "@/views/users/ActiveApps.vue";
import ArchiveApps from "@/views/users/ArchiveApps.vue";


const users_routes = [
    // {
    //     path: '/student/events',
    //     name: 'Events',
    //     component: Events,
    //     beforeEnter: [isAuthenticated, ]
    // },
    {
        path: '/student/events',
        name: 'Events',
        component: Events,
        beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/student/courses',
        name: 'Courses',
        component: Courses,
        beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/student/app/:serviceType/:appId',
        name: 'DetailApp',
        component: DetailApp,
        beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/student/active_apps',
        name: 'ActiveApps',
        component: ActiveApps,
        beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/student/archive_apps',
        name: 'ArchiveApps',
        component: ArchiveApps,
        beforeEnter: [isAuthenticated, ]
    },
    // {
    //   path: '/user_apps',
    //   name: 'UserApps',
    //   component: UserApps,
    // beforeEnter: [isAuthenticated, ]
    // },
    // {
    //     path: '/apps/app_detail/:eventId',
    //     name: 'AppView',
    //     component: AppView,
    //     beforeEnter: [isAuthenticated, ]
    // },
    // {
    //     path: '/user_schedule',
    //     name: 'UserSchedule',
    //     component: UserSchedule,
    //     beforeEnter: [isAuthenticated, ]
    // }
]

export default users_routes