# this function return data dictionary  like
# {'date': {'Type': 'Expenses', 'From': {'Name': 'Cash', 'Color':... and other}}
# with it I can get data from 1Money's .csv file, who have all transaction

def get_data_from_1money(money_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/1Money_30_04_2022.csv',
                         categories_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_categories-data.txt',
                         accounts_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_accounts-data.txt'):

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

            if clean_row[2] in color_accounts_data_dict:
                clean_row[2] = {'Name': clean_row[2], 'Color': color_accounts_data_dict[clean_row[2]]}

            elif not clean_row[2] in color_accounts_data_dict:
                clean_row[2] = {'Name': clean_row[2], 'Color': (0, 0.41, 0.24, 1)}

            if clean_row[3] in color_categories_data_dict:
                clean_row[3] = {'Name': clean_row[3], 'Color': color_categories_data_dict[clean_row[3]]}

            elif not clean_row[3] in color_categories_data_dict:
                clean_row[3] = {'Name': clean_row[3], 'Color': (0.38, 0.39, 0.61, 1)}

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

        return transaction_dict


if __name__ == '__main__':
    from datetime import datetime

    start_time = datetime.now()
    print(*get_data_from_1money().items(), sep='\n')
    print(f'This worked {datetime.now() - start_time}')
