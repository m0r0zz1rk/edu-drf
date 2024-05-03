import { createApp } from 'vue'
import App from './App.vue'
import router from './modules/router'
import {vuetify} from "./plugins/vuetify.js";
import VMask from "@ssibrahimbas/v-mask";

createApp(App)
    .use(router)
    .use(vuetify)
    .use(VMask)
    .mount('#app')
