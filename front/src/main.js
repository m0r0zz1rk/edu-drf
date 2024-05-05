import { createApp } from 'vue'
import App from './App.vue'
import router from './modules/router'
import {vuetify} from "./plugins/vuetify.js";
import VMask from "@ssibrahimbas/v-mask";
import store from "@/modules/store";

createApp(App)
    .use(store)
    .use(router)
    .use(vuetify)
    .use(VMask)
    .mount('#app')
