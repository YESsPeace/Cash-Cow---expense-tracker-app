def get_transaction_history(history_file_path):
    with open(history_file_path, encoding='utf-8') as history_file:
        import csv

        reader = csv.reader(history_file, delimiter=',', quotechar='"')

        transaction_dict = {}

        next(history_file)

        for row in reader:
            transaction_dict[row[0]] = {}

            transaction_dict[row[0]]['Date'] = row[1]

            transaction_dict[row[0]]['Type'] = row[2]

            if transaction_dict[row[0]]['Type'] == 'Income':
                transaction_dict[row[0]]['From'] = row[4]
                transaction_dict[row[0]]['To'] = row[3]

            else:
                transaction_dict[row[0]]['From'] = row[3]
                transaction_dict[row[0]]['To'] = row[4]

            transaction_dict[row[0]]['FromSUM'] = row[5]
            transaction_dict[row[0]]['FromCurrency'] = row[6]
            transaction_dict[row[0]]['ToSUM'] = row[7]
            transaction_dict[row[0]]['ToCurrency'] = row[8]

            if len(row) == 10:
                transaction_dict[row[0]]['Сomment'] = row[9]

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

    for trans_id in history_dict:
        item_date = history_dict[trans_id]['Date'].split('.')[::-1]
        item_date = [int(i) for i in item_date]
        item_date = datetime.datetime(item_date[0], item_date[1], item_date[2])

        if (item_date >= from_date) and (item_date <= to_date):
            history_for_the_period_dict[trans_id] = history_dict[trans_id]

    history_for_the_period_dict = dict(sorted(history_for_the_period_dict.items(),
                                              # key for creating my own sort func
                                              key=lambda item:
                                              # datetime has a func for typing date, which you need
                                              int(datetime.datetime([int(i) for i in item[1]['Date'].split('.')][2],
                                                                    [int(i) for i in item[1]['Date'].split('.')][1],
                                                                    [int(i) for i in item[1]['Date'].split('.')][0]
                                                                    ).strftime('%Y%m%d'))
                                              # convert to string format (YYYYMMDD) and then to int
                                              )[::-1])




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
        ).items(), sep='\n')
        print(f'This worked {datetime.datetime.now() - start_time}')
    if n == 2:
        import datetime

        start_time = datetime.datetime.now()

        history_period_dict = get_transaction_for_the_period(
            from_date='2023-01-01',
            to_date='2023-01-30',
            history_dict=get_transaction_history(
                history_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/transaction-history.csv',
            )
        )

        print(*history_period_dict.items(), sep='\n')

        print(f'This worked {datetime.datetime.now() - start_time}')
