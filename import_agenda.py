from db_table import db_table
import xlrd
import sys
import re

# CLEANHTML
# remove HTML tags from a string
#
# \parm raw_html  string  string that need to be cleaned
#
# \return cleantext  string  string that without HTML tags
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


# check if the user enters the correct number of parameter
if len(sys.argv) != 2:
    sys.exit("There should be only one parameter.")

# initial setup
filename = sys.argv[-1]
book = xlrd.open_workbook(filename)
sheet = book.sheet_by_index(0)
total_row = sheet.nrows
total_col = sheet.ncols
start_index = 15
table_name = "agenda"
schema = {
    "date": "text NOT NULL",
    "time_start": "text NOT NULL",
    "time_end": "text NOT NULL",
    "session": "text NOT NULL",
    "title": "text NOT NULL",
    "location": "text",
    "description": "text",
    "speaker": "text",
    "id": "text",
    "parentID": "text"
}
cols_name = [*schema]

# INSERT HELPER 
# get the specified row data from the sheet object and prepare item to be insert
# in DB, mapping column to value
#
# \parm row  int  row number in the sheet object (excel)
#
# \return item  dict<string, string> item to be insert in DB, mapping column to value
def insert_helper(row):
    row_list = sheet.row_values(row)
    # remove "'" single quote in string
    row_list = [s.replace("'", "") for s in row_list]
    # remove HTML tags
    row_list[6] = cleanhtml(row_list[6])
    item = dict(zip(schema, row_list))
    item["id"] = str(row+1)

    # check if the current session is a parent session
    if row_list[3] == "Session":
        item["parentID"] = str(-1)
    elif row_list[3] == "Sub":
        # go to the previous row to find its parent session
        lookup_index = row - 1
        pre_row_list = sheet.row_values(lookup_index)
        while(pre_row_list[3]!= "Session" and lookup_index >= start_index):
            lookup_index = lookup_index -1
            pre_row_list = sheet.row_values(lookup_index)
        item["parentID"] = str(lookup_index+1)

    return item

# initialize the database and create the table
db_table = db_table(table_name,schema)

# parse the content of the excel file and store the content in the table
for i in range(start_index,total_row):
    item = insert_helper(i)
    db_table.insert(item)

