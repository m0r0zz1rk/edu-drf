import {showAlert} from "../../../commons/alerts.js"
import {apiRequest} from "../../../commons/apiRequest.js";
import {getCookie} from "@/commons/cookie";

const isStudent = (to, from, next) => {
    // Проверка роли пользователя на обучающегося
  if (getCookie('cokoRole')) {
    if (getCookie('cokoRole') === 'student') {
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
      '/backend/api/v1/auth/get_user_role/',
      'GET',
      true,
      null,
      true
    )
      .then(resp => {
        if (resp.status === 200) {
          return resp.json()
        } else {
          switch (resp.status) {
            case '401':
            case '403':
              showAlert(
                'error',
                'Доступ к разделу',
                'Вы не авторизованы либо не имеете доступа к данному разделу'
              )
              next('/')
              break

            default:
              showAlert(
                'error',
                'Ошибка провери роли',
                'Произошла непредвиденная ошибка при проверке роли пользователя'
              )
              next('/')
          }
          return
        }
      })
      .then(data => {
        switch (data.role) {
          case 'dep':
          case 'centre':
            showAlert(
              'error',
              'Доступ к разделу',
              'У вас нет доступа к запрашиваемому разделу'
            )
            next('/')
            return;

          default:
            next()
        }
      })
  }
}

export default isStudent
