//Преобразовантие даты из текстового формата ДД.ММ.ГГГГ в объект Date
export function convertBackendDate(backendDate) {
  let arr = backendDate.split('.')
  return new Date(arr[2], arr[1]-1, arr[0])
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
