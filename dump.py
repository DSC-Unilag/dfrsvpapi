import csv
import pprint as pp


res = []

# with open('data.csv', 'r', encoding='utf-8') as file:
#     mfile = csv.DictReader(file)
    
#     for obj in mfile:
#         temp = {
#             'ticket_id': obj['Ticket number'],
#             'first_name': obj['First Name'],
#             'last_name': obj['Last Name']
#         }
#         res.append(temp)
    
   
def parseCsv(filename):
    res = []
    with open(filename, 'r', encoding='utf-8') as file:
        mfile = csv.DictReader(file)
        
        for obj in mfile:
            temp = {
                'ticket_id': obj['Ticket number'],
                'first_name': obj['First Name'],
                'last_name': obj['Last Name']
            }
            res.append(temp)
    with open('result.csv', 'w', encoding='utf-8') as file:
        fieldnames = ['ticket_id', 'first_name', 'last_name']
        wfile = csv.DictWriter(file, fieldnames=fieldnames, dialect='unix')

        wfile.writeheader()
        for row in res:
            wfile.writerow(row)
    return res

def readCsv(filename):
    res = []
    with open(filename, 'r', encoding='utf-8') as file:
        mfile = csv.DictReader(file)
        
        for obj in mfile:
            res.append(obj)
    return res

# pp.pprint(parseCsv('data.csv'))
# print(r)