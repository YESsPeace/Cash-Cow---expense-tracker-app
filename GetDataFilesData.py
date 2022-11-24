def get_accounts_data(accounts_data_file_path='data_files/Test_files/test_accounts-data.txt'):
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
                color = tuple([float(i) for i in data_list[2].split(',')])

                accounts_data_dict['Accounts'][data_list[0]] = {}

                accounts_data_dict['Accounts'][data_list[0]]["Name"] = data_list[1]
                accounts_data_dict['Accounts'][data_list[0]]["Color"] = color
                accounts_data_dict['Accounts'][data_list[0]]["Balance"] = data_list[3]
                accounts_data_dict['Accounts'][data_list[0]]["Currency"] = data_list[4][:-1]

            except IndexError:
                # if we do not have some data
                continue

        elif is_savings:
            data_list = line.split('-')

            try:
                color = tuple([float(i) for i in data_list[2].split(',')])

                accounts_data_dict['Savings'][data_list[0]] = {}

                accounts_data_dict['Savings'][data_list[0]]["Name"] = data_list[1]
                accounts_data_dict['Savings'][data_list[0]]["Color"] = color
                accounts_data_dict['Savings'][data_list[0]]["Balance"] = data_list[3]
                accounts_data_dict['Savings'][data_list[0]]["Currency"] = data_list[4][:-1]


            except IndexError:
                # if we do not have some data
                # or do not have any accounts of this type
                continue

    return accounts_data_dict

def get_categories_data_from(categories_data_file_path='data_files/Test_files/test_categories-data.txt'):
    categories_data_dictionary = {}

    try:
        with open(categories_data_file_path, mode='r+', encoding='utf-8-sig') as categories_data_file:
            for line in categories_data_file:
                line = line.split('-')

                number_of_category = line[0]
                name = line[1]
                color = tuple([float(i) for i in line[2][:-1].split(',')])

                categories_data_dictionary[number_of_category] = {
                    "Name": name,
                    "Color": color
                }

    except FileNotFoundError:
        for number_of_category in range(16):
            categories_data_dictionary['Categories_' + str(number_of_category)] = {
                "Name": 'FileNotFoundError',
                "Color": (0, 0, 0, 1)
            }

    return categories_data_dictionary

if __name__ == '__main__':
    print(get_accounts_data())
    print()
    print(get_categories_data_from())