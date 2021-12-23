import sys
import csv
from dbfread import DBF

# run as: python3 dbf_to_csv.py > outputfile

table = DBF('SBE_PRECINCTS_CENSUSBLOCKS_20210923.dbf')
writer = csv.writer(sys.stdout)

writer.writerow(table.field_names)
for record in table:
    writer.writerow(list(record.values()))