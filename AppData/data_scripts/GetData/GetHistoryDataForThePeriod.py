def get_transaction_for_the_period(from_date, to_date):
    pass


if __name__ == '__main__':
    import datetime

    date_today = datetime.date.today()
    first_day = date_today.replace(day=1)

    get_transaction_for_the_period(
        from_date=str(first_day),
        to_date=str(date_today)
    )
