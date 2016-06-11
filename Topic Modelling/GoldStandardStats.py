import re
import xlrd
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def get_pre_sheets(workbooks_paths):
    pre_sheets = []
    for path in workbooks_paths:
        pre_workbook = xlrd.open_workbook(path)
        pre_sheet = pre_workbook.sheet_by_index(0)
        pre_sheets.append(pre_sheet)
    return pre_sheets

def groupArticlesFromSpreadsheets(spreadsheets):
    stats = [0, 0, 0]


    for sheet in spreadsheets:
        start_col = 0
        title = sheet.cell(0,start_col).value
        while re.match("(.*(Timestamp|Name|Age|Degree|Profession).*)",title):
            start_col += 1
            title = sheet.cell(0, start_col).value
        for i in range(start_col,sheet.ncols):
            title = sheet.cell(0, i).value
            if re.match("^(.*)\s-\shttps://",title):
                title = re.match("^(.*)\s-\shttps://",title).group(1)

                scores = [['Yes', 0], ['Maybe', 0], ['No', 0]]
                for j in range(1, sheet.nrows):
                    for s in scores:
                        if sheet.cell(j, i).value == s[0]:
                            s[1] += 1
                relevance = int(round(float(3 * scores[0][1] + 2 * scores[1][1] + scores[2][1]) / (
                            scores[0][1] + scores[1][1] + scores[2][1]) - 1))
                if relevance == 2:
                    stats[0] += 1
                elif relevance == 1:
                    stats[1] += 1
                elif relevance == 0:
                    stats[2] += 1

    return stats


if sys.argv.__len__() == 2:
    pathFolder = sys.argv[1]
    pathDictionary = sys.argv[1] + "/dictionary.dict"
    pathCorpus = sys.argv[1] + "/corpus.mm"
    pathModel = sys.argv[1] + "/models"
    pathIndex = sys.argv[1] + "/index"
    pathTFIDF = sys.argv[1] + "/models/model.tfidf"
    pathBinding = sys.argv[1] + "/corpus-docs.binding"
else:
    print "pathFolder"
    quit()

responses_location = pathFolder + "/relevant-docs/responses/relevant-docs-normalized (Responses).xlsx"
spreadsheets_paths = [responses_location]

print groupArticlesFromSpreadsheets(get_pre_sheets(spreadsheets_paths))