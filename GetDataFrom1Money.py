def get_data_from_1money(money_file_path='data_files/Test_files/1Money_30_04_2022.csv',
                         categories_data_file_path='data_files/Test_files/test_categories-data.txt',
                         accounts_data_file_path='data_files/Test_files/test_accounts-data.txt'):
    import csv

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

    with open(money_file_path, encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        transaction_dict = {}

        for row in reader:
            if "ДАТА" in row:
                continue

            clean_row = []
            for i in row:
                if i != "":
                    if '(' in i:
                        i = i.split('(')[0][:-1]

                        clean_row.append(i)
                    else:
                        clean_row.append(i)

            if clean_row[3] in color_categories_data_dict:
                clean_row[3] = {'Name': clean_row[3], 'Color': color_categories_data_dict[row[3]]}

            if clean_row[2] in color_accounts_data_dict:
                clean_row[2] = {'Name': clean_row[2], 'Color': color_accounts_data_dict[row[2]]}

            transaction_dict[clean_row[0]] = clean_row[1:]

        return transaction_dict

if __name__ == '__main__':
    print(*get_data_from_1money(money_file_path='data_files/Test_files/transaction-history.csv').items(), sep='\n')