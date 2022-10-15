print('# Txt-catrgories-data.py is open')

try:
    categories_data_file = open('Data\data_files\categories-data.txt', 'r')
    categories_data_file.close()

    print('# data_file: categories-data.txt is read')

except FileNotFoundError:
    categories_data_file = open('Data\data_files\categories-data.txt', 'a')
    categories_data_file.close()

    print('# data_file: categories-data.txt is done')

    categories_data_file = open('Data\data_files\categories-data.txt', 'w+')

    for i in range(1, 12 + 1):
        categories_data_file.write(str(i) + '-' + str(i) + '\n')

    print('# data_file: categories-data.txt is written')
