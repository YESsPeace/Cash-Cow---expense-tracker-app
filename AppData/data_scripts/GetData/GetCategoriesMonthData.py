def get_categories_month_data(month_history_dict):
    categories_month_data_dict = {}

    for transaction in month_history_dict.values():
        if transaction['Type'] == 'Expenses':
            if transaction['To'] in categories_month_data_dict:
                categories_month_data_dict[transaction['To']]['SUM'] += \
                    int(transaction['ToSUM'])

            else:
                categories_month_data_dict[transaction['To']] = {
                    'Currency': transaction['ToCurrency'],
                    'SUM': int(transaction['ToSUM'])
                }

    return categories_month_data_dict
