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

    history_for_the_period_dict = get_sorted_history_dict_by_date(history_for_the_period_dict)

    return history_for_the_period_dict


def month_in_history(history_dict):
    if len(history_dict) != 0:

        import datetime
        from dateutil.relativedelta import relativedelta

        history_dict = get_sorted_history_dict_by_date(history_dict)

        first_trans_id = list(history_dict)[-1]
        first_date = history_dict[first_trans_id]['Date']

        last_trans_id = list(history_dict)[0]
        last_date = history_dict[last_trans_id]['Date']

        first_date = first_date.split('.')
        first_date = [int(i) for i in first_date]
        first_date = datetime.datetime(first_date[2], first_date[1], first_date[0])

        print('# first_date:', first_date)

        last_date = last_date.split('.')
        last_date = [int(i) for i in last_date]
        last_date = datetime.datetime(last_date[2], last_date[1], last_date[0])

        print('# last_date:', last_date)

        difference_in_months = relativedelta(last_date, first_date).months

        print('# difference_in_months:', difference_in_months)

        return difference_in_months

    else:
        return 0


def get_sorted_history_dict_by_date(history_dict):
    import datetime

    return dict(sorted(history_dict.items(),
                       # key for creating my own sort func
                       key=lambda item:
                       # datetime has a func for typing date, which you need
                       int(datetime.datetime([int(i) for i in item[1]['Date'].split('.')][2],
                                             [int(i) for i in item[1]['Date'].split('.')][1],
                                             [int(i) for i in item[1]['Date'].split('.')][0]
                                             ).strftime('%Y%m%d'))
                       # convert to string format (YYYYMMDD) and then to int
                       )[::-1])


def get_categories_month_data(month_history_dict):
    categories_month_data_dict = {}

    for transaction in month_history_dict.values():
        if transaction['Type'] == 'Expenses':
            if transaction['To'] in categories_month_data_dict:
                categories_month_data_dict[transaction['To']]['SUM'] += \
                    float(transaction['ToSUM'])

            else:
                categories_month_data_dict[transaction['To']] = {
                    'Currency': transaction['ToCurrency'],
                    'SUM': float(transaction['ToSUM'])
                }

    return categories_month_data_dict


def get_incomes_month_data(month_history_dict):
    incomes_month_data_dict = {}

    for transaction in month_history_dict.values():
        if transaction['Type'] == 'Income':
            if transaction['From'] in incomes_month_data_dict:
                incomes_month_data_dict[transaction['From']]['SUM'] += \
                    float(transaction['ToSUM'])

            else:
                incomes_month_data_dict[transaction['From']] = {
                    'Currency': transaction['FromCurrency'],
                    'SUM': float(transaction['FromSUM'])
                }
    return incomes_month_data_dict
