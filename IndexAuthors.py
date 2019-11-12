import csv

################ MAIN ##############################

authors = set()

with open('ListaAutores.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in reader:
        rowNames = row[0].split(", ")
        for i in range(len(rowNames)):
            if rowNames[i] not in authors:
                authors.add(rowNames[i])
csvfile.closed

with open('ListaFinal.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\"')
    for name in authors:
        writer.writerow([name])
csvfile.closed
