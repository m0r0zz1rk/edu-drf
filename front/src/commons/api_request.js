import {getCookie} from "./cookie.js";
import {showAlert} from "./alerts.js";

export function apiRequest (
    endpoint,
    method,
    tokenRequired,
    body,
    responseOnly = false,
    formData = false
) {
    // Функция для обращений к backend
    const backendUrl = import.meta.env.VITE_BACKEND_URL
    let csrfToken = getCookie('csrftoken')
    let headers = {
        'X-CSRFToken': csrfToken
    }
    if (!(formData)) {
        headers['Content-Type'] = 'application/json;charset=utf-8'
    }
    if (tokenRequired) {
        headers['Authorization'] = 'Token '+getCookie('cokoToken')
    }
    let request_parameters = {
        'method': method,
        'headers': headers
    }
    if (body) {
        if (formData) {
            request_parameters['body'] = body
        } else {
            request_parameters['body'] = JSON.stringify(body)
        }
    }
    if (responseOnly) {
        return fetch(backendUrl+endpoint, request_parameters)
            .catch(e => {return null})
            .then(resp => (resp))
    } else {
        return fetch(backendUrl+endpoint, request_parameters)
            .catch(e => {return null})
            .then(resp => {
                if(!([200, 201, 202, 204, 401, 403, 404, 409, 500].includes(resp.status))) {
                    showAlert(
                        'error',
                        'Ошибка запроса',
                        'Произошла непредвиденная ошибка, повторите попытку позже'
                    )
                    return false
                } else {
                    return resp.json()
                }
            })
            .then(data => (data))
    }
}
