import datetime as dt
date_format = '%d.%m.%Y'

class Record:
    def __init__(self, comment, amount, date=None): 
        self.amount = amount
        self.comment = comment
        
        if date is not None:
            '''Форматирует строку с датой в формат даты.'''
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
        return sum(record.amount for record in self.records if record.date == today)

    def get_week_stats(self):
        today = dt.datetime.today().date()
        week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records if week_ago <= record.date <= today)


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """Определяет, сколько ещё можно съесть сегодня."""
        available_today = self.limit - self.get_today_stats()
        if self.get_today_stats() <  self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {available_today} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.00
    EURO_RATE = 86.00

    def get_today_cash_remained(self, currency):
        currency_rate_dict = {'rub': 1, 'usd': self.USD_RATE, 'eur': self.EURO_RATE}
        currency_name_dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        #можно создать get_today_remained в родительском калькуляторе и обращаться к нему, а не 2 раза в кальках делать отдельно одно и то же
        self.available_today = abs(round((self.limit - self.get_today_stats()) / currency_rate_dict[currency], 2))
        """Считает доступный остаток в запрошенной валюте, округляя до 2-х знаков после запятой."""
        if self.get_today_stats() <  self.limit:
            return (f'На сегодня осталось {self.available_today} {currency_name_dict[currency]}')
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        return (f'Денег нет, держись: твой долг - {self.available_today} {currency_name_dict[currency]}')


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(-300)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('eur'))
