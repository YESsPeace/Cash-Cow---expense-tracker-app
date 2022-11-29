def get_accounts_and_savings_names(data_from_1money_dict):
    # data dict with all transactions
    money_dict = data_from_1money_dict

    # empty lists for return
    accounts_name_type_income_or_expenses = []
    accounts_name_type_transfer = []

    # cycle which get names from dict with all transaction data
    for transaction in money_dict.values():  # just addition into list, names' distribution will be soon
        if transaction['Type'] == 'Income':
            flag = True
            accounts_already_in = None

            for i in range(len(accounts_name_type_income_or_expenses)):
                try:
                    if accounts_name_type_income_or_expenses[i]['Name'] == transaction['To']['Name']:
                        accounts_already_in = accounts_name_type_income_or_expenses[i]
                        accounts_name_type_income_or_expenses[i] = None
                        flag = False
                        break

                except (KeyError, TypeError):
                    continue

            if flag == True:  # if it's a new account
                name = transaction['To']['Name']
                balance = round(float(transaction['ToSUM']), 2)
                currency = transaction['ToCurrency']

                new_account_1 = {'Name': name, 'Balance': balance, 'Currency': currency}

            else:  # if it's an old account
                name = accounts_already_in['Name']
                balance = round(float(accounts_already_in['Balance']) + float(transaction['ToSUM']), 2)  # old balance + new transaction Sum
                currency = accounts_already_in['Currency']

                new_account_1 = {'Name': name, 'Balance': balance, 'Currency': currency}


            accounts_name_type_income_or_expenses.append(new_account_1)

        elif transaction['Type'] == 'Expenses':
            flag = True
            accounts_already_in = None

            for i in range(len(accounts_name_type_income_or_expenses)):
                try:
                    if accounts_name_type_income_or_expenses[i]['Name'] == transaction['From']['Name']:
                        accounts_already_in = accounts_name_type_income_or_expenses[i]
                        accounts_name_type_income_or_expenses[i] = None
                        flag = False
                        break

                except (KeyError, TypeError):
                    continue

            if flag == True:  # if it's a new account
                name = transaction['From']['Name']
                balance = round(float(transaction['FromSUM']), 2)
                currency = transaction['FromCurrency']

                new_account_1 = {'Name': name, 'Balance': balance, 'Currency': currency}

            else:  # if it's an old account
                name = accounts_already_in['Name']
                balance = round(float(accounts_already_in['Balance']) - float(transaction['FromSUM']), 2)  # old balance + new transaction Sum
                currency = accounts_already_in['Currency']

                new_account_1 = {'Name': name, 'Balance': balance, 'Currency': currency}

            accounts_name_type_income_or_expenses.append(new_account_1)

        elif transaction['Type'] == 'Transfer':
            new_account_1 = None
            new_account_2 = None

            flag_1, flag_2 = True, True

            account_already_in_1 = None
            account_already_in_2 = None

            for i in range(len(accounts_name_type_transfer)):
                try:
                    if accounts_name_type_transfer[i]['Name'] == transaction['From']['Name']:
                        account_already_in_1 = accounts_name_type_transfer[i]
                        accounts_name_type_transfer[i] = None
                        flag_1 = False
                        break

                except (KeyError, TypeError):
                    continue


            for k in range(len(accounts_name_type_transfer)):
                try:
                    if accounts_name_type_transfer[k]['Name'] == transaction['To']['Name']:
                        account_already_in_2 = accounts_name_type_transfer[k]
                        accounts_name_type_transfer[k] = None
                        flag_2 = False
                        break

                except (KeyError, TypeError):
                    continue

            if flag_1 == True:  # if it's a new account
                name = transaction['From']['Name']
                balance = round(-float(transaction['FromSUM']), 2)
                currency = transaction['FromCurrency']

                new_account_1 = {'Name': name, 'Balance': balance, 'Currency': currency}

            else:  # if it's an old account
                name = account_already_in_1['Name']
                balance = round(float(account_already_in_1['Balance']) - float(transaction['FromSUM']), 2)
                currency = account_already_in_1['Currency']

                new_account_1 = {'Name': name, 'Balance': balance, 'Currency': currency}

            if flag_2 == True:
                name = transaction['To']['Name']
                balance = round(float(transaction['ToSUM']), 2)
                currency = transaction['ToCurrency']

                new_account_2 = {'Name': name, 'Balance': balance, 'Currency': currency}

            else:   # if it's an old account
                name = account_already_in_2['Name']
                balance = round(float(account_already_in_2['Balance']) + float(transaction['ToSUM']), 2)
                currency = account_already_in_2['Currency']

                new_account_2 = {'Name': name, 'Balance': balance, 'Currency': currency}

            accounts_name_type_transfer.append(new_account_1)
            accounts_name_type_transfer.append(new_account_2)

    # cycle which distribute a name of an account
    for i in range(len(accounts_name_type_transfer)):
        # if account in expenses, then it's not a savings
        for k in range(len(accounts_name_type_income_or_expenses)):
            try:
                if accounts_name_type_transfer[i]['Name'] == accounts_name_type_income_or_expenses[k]['Name']:
                    # I used this way, cause else the cycle will be losing elements, when it's deleting they
                    # because he check the list step by step
                    accounts_name_type_income_or_expenses[k]['Balance'] += accounts_name_type_transfer[i]['Balance']

                    accounts_name_type_transfer[i] = None
                    break

            except TypeError:
                continue


    # deleting all None
    accounts_name_type_income_or_expenses = [i for i in accounts_name_type_income_or_expenses if i is not None]
    accounts_name_type_transfer = [i for i in accounts_name_type_transfer if i is not None]

    return accounts_name_type_income_or_expenses, accounts_name_type_transfer


