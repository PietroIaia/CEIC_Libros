import csv

def createFirstName(info, end):
    name = ""
    for i in range(end - 1):
        name += info[i]
        name += " "

    name += info[end - 1]

    return name

newCSV = []
key = 0

with open('ListaFinal.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in reader:
        info = row[0].split(" ")
        if len(info) == 1:
            newCSV.append(["NA", info[0], key])
            key += 1
        else:
            fname = createFirstName(info, len(info) - 1)
            newCSV.append([fname, info[len(info) - 1], key])
            key += 1
csvfile.closed

with open('AutoresIndexados.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\"')
    for author in newCSV:
        writer.writerow(author)
csvfile.closed