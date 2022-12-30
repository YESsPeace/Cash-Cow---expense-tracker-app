def get_transaction_history(history_file_path, categories_data_file_path,
                            accounts_data_file_path):
    with open(categories_data_file_path, mode='r+', encoding="utf-8-sig") as categories_data_file:
        color_categories_data_dict = {}

        for line in categories_data_file:
            name_of_categories = line.split('-')[1]
            color_of_categories = tuple([float(i) for i in line.split('-')[2][:-1].split(',')])

            color_categories_data_dict[name_of_categories] = color_of_categories

    with open(accounts_data_file_path, mode='r+', encoding="utf-8-sig") as accounts_and_savings_data_file:
        color_accounts_data_dict = {}

        for line in accounts_and_savings_data_file:
            data_list = line.split('-')

            try:
                name_of_account = data_list[1]
                color_of_account = tuple([float(i) for i in data_list[2][:-1].split(',')])

                color_accounts_data_dict[name_of_account] = color_of_account

            except IndexError:
                continue

            except ValueError:
                continue

    with open(history_file_path, encoding='utf-8') as history_file:
        import csv

        reader = csv.reader(history_file, delimiter=',', quotechar='"')

        transaction_dict = {}

        next(history_file)

        num_of_row = 0

        for row in reader:
            try:

                if row[2] in color_accounts_data_dict:
                    row[2] = {'Name': row[2], 'Color': color_accounts_data_dict[row[2]]}

                elif not row[2] in color_accounts_data_dict:
                    row[2] = {'Name': row[2], 'Color': (0, 0.41, 0.24, 1)}

                if row[3] in color_categories_data_dict:
                    row[3] = {'Name': row[3], 'Color': color_categories_data_dict[row[3]]}

                elif not row[3] in color_categories_data_dict:
                    row[3] = {'Name': row[3], 'Color': (0.38, 0.39, 0.61, 1)}

                transaction_dict[num_of_row] = {}

                transaction_dict[num_of_row]['Date'] = row[0]

                transaction_dict[num_of_row]['Type'] = row[1]

                if transaction_dict[num_of_row]['Type'] == 'Income':
                    transaction_dict[num_of_row]['From'] = row[3]
                    transaction_dict[num_of_row]['To'] = row[2]

                else:
                    transaction_dict[num_of_row]['From'] = row[2]
                    transaction_dict[num_of_row]['To'] = row[3]

                transaction_dict[num_of_row]['FromSUM'] = row[4]
                transaction_dict[num_of_row]['FromCurrency'] = row[5]
                transaction_dict[num_of_row]['ToSUM'] = row[6]
                transaction_dict[num_of_row]['ToCurrency'] = row[7]

                if len(row) == 9:
                    transaction_dict[num_of_row]['Сomment'] = row[8]

                num_of_row += 1

            except IndexError:
                num_of_row += 1

        return transaction_dict


def get_transaction_for_the_period(from_date, to_date, history_dict):
    import datetime

    from_date = from_date.replace('-', '.')
    to_date = to_date.replace('-', '.')

    from_date = from_date.split('.')
    from_date = [int(i) for i in from_date]
    from_date = datetime.datetime(from_date[0], from_date[1], from_date[2])

    to_date = to_date.split('.')
    to_date = [int(i) for i in to_date]
    to_date = datetime.datetime(to_date[0], to_date[1], to_date[2])

    history_for_the_period_dict = {}

    num_of_transaction = 0
    for item in history_dict.items():
        item_date = item[1]['Date'].split('.')[::-1]
        item_date = [int(i) for i in item_date]
        item_date = datetime.datetime(item_date[0], item_date[1], item_date[2])

        if (item_date >= from_date) and (item_date <= to_date):
            history_for_the_period_dict[num_of_transaction] = item[1]
            num_of_transaction += 1

    return history_for_the_period_dict


if __name__ == '__main__':
    # date_today = datetime.date.today()
    # first_day = str(date_today.replace(day=1)).replace('-', '.')
    # date_today = str(date_today).replace('-', '.')

    print('Что чекнуть?')
    print('1. get_transaction_history')
    print('2. get_transaction_for_the_period')
    n = int(input())

    if n == 1:
        import datetime

        start_time = datetime.datetime.now()

        print(*get_transaction_history(
            history_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/transaction-history.csv',
            categories_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_categories-data.txt',
            accounts_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_accounts-data.txt'
        ).items(), sep='\n')
        print(f'This worked {datetime.datetime.now() - start_time}')
    if n == 2:
        import datetime

        start_time = datetime.datetime.now()

        print(*get_transaction_for_the_period(
            from_date='2022-12-28',
            to_date='2022-12-28',
            history_dict=get_transaction_history(
                history_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/transaction-history.csv',
                categories_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_categories-data.txt',
                accounts_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_accounts-data.txt'
            )
        ).items(), sep='\n')
        print(f'This worked {datetime.datetime.now() - start_time}')
