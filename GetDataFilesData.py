def get_accounts_data_from_accounts_data_txt(accounts_data_file_path='data_files/accounts-data.txt'):
    accounts_data_dict = {"Accounts": {}, "Savings": {}}

    try:
        accounts_and_savings_data_file = open(accounts_data_file_path, 'r+', encoding="utf-8-sig")

    except FileNotFoundError:
        return {"Accounts": {"Name": 'Error! Please check that the files is here', "Color": '0, 0, 0, 1',
                             'Balance': "0", 'Currency': 'None'}, "Savings": {}}

    # check flags
    is_accounts = False
    is_savings = False

    for line in accounts_and_savings_data_file:
        if line.split()[0] == 'accounts':
            is_accounts = True
            is_savings = False

        elif line.split()[0] == 'savings':
            is_accounts = False
            is_savings = True

        elif is_accounts:
            data_list = line.split('-')

            try:
                color = data_list[2]

                accounts_data_dict['Accounts'][data_list[0]] = {"Name": data_list[1], "Color": color,
                                                                'Balance': data_list[3], 'Currency': data_list[4][:-1]}
            except IndexError:
                continue

        elif is_savings:
            data_list = line.split('-')

            try:
                color = data_list[2]

                accounts_data_dict['Savings'][data_list[0]] = {"Name": data_list[1], "Color": color,
                                                               'Balance': data_list[3], 'Currency': data_list[4][:-1]}
            except IndexError:
                continue

    return accounts_data_dict


if __name__ == '__main__':
    print(get_accounts_data_from_accounts_data_txt())
