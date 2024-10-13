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
    {
      path: '/centre/edu/student_group/:groupId',
      name: 'EduDetailStudentGroup',
      component: EduDetailStudentGroup,
      beforeEnter: [isAuthenticated, isAdministrator]
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
        beforeEnter: [isAuthenticated, isAdministrator]
    },
    {
        path: '/centre/journal',
        name: 'Journal',
        component: Journal,
        beforeEnter: [isAuthenticated, isAdministrator]
    }
]

export default centre_routes
