def create_accounts_data_file(path):
    print('# Txt-accounts-data.py is open')

    try:
        accounts_data_file = open(path, 'r')
        accounts_data_file.close()

        print("# data_file: TxtAccountsData is done")

    except:
        accounts_data_file = open(path, 'a+')
        accounts_data_file.close()
        print("# data_file: TxtAccountsData is created")

