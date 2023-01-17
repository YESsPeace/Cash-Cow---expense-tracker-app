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

        file = open(path, 'w', encoding="utf-8-sig")

        writer = csv.writer(file, delimiter=',', quotechar='"')

        writer.writerow(
            ['id'] + ['Date'] + ['Type'] + ['From'] + ['To'] + ['FromSUM'] +
            ['FromCurrency'] + ['ToSUM'] + ['ToCurrency'] + ['Сomment'])

        print('# data_file: transaction-history.csv is open')

if __name__ == '__main__':
    create_transaction_history_file('C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/transaction-history.csv')
