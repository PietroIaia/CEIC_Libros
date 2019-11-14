import csv
import sys

authorInfo = []
writtenBy = []

with open('AutoresIndexados.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in reader:
        if row[0] != "NA":
            authorInfo.append([row[0] + " " + row[1], row[2]])
        else:
            authorInfo.append([row[1], row[2]])
csvfile.closed

with open('Codes.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    reader.__next__()
    for row in reader:
        for i in range(len(authorInfo)):
            if authorInfo[i][0] in row[1]: 
                writtenBy.append([row[3], authorInfo[i][1]])
csvfile.closed

with open('writtenBy.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\"')
    for info in writtenBy:
        writer.writerow(info)
csvfile.closed
