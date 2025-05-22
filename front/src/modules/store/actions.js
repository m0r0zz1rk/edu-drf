import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {delCookie, setCookie} from "@/commons/cookie";

const actions = {
  AUTH_REQUEST ({commit, dispatch}, user ) {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST');
      apiRequest(
        '/backend/api/v1/auth/login/',
        'POST',
        false,
        {
          'login': user.username,
          'password': user.password,
          'centre_auth': user.cokoLogin
        },
        false,
        false
      )
        .then(data => {
          if (!('coko_token' in data)){
            commit('AUTH_ERROR')
            showAlert(
              'error',
              'Вход в систему',
              data.error
            )
            reject(data.error)
          } else {
            const token = data.coko_token
            const role = data.coko_role
            const dep = data.coko_dep
            const depDisplay = data.coko_dep_display
            commit('AUTH_SUCCESS', token, role)
            setCookie('cokoToken', token)
            setCookie('cokoRole', role)
            setCookie('cokoDep', dep)
            setCookie('cokoDepDisplay', depDisplay)
            showAlert(
              'success',
              'Вход в систему',
              'Вход выполнен успешно'
            )
            resolve();
          }
        })
        .catch(err => {
          commit('AUTH_ERROR')
          delCookie('cokoToken') // if the request fails, remove any possible user token if possible
          delCookie('cokoRole') // if the request fails, remove any possible user token if possible
          reject(err)
          showAlert(
            'error',
            'Вход в систему',
            'Произошла неизвестная ошибка, пожалуйста, повторите попытку'
          )
        })
    })
  },
  AUTH_LOGOUT ({commit, dispatch}) {
    return new Promise((resolve, reject) => {
      delCookie('cokoToken') // clear your user's token from localstorage
      delCookie('cokoRole') // clear your user's token from localstorage
      commit('AUTH_LOGOUT')
      resolve()
    })
  }
}

export default actions
