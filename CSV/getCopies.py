import csv

ejemplares = []

with open('Codes.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    reader.__next__()
    for row in reader:
        for i in range(int(row[2])):
            ejemplares.append([i, row[3]])
csvfile.closed

with open('CopyCodes.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\"')
    for copy in ejemplares:
        writer.writerow(copy)
csvfile.closed