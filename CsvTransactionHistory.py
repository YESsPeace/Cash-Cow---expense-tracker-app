def create_transaction_history_file(path):
    import csv

    print('# Csv-transaction-history.py is open')

    try:
        file = open(path, 'r', encoding="utf-8-sig")

        print('# data_file: transaction-history.csv is open')

    except FileNotFoundError:
        transaction_history_file = open(path, 'a')
        transaction_history_file.close()

        print('# transaction-history.csv is done')

        file = open(path, 'w', encoding="UTF8")

        writer = csv.writer(file, delimiter=',', quotechar='"')

        writer.writerow(
            ['ДАТА'] + ['ТИП'] + ['СО СЧЁТА'] + ['НА СЧЁТ / НА КАТЕГОРИЮ'] + ['СУММА'] + ['ВАЛЮТА'] + ['СУММА 2'] +
            ['ВАЛЮТА 2'] + ['МЕТКИ'] + ['ЗАМЕТКИ'])

        print('# data_file: transaction-history.csv is open')
