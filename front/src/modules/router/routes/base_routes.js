import Login from "@/views/Login.vue";
import Main from "@/views/Main.vue";
import isAuthenticated from "@/modules/router/permissions/is_authenticated";
import Profile from "@/views/Profile.vue";
import isStudent from "@/modules/router/permissions/is_student";
import PasswordReset from "@/views/PasswordReset.vue";

const base_routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
      path: '/',
      name: 'Main',
      component: Main,
      beforeEnter: isAuthenticated
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      beforeEnter: [isAuthenticated, isStudent]
    },
    {
        path: '/password_reset',
        name: 'PasswordReset',
        component: PasswordReset,
    }
]

export default base_routes
