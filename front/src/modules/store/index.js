import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import state from "@/modules/store/state";
import getters from "@/modules/store/getters";
import mutations from "@/modules/store/mutations";
import actions from "@/modules/store/actions";
import {delCookie, getCookie, setCookie} from "@/commons/cookie";

export default createStore({
  plugins: [createPersistedState({
    storage: {
      getItem: key => getCookie(key),
      setItem: (key, value) => setCookie(key, value),
      removeItem: key => delCookie(key)
    }
  })],
  state: state,
  getters: getters,
  mutations: mutations,
  actions: actions,
  modules: {}
})
