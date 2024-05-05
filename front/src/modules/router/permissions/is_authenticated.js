import {getCookie} from "@/commons/cookie";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

const isAuthenticated = (to, from, next) => {
    if (!(getCookie('cokoToken'))) {
      showAlert(
        'error',
        'Проверка авторизации',
        'Пожалуйста, войдите в систему'
      )
      next('/login?nextUrl='+to.path)
      return
    } else {
      apiRequest(
        '/backend/api/v1/auth/check_auth/',
        'GET',
        true,
        null,
        true
      )
        .then(resp => {
          if (resp.status === 401 || resp.status === 403) {
            showAlert(
              'error',
              'Проверка авторизации',
              'Пожалуйста, войдите в систему',
              false)
            next('/login?nextUrl='+to.path)
            return
          } else if (resp.status === 500) {
            showAlert(
              'error',
              'Проверка авторизации',
              'Произошла внутренняя ошибка сервера, повторите попытку позже'
            )
            next('/login?nextUrl='+to.path)
            return
          } else {
            next()
            return
          }
        })
    }
}

export default isAuthenticated
