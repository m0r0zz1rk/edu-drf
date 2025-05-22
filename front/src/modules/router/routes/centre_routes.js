import isAdministrator from "../permissions/is_administrator.js";
import isAuthenticated from "../permissions/is_authenticated.js";

import Journal from "../../../views/administrator/Journal.vue";
import Guides from "@/views/administrator/Guides.vue";
import Users from "@/views/administrator/Users.vue";
import Edu from "@/views/administrator/Edu.vue";
import EduDetailStudentGroup from "@/views/administrator/edu/EduDetailStudentGroup.vue";
import Surveys from "@/views/administrator/Surveys.vue";
import Reports from "@/views/administrator/Reports.vue";
import PersonalSchedule from "@/views/administrator/PersonalSchedule.vue";
import {isDepOrAdministrator} from "@/modules/router/permissions/is_dep_or_admin";

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
      beforeEnter: [isAuthenticated, isDepOrAdministrator]
    },
    {
      path: '/centre/edu/student-group/:groupId',
      name: 'EduDetailStudentGroup',
      component: EduDetailStudentGroup,
      beforeEnter: [isAuthenticated, isDepOrAdministrator]
    },
    {
        path: '/centre/surveys',
        name: 'Surveys',
        component: Surveys,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/centre/reports',
        name: 'Reports',
        component: Reports,
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/centre/personal_schedule',
        name: 'PersonalSchedule',
        component: PersonalSchedule,
        beforeEnter: [isAuthenticated, isDepOrAdministrator]
    },
    {
        path: '/centre/journal',
        name: 'Journal',
        component: Journal,
        beforeEnter: [isAuthenticated, isAdministrator]
    }
]

export default centre_routes
