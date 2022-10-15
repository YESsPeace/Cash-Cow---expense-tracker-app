print('# Txt-catrgories-data.py is open')

categories_data_file = open('Data\data_files\categories-data.txt', 'a')
categories_data_file.close()

print('# categories-data.txt is done')

categories_data_file = open('Data\data_files\categories-data.txt', 'w+')

for i in range(1, 12 + 1):
    categories_data_file.write(str(i) + '-' + str(i) + '\n')

print('# categories-data.txt is written')
