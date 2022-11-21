def create_categories_data_file(path):
    print('# Txt-catrgories-data.py is open')

    try:
        categories_data_file = open(path, 'r')
        categories_data_file.close()

        print('# data_file: categories-data.txt is read')

    except FileNotFoundError:
        categories_data_file = open(path, 'a')
        categories_data_file.close()

        print('# data_file: categories-data.txt is done')

        categories_data_file = open(path, 'w+')

        for i in range(4*4):
            categories_data_file.write('CategoriesMenu_Button_' + str(i) + '-' + '+' + '-' + '.38, .39, .61, 1' + '\n')

        print('# data_file: categories-data.txt is written')
