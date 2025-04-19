// Получение описаний столбцов для таблицы ОО
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";

export const getOoFieldsArray = async () => {
  const moListRequest = await apiRequest(
    '/backend/api/v1/guides/mo/',
    'GET',
    true,
    null
  )
  if (moListRequest.error) {
    showAlert(
      'error',
      'Получение списка МО',
      moListRequest.error
    )
    return false
  }
  const ooTypeListRequest = await apiRequest(
    '/backend/api/v1/guides/oo_type/',
    'GET',
    true,
    null
  )
  if (ooTypeListRequest.error) {
    showAlert(
      'error',
      'Получение списка типов ОО',
      ooTypeListRequest.error
    )
    return false
  }
  return [
    {
      ui: 'input',
      type: 'text',
      key: 'short_name',
      addRequired: true,
    },
    {
      ui: 'input',
      type: 'text',
      key: 'full_name',
      addRequired: true,
    },
    {
      ui: 'select',
      items: [...moListRequest.map((mo) => mo.name)],
      key: 'mo',
      addRequired: true
    },
    {
      ui: 'select',
      items: [...ooTypeListRequest.map((ooType) => ooType.name)],
      key: 'oo_type',
      addRequired: true
    },
    {
      ui: 'input',
      type: 'text',
      key: 'form',
      addRequired: true,
    },
    {
      ui: 'actions',
      key: 'actions'
    }
  ]
}
