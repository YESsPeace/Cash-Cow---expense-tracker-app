import csv

with open('data_files/Test_files/1Money_30_04_2022.csv', encoding="utf-8-sig") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    numOline = 0
    for row in reader:
        if numOline > 5:
            break
        else:
            print(row)

        numOline += 1