// Конвертация строкого формата времени (ЧЧ:ММ) в количество секунд
export function convertTimeStrToSeconds(time_str) {
    let re_time_str = new RegExp("[0-9]{2}:[0-9]{2}")
    let seconds = 0
    if (re_time_str.test(time_str)) {
        let split = time_str.split(':')
        seconds = (Number(split[0]) * 60 * 60) + (Number(split[1] * 60))
    }
    return seconds
}

// Конвертация количества секунд в формате времени (ЧЧ:ММ)
export function convertSecondsToTimeStr(seconds) {
    if (seconds < 0) {
        return '00:00'
    }
    let hours = Math.floor(seconds / 3600)
    let minutes = Math.floor((seconds % 3600) / 60)
    if (hours < 10) {
        hours = '0' + hours
    }
    if (minutes < 10) {
        minutes = '0' + minutes
    }
    return hours+':'+minutes
}
