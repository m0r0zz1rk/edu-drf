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
