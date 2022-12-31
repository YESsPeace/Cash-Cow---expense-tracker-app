def get_accounts_data(accounts_data_file_path):
    accounts_data_dict = {}

    try:
        accounts_data_file = open(accounts_data_file_path, 'r+', encoding="utf-8-sig")

    except FileNotFoundError:
        return {"Name": 'Error! Please check that the files is here', "Color": '0, 0, 0, 1',
                'Balance': "0", 'Currency': 'None'}

    for line in accounts_data_file:
        data_list = line.split('-')

        try:
            color = tuple([float(i) for i in data_list[2].split(',')])

            accounts_data_dict[data_list[0]] = {}

            accounts_data_dict[data_list[0]]["Name"] = data_list[1]
            accounts_data_dict[data_list[0]]["Color"] = color
            accounts_data_dict[data_list[0]]["Balance"] = data_list[3]
            accounts_data_dict[data_list[0]]["Currency"] = data_list[4][:-1]

        except IndexError:
            # if we do not have some data
            continue

    return accounts_data_dict


def get_savings_data(savings_data_file_path):
    savings_data_dict = {}

    try:
        savings_data_file = open(savings_data_file_path, 'r+', encoding="utf-8-sig")

    except FileNotFoundError:
        return {"Name": 'Error! Please check that the files is here', "Color": '0, 0, 0, 1',
                'Balance': "0", 'Currency': 'None'}

    for line in savings_data_file:
        data_list = line.split('-')

        try:
            color = tuple([float(i) for i in data_list[2].split(',')])

            savings_data_dict[data_list[0]] = {}

            savings_data_dict[data_list[0]]["Name"] = data_list[1]
            savings_data_dict[data_list[0]]["Color"] = color
            savings_data_dict[data_list[0]]["Balance"] = data_list[3]
            savings_data_dict[data_list[0]]["Goal"] = data_list[4]
            savings_data_dict[data_list[0]]["Currency"] = data_list[5][:-1]

        except IndexError:
            # if we do not have some data
            continue

    return savings_data_dict


def get_categories_data_from(categories_data_file_path):
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
    print(get_accounts_data(
        accounts_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_accounts-data.txt'
    ))
    print()
    print(get_savings_data(
        savings_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_savings-data.txt'
    ))
    print()
    print(get_categories_data_from(
        categories_data_file_path='C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Test_files/test_categories-data.txt'
    ))
