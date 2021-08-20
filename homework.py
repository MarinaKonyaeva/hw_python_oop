import datetime as dt


date_format = '%d.%m.%Y'


class Record:
    def __init__(self, comment, amount, date=None):
        self.amount = amount
        self.comment = comment

        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.date.today()


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if week_ago <= record.date <= today)

    def get_today_remained(self):
        return self.limit - self.get_today_stats()



class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        available_today = self.get_today_remained()
        if self.get_today_remained() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{available_today} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.00
    EURO_RATE = 86.00

    def get_today_cash_remained(self, currency):
        rate_dict = {'rub': 1, 'usd': self.USD_RATE,
                     'eur': self.EURO_RATE}
        currency_name_dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        change_currency = (self.get_today_remained() / rate_dict[currency])
        formated_answer = abs(round(change_currency, 2))
        currency_name = currency_name_dict[currency]
        if self.get_today_remained() > 0:
            return ('На сегодня осталось '
                    f'{formated_answer} {currency_name}')
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        return (f'Денег нет, держись: твой долг - '
                f'{formated_answer} {currency_name}')
