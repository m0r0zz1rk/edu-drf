import * as XLSX from 'xlsx/xlsx.js'

export function xlsxDownloadFunction(wb_name, headers, info) {
  const worksheet = XLSX.utils.json_to_sheet()
  const workbook = XLSX.utils.book_new()

  XLSX.utils.book_append_sheet(workbook, worksheet, wb_name)
  XLSX.utils.sheet_add_aoa(worksheet, [headers], {origin: 'A1'})

  const filename = wb_name+'.xlsx'
  XLSX.writeFileSync(workbook, filename, {compression: true})
}
