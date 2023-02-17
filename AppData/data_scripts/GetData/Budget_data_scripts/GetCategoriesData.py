def get_categories_budget_data(budget_data_file_path):
    try:
        with open(budget_data_file_path, encoding='utf-8') as budget_file:
            import csv

            reader = csv.reader(budget_file, delimiter=',')

            budget_data_dict = {}

            for row in reader:
                categories_id = row[0]

                budget_data_dict[row[0]] = {}

                budget_data_dict[categories_id]['Currency'] = row[1]
                budget_data_dict[categories_id]['SUM'] = row[2]

        return budget_data_dict

    except FileNotFoundError:
        return None


if __name__ == '__main__':
    print(*get_categories_budget_data(
        'C:/Users/damer/PycharmProjects/Money-statistics/AppData/data_files/Budget_files/2023-02/caregories-data.csv'
    ).items(), sep='\n')