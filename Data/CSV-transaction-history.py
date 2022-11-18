import csv

print('# Csv-transaction-history.py is open')

try:
    file = open('Data\data_files\\transaction-history.csv', 'r', encoding="utf-8-sig")

    print('# data_file: transaction-history.csv is open')

except FileNotFoundError:
    transaction_history_file = open('Data\data_files\\transaction-history.csv', 'a')
    transaction_history_file.close()

    print('# transaction-history.csv is done')

    file = open('Data\data_files\\transaction-history.csv', 'w', encoding="UTF8")

    writer = csv.writer(file, delimiter=',', quotechar='"')

    writer.writerow(
        ['ДАТА'] + ['ТИП'] + ['СО СЧЁТА'] + ['НА СЧЁТ / НА КАТЕГОРИЮ'] + ['СУММА'] + ['ВАЛЮТА'] + ['СУММА 2'] +
        ['ВАЛЮТА 2'] + ['МЕТКИ'] + ['ЗАМЕТКИ'])

    print('# data_file: transaction-history.csv is open')
