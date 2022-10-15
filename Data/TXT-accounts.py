print('# Txt-catrgories-data.py is open')

try:
    accounts_data_file = open('Data\data_files\\accounts-data.txt', 'r')
    accounts_data_file.close()

    print("# data_file: transaction-history.csv is open'")

except FileNotFoundError:
    accounts_data_file = open('Data\data_files\\accounts-data.txt', 'a')
    accounts_data_file.close()

    print('# data_file: accounts-data.txt is done')
