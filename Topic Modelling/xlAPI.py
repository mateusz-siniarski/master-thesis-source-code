import xlrd
import xlwt

def getSpreadsheetFile(ss_path, sheet_id=0):
    workbook = xlrd.open_workbook(ss_path)
    sheet = workbook.sheet_by_index(sheet_id)
    return sheet

