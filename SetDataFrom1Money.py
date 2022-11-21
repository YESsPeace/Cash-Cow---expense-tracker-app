from GetDataFrom1Money import get_data_from_1money


def set_accounts_data_from_1money(data_from_1money_dict, accounts_data_file_path='data_files/accounts-data.txt'):
    # getting old data
    from GetDataFilesData import get_accounts_data_from_accounts_data_txt

    old_data_dict = get_accounts_data_from_accounts_data_txt()


def set_categories_data_from_1money(data_from_1money_dict, categories_data_file_path='data_files/categories-data.txt'):
    pass


if __name__ == '__main__':
    data_dict_from_1money = get_data_from_1money()
    set_accounts_data_from_1money(data_from_1money_dict=data_dict_from_1money)
