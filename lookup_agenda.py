from db_table import db_table
import sys
import sqlite3

# check if the user enters the correct number of parameter
if len(sys.argv) < 3:
    sys.exit("There should be exactly two parameter. i.e. $> python3 lookup_agenda.py location Room 201")

# Setup
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
column_name = [*schema]
column = sys.argv[1]
value = sys.argv[2:]
value = ' '.join(value)
db_name = "interview_test.db"
table_name = "agenda"
conn = sqlite3.connect(db_name)
c = conn.cursor()
query_cols = ["date","time_start","time_end","title","location","description","speaker"]
query_result = []

# Column can only be one of {date, time_start, time_end, title, location, description, speaker}
if not column in query_cols:
    sys.exit("Column can only be one of {date, time_start, time_end, title, location, description, speaker}")

# QUERY HELPER
#
# \parm type  string  check if the column is "speaker"
#
# \return  none  just output the query result
def query_helper(type):
    query_string = "SELECT * FROM %s " % (table_name)
    if type == "speaker":
        query_string += "WHERE" + " %s LIKE '%s'" % (column,value)
    else:
        query_string += "WHERE" + " %s = '%s'" % (column,value)

    # finding query result ids
    query_string_id = query_string.replace("*","id")
    ids_string = ""
    for ids in c.execute(query_string_id):
        ids_string += "," + "".join(ids)

    # subsessions need to be returned too
    query_string += " OR parentID IN (%s)" % (ids_string[1:])
    query_string += " ORDER BY id"

    for row in c.execute(query_string):
        result_row = {}
        for i in range(0, len(column_name)):
            result_row[column_name[i]] = row[i]
        print(result_row, end="\n\n")


if column == "speaker":
    query_helper("speaker")
else:
    query_helper("other")
        
    