def set_accounts_data_from_1money(may_new_accounts_names_list,
                                  accounts_data_file_path='data_files/accounts-data.txt'):
    # getting old data
    accounts_data_file = open(accounts_data_file_path, mode='r+', encoding='utf-8-sig')

    old_lines = accounts_data_file.readlines()

    last_num_of_account = int(old_lines[-1].split('-')[0].split('_')[1])

    old_accounts_names = []
    # getting old data
    for line in accounts_data_file:
        account_name = line.split('-')[1]
        old_accounts_names.append(account_name)

    accounts_data_file.close()

    # set new accounts
    with open(accounts_data_file_path, mode='w+', encoding='utf-8-sig') as accounts_data_file:
        for old_line in old_lines:
            accounts_data_file.write(old_line)

        for account in may_new_accounts_names_list:
            if not account in old_accounts_names:
                last_num_of_account += 1
                accounts_data_file.write('account_' + str(last_num_of_account) + '-' + account['Name'] +
                                         '-' + '0, .41, .24, 1' + '-' + account['Balance'] + '-' + account['Currency'] +'\n')


def set_savings_data_from_1money(savings_names_list, savings_data_file_path='data_files/savings-data.txt'):
    pass


def set_categories_data_from_1money(data_from_1money_dict, categories_data_file_path='data_files/categories-data.txt'):
    # getting old data
    categories_dict = {}
    old_categories_list = []
    last_category_num = 0
    with open(categories_data_file_path, mode='r+', encoding='utf-8-sig') as categories_data_file:
        for line in categories_data_file:
            categories_id, name, color = line[:-1].split('-')
            if name != '+':
                old_categories_list.append(name)
                categories_dict[categories_id] = {'Name': name, 'Color': color}
                last_category_num += 1

    # getting categories from 1Money
    new_categories_list = []
    for transaction in data_from_1money_dict:
        if data_from_1money_dict[transaction]['Type'] == 'Expenses':
            name = data_from_1money_dict[transaction]['To']['Name']
            if not name in new_categories_list:
                if not name in old_categories_list:
                    new_categories_list.append(name)

    # adding new categories to dictionary with color
    for name in new_categories_list:
        categories_dict['Categories_' + str(last_category_num)] = {'Name': name, 'Color': '.38, .39, .61, 1'}
        last_category_num += 1

    # setting all categories to file
    with open(categories_data_file_path, mode='w+', encoding='utf-8-sig') as categories_data_file:
        for category_id in categories_dict:
            name = categories_dict[category_id]['Name']
            color = categories_dict[category_id]['Color']
            categories_data_file.write(
                category_id + '-' + name + '-' + color + '\n'
            )
        # adding missing categories
        if last_category_num < 15:
            for num in range(last_category_num, 16):
                category_id = 'Categories_' + str(num)
                name = '+'
                color = '.38, .39, .61, 1'
                categories_data_file.write(
                    category_id + '-' + name + '-' + color + '\n'
                )

def set_incomes_data_from_1money():
    pass


if __name__ == '__main__':
    print('Что нужно проверить?')
    print('1. get_accounts_and_savings_names')
    print('2. set_accounts_data_from_1money')
    print('3. set_savings_data_from_1money')
    print('4. set_categories_data_from_1money')

    from GetDataFrom1Money import get_data_from_1money
    data_dict_from_1money = get_data_from_1money()

    n = int(input('Ответ (цифра): '))

    if n == 1:
        accounts_and_savings_names = get_accounts_and_savings_names(data_from_1money_dict=data_dict_from_1money)
        accounts_names_list, savings_names_list = accounts_and_savings_names[0], accounts_and_savings_names[1]

        print(f"accounts' names: {accounts_names_list}")
        print(f"savings' names: {savings_names_list}")

    elif n == 2:
        accounts_and_savings_names = get_accounts_and_savings_names(data_from_1money_dict=data_dict_from_1money)
        accounts_names_list, savings_names_list = accounts_and_savings_names[0], accounts_and_savings_names[1]

        set_accounts_data_from_1money(accounts_names_list)

    elif n == 3:
        pass

    elif n == 4:
        set_categories_data_from_1money(data_dict_from_1money)
