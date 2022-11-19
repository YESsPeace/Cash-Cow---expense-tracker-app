def create_accounts_data_file(path):
    print('# Txt-catrgories-data.py is open')

    try:
        accounts_data_file = open(path, 'r')
        accounts_data_file.close()

        print("# data_file: transaction-history.csv is open'")

    except FileNotFoundError:
        accounts_data_file = open(path, 'a')
        accounts_data_file.close()

        print('# data_file: accounts-data.txt is done')
