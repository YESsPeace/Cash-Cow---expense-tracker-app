def get_accounts_and_savings_names(data_from_1money_dict):
    # data dict with all transactions
    money_dict = data_from_1money_dict

    # empty lists for return
    accounts_name_type_income_or_expenses = []
    accounts_name_type_transfer = []

    # cycle which get names from dict with all transaction data
    for transaction in money_dict.values():  # just addition into list, names' distribution will be soon
        if transaction['Type'] == 'Income':
            new_account_1 = transaction['To']['Name']

            if not new_account_1 in accounts_name_type_income_or_expenses:
                accounts_name_type_income_or_expenses.append(new_account_1)

        if transaction['Type'] == 'Expenses':
            new_account_1 = transaction['From']['Name']

            if not new_account_1 in accounts_name_type_income_or_expenses:
                accounts_name_type_income_or_expenses.append(new_account_1)

        elif transaction['Type'] == 'Transfer':
            new_account_1 = transaction['From']['Name']
            new_account_2 = transaction['To']['Name']

            if not new_account_1 in accounts_name_type_transfer:
                accounts_name_type_transfer.append(new_account_1)

            if not new_account_2 in accounts_name_type_transfer:
                accounts_name_type_transfer.append(new_account_2)

    # cycle which distribute a name of an account
    for account in accounts_name_type_transfer:
        # if account in expenses, then it's not a savings
        if account in accounts_name_type_income_or_expenses:
            accounts_name_type_transfer.remove(account)

    return accounts_name_type_income_or_expenses, accounts_name_type_transfer



def set_accounts_data_from_1money(may_new_accounts_names_list, accounts_data_file_path='data_files/Test_files/test_accounts-data.txt'):
    # getting old data
    from GetDataFilesData import get_accounts_data

    old_data_dict = get_accounts_data()

    accounts_data_file = open(accounts_data_file_path, mode='r+', encoding='utf-8-sig')

    old_lines = accounts_data_file.readlines()

    last_num_of_account = int(old_lines[-1].split('-')[0].split('_')[1])

    old_accounts_names = []
    for line in accounts_data_file:
        account_name = line.split('-')[1]
        old_accounts_names.append(account_name)

    accounts_data_file.close()

    with open(accounts_data_file_path, mode='w+', encoding='utf-8-sig') as accounts_data_file:
        for old_line in old_lines:
            accounts_data_file.write(old_line)

        for name in may_new_accounts_names_list:
            if not name in old_accounts_names:
                last_num_of_account += 1
                accounts_data_file.write('account_' + str(last_num_of_account) + '-' + name +
                                         '-' + '0, .41, .24, 1' + '\n')

def set_gategories_data_from_1money(savings_names_list, savings_data_file_path='data_files/savings-data.txt'):
    pass


def set_categories_data_from_1money(data_from_1money_dict, categories_data_file_path='data_files/categories-data.txt'):
    pass


if __name__ == '__main__':
    from GetDataFrom1Money import get_data_from_1money

    data_dict_from_1money = get_data_from_1money()

    accounts_and_savings_names = get_accounts_and_savings_names(data_from_1money_dict=data_dict_from_1money)
    accounts_names_list, savings_names_list = accounts_and_savings_names[0], accounts_and_savings_names[1]

    print(f"accounts' names: {accounts_names_list}")
    print(f"savings' names: {savings_names_list}")

    print()

    set_accounts_data_from_1money(accounts_names_list)
