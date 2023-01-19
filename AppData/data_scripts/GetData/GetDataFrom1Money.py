# this function return data dictionary  like
# {'date': {'Type': 'Expenses', 'From': {'Name': 'Cash', 'Color':... and other}}
# with it I can get data from 1Money's .csv file, who have all transaction

def get_data_from_1money(money_file_path, categories_data_file_path, accounts_data_file_path):

    with open(categories_data_file_path, mode='r+', encoding="utf-8-sig") as categories_data_file:
        categories_data_dict = {}

        for line in categories_data_file:
            line = line.split('-')

            id_of_categories = line[0]
            name_of_categories = line[1]
            color_of_categories = tuple([float(i) for i in line[2].split(',')])

            categories_data_dict[name_of_categories] = {'id': id_of_categories, 'Color': color_of_categories}

        latest_id_of_categories = id_of_categories

    with open(accounts_data_file_path, mode='r+', encoding="utf-8-sig") as accounts_data_file:
        accounts_data_dict = {}

        for line in accounts_data_file:
            data_list = line.split('-')

            id_of_account = data_list[0]
            name_of_account = data_list[1]
            color_of_account = tuple([float(i) for i in data_list[2].split(',')])

            accounts_data_dict[name_of_account] = {'id': id_of_account, 'Color': color_of_account}

        latest_id_of_account = id_of_account

    # with open(savings_data_file_path, mode='r+', encoding="utf-8-sig") as savings_data_file:
    #     savings_data_dict = {}
    #
    #     for line in savings_data_file:
    #         line = line.split('-')
    #
    #         id_of_savings = line[0]
    #         name_of_savings = line[1]
    #         color_of_savings = tuple([float(i) for i in line[2].split(',')])
    #
    #         savings_data_dict[name_of_savings] = {'id': id_of_savings, 'Color': color_of_savings}
    #
    #     latest_id_of_savings = id_of_savings

    with open(money_file_path, encoding="utf-8-sig") as csvfile:
        import csv
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        transaction_dict = {}

        dict_for_translation = {'Доход': 'Income', 'Расход': 'Expenses', 'Перевод': 'Transfer', 'Наличные': 'Cash',
                                'Зарплата': 'Salary'}

        num_of_row = 0
        for row in reader:
            if "ДАТА" in row:
                continue

            elif row == ['', '']:  # After that in the file will be Accounts amounts
                break

            clean_row = []

            num_of_i = 0
            for i in row:
                if i != "":
                    if '(' in i:
                        i = i.split('(')[0][:-1]

                    if i in dict_for_translation:
                        i = dict_for_translation[i]

                    clean_row.append(i)
                    num_of_i += 1
            # in accounts dict
            if clean_row[2] in accounts_data_dict:
                name_of = clean_row[2]
                id_of = accounts_data_dict[name_of]['id']

                clean_row[2] = id_of

            elif not clean_row[2] in accounts_data_dict:
                latest_id_of_account = latest_id_of_account.split('_')
                name_id = latest_id_of_account[0]
                num_id = str(int(latest_id_of_account[1]) + 1)
                latest_id_of_account = f'{name_id}_{num_id}'

                accounts_data_dict[clean_row[2]] = {'id': latest_id_of_account}

                clean_row[2] = latest_id_of_account

            # in categories dict
            if clean_row[3] in categories_data_dict:
                name_of = clean_row[3]
                id_of = categories_data_dict[name_of]['id']

                clean_row[3] = id_of

            elif not clean_row[3] in categories_data_dict:
                latest_id_of_categories = latest_id_of_categories.split('_')
                name_id = latest_id_of_categories[0]
                num_id = str(int(latest_id_of_categories[1]) + 1)
                latest_id_of_categories = f'{name_id}_{num_id}'

                categories_data_dict[clean_row[3]] = {'id': latest_id_of_categories}

                clean_row[3] = latest_id_of_categories

            transaction_dict[num_of_row] = {}

            transaction_dict[num_of_row]['Date'] = clean_row[0]

            transaction_dict[num_of_row]['Type'] = clean_row[1]

            if transaction_dict[num_of_row]['Type'] == 'Income':
                transaction_dict[num_of_row]['From'] = clean_row[3]
                transaction_dict[num_of_row]['To'] = clean_row[2]

            else:
                transaction_dict[num_of_row]['From'] = clean_row[2]
                transaction_dict[num_of_row]['To'] = clean_row[3]

            transaction_dict[num_of_row]['FromSUM'] = clean_row[4]
            transaction_dict[num_of_row]['FromCurrency'] = clean_row[5]
            transaction_dict[num_of_row]['ToSUM'] = clean_row[6]
            transaction_dict[num_of_row]['ToCurrency'] = clean_row[7]

            if len(clean_row) >= 9:
                transaction_dict[num_of_row]['Сomment'] = clean_row[8]

            num_of_row += 1

        # changing transaction id
        # the newer transaction the bigger number of it
        changed_transaction_dict = {}
        latest_new_key = 0

        for old_key in range(num_of_row - 1, -1, -1):
            changed_transaction_dict[latest_new_key] = transaction_dict[old_key]
            del transaction_dict[old_key]
            latest_new_key += 1


        return changed_transaction_dict


if __name__ == '__main__':
    from datetime import datetime

    start_time = datetime.now()
    print(*get_data_from_1money(money_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/1Money_30_04_2022.csv',
                         categories_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_categories-data.txt',
                         accounts_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_accounts-data.txt',
                         # savings_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_savings-data.txt'
                                ).items(), sep='\n')
    print(f'This worked {datetime.now() - start_time}')
