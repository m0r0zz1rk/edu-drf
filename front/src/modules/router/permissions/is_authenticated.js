import {getCookie} from "../../../commons/cookie.js";
import {apiRequest} from "../../../commons/api_request.js";
import {showAlert} from "../../../commons/alerts.js";

const isAuthenticated = (to, from, next) => {
    if (!(getCookie('isAuthenticated'))) {
        showAlert(
            'error',
            'Проверка авторизации',
            'Пожалуйста, войдите в систему'
        )
        next('/?nextUrl='+to.path)
        return
    } else {
        apiRequest(
            '/api/v1/auth/check_auth/',
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
                    next('/?nextUrl='+to.path)
                    return
                } else if (resp.status === 500) {
                    showAlert(
                        'error',
                        'Проверка авторизации',
                        'Произошла внутренняя ошибка сервера, повторите попытку позже'
                    )
                    next('/?nextUrl='+to.path)
                    return
                } else {
                    next()
                    return
                }
            })
    }
}

export default isAuthenticated