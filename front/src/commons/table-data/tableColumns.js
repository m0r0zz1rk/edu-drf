// Столбцы таблиц
import {getOoFieldsArray} from "@/commons/table-data/get-data-for-fields-array/getOoFieldsArray";

export const tableColumns = {
  oo: {
    tableHeaders: [
      {
        'title': 'Краткое наименование',
        'key': 'short_name'
      },
      {
        'title': 'Полное наименование',
        'key': 'full_name'
      },
      {
        'title': 'МО',
        'key': 'mo'
      },
      {
        'title': 'Тип ОО',
        'key': 'oo_type'
      },
      {
        'title': 'Форма',
        'key': 'form'
      },
      {
        'title': 'Управление',
        'key': 'actions'
      }
    ],
    fieldsArray: null
  }
}
