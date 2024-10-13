import daysOfWeek from "@/commons/consts/daysOfWeek";

//Преобразовантие даты из текстового формата ДД.ММ.ГГГГ в объект Date
export function convertBackendDate(backendDate) {
  try{
    let arr = backendDate.split('.')
    return new Date(arr[2], arr[1]-1, arr[0])
  } catch (e) {
    return backendDate
  }
}

//Преобразование объекта Date в текстовый формат даты: ДД.ММ.ГГГГ
export function convertDateToBackend(frontDate) {
  let day = frontDate.getDate()
  if (day < 10) {
    day = String('0'+day)
  }
  let month = Number(frontDate.getMonth()+1)
  if (month < 10) {
    month = String('0'+month)
  }
  return day + '.' + month + '.' + frontDate.getFullYear()
}

// Получение дня недели для полученной даты
export function getDayOfWeek(date) {
  let internal = date
  if (!(Object.prototype.toString.call(date) === '[object Date]')) {
    internal = convertBackendDate(date)
  }
  return daysOfWeek[internal.getDay()]
}