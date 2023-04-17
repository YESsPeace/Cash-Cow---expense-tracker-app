from database import accounts_db_read, savings_db_read


def calculate(expression):
    if '+' in expression:
        num_1, num_2 = expression.split('+')
        answer = float(num_1[2:]) + float(num_2)
        answer = float("{:.2f}".format(answer))
        if answer % 1 == 0:
            answer = int(answer)

        return str(answer)

    elif '-' in expression:
        num_1, num_2 = expression.split('-')
        answer = float(num_1[2:]) - float(num_2)
        answer = float("{:.2f}".format(answer))
        if answer % 1 == 0:
            answer = int(answer)

        return str(answer)

    elif '÷' in expression:
        num_1, num_2 = expression.split('÷')
        answer = float(num_1[2:]) / float(num_2)
        answer = float("{:.2f}".format(answer))
        if answer % 1 == 0:
            answer = int(answer)

        return str(answer)

    elif 'x' in expression:
        num_1, num_2 = expression.split('x')
        answer = float(num_1[2:]) * float(num_2)
        answer = float("{:.2f}".format(answer))
        if answer % 1 == 0:
            answer = int(answer)

        return str(answer)

    else:
        return False

def get_total_accounts_balance():
    return sum([value_dict['Balance'] for value_dict in (accounts_db_read() | savings_db_read()).values()])