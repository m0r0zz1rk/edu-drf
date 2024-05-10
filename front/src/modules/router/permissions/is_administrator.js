import {showAlert} from "../../../commons/alerts.js"
import {apiRequest} from "../../../commons/api_request.js";
import {getCookie} from "@/commons/cookie";

const isAdministrator = (to, from, next) => {
    // Проверка роли пользователя на администратора системы
  if (getCookie('cokoRole')) {
    if (getCookie('cokoRole') === 'centre') {
      next()
      return
    } else {
      showAlert(
        'error',
        'Доступ к разделу',
        'У вас нет доступа к запрашиваемому разделу'
      )
      next('/')
      return;
    }
  } else {
    apiRequest(
      'backend/api/v1/auth/get_user_role/',
      true,
      'GET',
      null,
      true
    )
      .then(resp => {
        switch (resp.status) {
          case '401':
          case '403':
            showAlert(
              'error',
              'Доступ к разделу',
              'Вы не авторизованы либо не имеете доступа к данному разделу'
            )
            next('/main')
            return;

          case '200':
            return resp.json()

          default:
            showAlert(
              'error',
              'Ошибка провери роли',
              'Произошла непредвиденная ошибка при проверке роли пользователя'
            )
            next('/main')
            return;
        }
      })
      .then(data => {
        switch (data.role) {
          case 'student':
          case 'dep':
            showAlert(
              'error',
              'Доступ к разделу',
              'У вас нет доступа к запрашиваемому разделу'
            )
            next('/main')
            return;

          default:
            next()
        }
      })
  }
}

export default isAdministrator
