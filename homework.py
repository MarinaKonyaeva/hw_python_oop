import datetime as dt
date_format = '%d.%m.%Y'


class Record:
    def __init__(self, comment, amount, date=None):
        self.amount = amount
        self.comment = comment

        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.datetime.today().date()


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.today().date()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.datetime.today().date()
        week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if week_ago <= record.date <= today)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        available_today = self.limit - self.get_today_stats()
        if self.get_today_stats() < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {available_today} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.00
    EURO_RATE = 86.00

    def get_today_cash_remained(self, currency):
        currency_rate_dict = {'rub': 1, 'usd': self.USD_RATE, 
                              'eur': self.EURO_RATE}
        currency_name_dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        self.available_today = self.limit - self.get_today_stats()
        self.change_currency = self.available_today / currency_rate_dict[currency]
        self.formated_answer = abs(round(self.change_currency, 2))
        if self.get_today_stats() < self.limit:
            return (f'На сегодня осталось '
                    f'{self.formated_answer} {currency_name_dict[currency]}')
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        return (f'Денег нет, держись: твой долг - '
                f'{self.formated_answer} {currency_name_dict[currency]}')
