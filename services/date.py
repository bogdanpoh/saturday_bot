import calendar
import locale
from datetime import date

import config
from helpers import constants


class DateManager(object):
    date_from = None

    @staticmethod
    def day_name(date):
        return date.strftime(constants.day_name_format).capitalize()

    @staticmethod
    def is_weekday(date):
        return constants.is_weekday if date.weekday() < 5 else constants.is_weekend

    def __init__(self, date_from, dev_locale=True):
        self.date_from = date_from
        locale_config = config.locale_dev if dev_locale else config.locale_production
        locale.setlocale(locale.LC_ALL, locale_config)

        # locale.setlocale(locale.LC_ALL, 'ru_UA.utf8')
        # uk_UA.UTF - 8
        # locale.setlocale(locale.LC_ALL, 'C')

    def current_date(self):
        return "{0} {1} {2}".format(
            self.date_from.day,
            self.date_from.strftime(constants.month_name_format),
            self.date_from.year
        )

    def date_to_event(self, to_day):
        return date(self.date_from.year, self.date_from.month, to_day)

    def prepare_info(self, text, day_to):
        day_to_event = day_to - self.date_from.day
        date_event = self.date_to_event(self.date_from.day + day_to_event)
        day_name = DateManager.day_name(date_event)
        day_status = DateManager.is_weekday(date_event)

        answer = "{0} {1}: {2}\n({3}, {4})\n".format(constants.start_text, text, day_to_event, day_name, day_status) \
            if day_to_event > 0 \
            else "{0} {1}\n".format(constants.received_text, constants.done_emoji)
        return answer

    def to_prepayment_info(self, day_to):
        return self.prepare_info("авансу", day_to)

    def to_scholarship_info(self, day_to):
        return self.prepare_info("стипендії", day_to)

    def to_salary_info(self):
        last_day_month = calendar.monthrange(self.date_from.year, self.date_from.month)[-1]
        return self.prepare_info("ЗП", last_day_month)

    def get_info(self):
        current_date = self.current_date()
        prepayment = self.to_prepayment_info(day_to=constants.prepayment_day)
        scholarship = self.to_scholarship_info(day_to=constants.scholarship_day)
        salary = self.to_salary_info()

        info = "{0}\n\n{1}\n{2}\n{3}".format(current_date, prepayment, scholarship, salary)
        return info






