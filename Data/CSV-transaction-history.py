import csv

print('# Csv-transaction-history.py is open')

transaction_history_file = open('Data\data_files\\transaction-history.csv', 'a')
transaction_history_file.close()

print('# transaction-history.csv is done')

file = open('Data\data_files\\transaction-history.csv', 'w', encoding="UTF8")

writer = csv.writer(file)

writer.writerow(
    ['ДАТА'] + ['ТИП'] + ['СО СЧЁТА'] + ['НА СЧЁТ / НА КАТЕГОРИЮ'] + ['СУММА'] + ['ВАЛЮТА'] + ['СУММА 2'] +
    ['ВАЛЮТА 2'] + ['МЕТКИ'] + ['ЗАМЕТКИ'])

print('# transaction-history.csv is written')
