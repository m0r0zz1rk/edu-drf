export function getCookie(cName) {
    // Получение параметра cookie
    let cStart = 0;
    let cEnd = 0;
    if (document.cookie.length > 0) {
        cStart = document.cookie.indexOf(cName+'=');
        if (cStart !== -1) {
            cStart = cStart + cName.length + 1;
            cEnd = document.cookie.indexOf(';', cStart);
            if (cEnd === -1) {
                cEnd = document.cookie.length;
            }
            return unescape(document.cookie.substring(cStart, cEnd));
        }
    }
}

export function setCookie(cName, cValue) {
    // Установка параметра cookie
    if (document.cookie.length > 0) {
        if (document.cookie.indexOf(cName + '=') !== -1) {
            delCookie(cName)
        }
    }
    document.cookie = cName + '=' + cValue + ';httpOnly';
}

export function delCookie(cName) {
    // Удаление параметра cookie
    document.cookie = cName+'='+new Date(0);
}