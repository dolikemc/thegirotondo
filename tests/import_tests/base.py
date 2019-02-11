import datetime
import locale
import re
import time


class ContaoParser:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def get_index(column):
        return ContaoParser.get_mapping()[column]

    @staticmethod
    def get_mapping():
        return {'contao_id': 0,
                'title': 6,
                'ip-address': 7,
                'registration_date': 14,
                'start_date': 15,
                'time_frame_text': 16,
                'child_pre_name': 17,
                'child_sur_name': 18,
                'birth_date': 19,
                'gender': 20,
                'child_nationality': 21,
                'father_name': 22,
                'father_profession': 23,
                'father_nationality': 24,
                'father_martial_status': 25,
                'father_mobile': 26,
                'father_email': 27,
                'mother_name': 28,
                'mother_profession': 29,
                'mother_nationality': 30,
                'mother_martial_status': 31,
                'mother_mobile': 32,
                'mother_email': 33,
                'street': 34,
                'number': 35,
                'zip': 36,
                'city': 37,
                'phone': 38,
                'email': 39,
                'remark': 40,
                'angabe_platz_verwaltung': 41,
                'declaration': 42,
                'risposta_comitato': 43,  # only in german export
                'data_incontro': 44,  # only in german export
                'varie': 45}  # only in german export

    @property
    def to_date(self):

        found_date = datetime.date.today()
        try:
            is_int = int(self.text)
            if is_int > 1300000000:
                found_date = datetime.date.fromtimestamp(is_int)
            elif is_int > 20000000:
                tst = time.strptime(str(is_int), '%Y%m%d')
                found_date = datetime.date(year=tst.tm_year, month=tst.tm_mon, day=tst.tm_mday)
            elif is_int > 100000:
                tst = time.strptime(str(is_int), '%d%m%Y')
                found_date = datetime.date(year=tst.tm_year, month=tst.tm_mon, day=tst.tm_mday)
            elif is_int > 2000:
                found_date = datetime.date(year=is_int, month=1, day=1)
            return found_date

        except ValueError:
            pass  # next try 12.31.2011

        for date_local in (None, 'de_DE', 'it_IT', 'en_US'):
            locale.setlocale(locale.LC_TIME, date_local)
            for pattern in (
                    '%d.%m.%Y', '%d.%m.%Y %H:%M', '%d.%m.%Y %H:%M:%S', '%Y.%m.%d', '%d-%m-%Y', '%Y-%m-%d',
                    '%d %m %Y',
                    '%d.%m.%y', '%d-%m-%y', '%d. %B %Y', '%d %B %Y', '%d%B%Y', '%d-%m-%Y %H:%M:%S', '%B %Y',
                    '%d.%b. %Y',
                    '%d.%m%Y'):
                try:
                    tst = time.strptime(self.text, pattern)
                    found_date = datetime.date(year=tst.tm_year, month=tst.tm_mon, day=tst.tm_mday)
                    return found_date
                except ValueError:
                    pass  # next try
        raise ValueError("can't find a date format for %s" % self.text)

    @property
    def to_datetime(self):
        match = re.match(r'(?P<start_hour>\d+)[.,:h]+(?P<start_min>\d+)$', self.text)
        if match:
            return (datetime.time(hour=int(match.group('start_hour')), minute=int(match.group('start_min'))),
                    datetime.time(hour=8 + int(match.group('start_hour')), minute=int(match.group('start_min'))))
        pattern = re.compile(
            r'[\D]*(?P<start_hour>\d+)[.,:h]?(?P<start_min>\d*)[\D]+(?P<end_hour>\d+)[.,:h]?(?P<end_min>\d*)')
        match = pattern.match(self.text)
        if match:
            start_hour = int(match.group('start_hour'))
            start_minute = 0
            if match.group('start_min'):
                start_minute = int(match.group('start_min'))

            end_hour = int(match.group('end_hour'))
            end_minute = 0
            if match.group('end_min'):
                end_minute = int(match.group('end_min'))
            return (
                datetime.time(hour=start_hour, minute=start_minute), datetime.time(hour=end_hour, minute=end_minute))

        match = re.match(r'[\D]*(?P<hours>\d+)[\D]*', self.text)
        if match:
            return datetime.time(hour=8, minute=30), datetime.time(hour=8 + int(match.group('hours')), minute=30)

        match = re.match(r'ganztags|pieno|full time|tempo pieno|In linea con Scuola Europea', self.text, re.IGNORECASE)
        if match:
            return datetime.time(hour=8, minute=30), datetime.time(hour=17, minute=30)
        match = re.match(r'vormittags|morning|(Per iniziare solo la )?mattina|mattino|Mezzagiornata', self.text,
                         re.IGNORECASE)
        if match:
            return datetime.time(hour=8, minute=30), datetime.time(hour=13, minute=30)
        match = re.match(r'al momento non saprei|Wissen wir noch nicht genau', self.text, re.IGNORECASE)
        if match:
            return datetime.time(hour=9, minute=0), datetime.time(hour=17, minute=30)
        match = re.match(r'pomeriggio', self.text, re.IGNORECASE)
        if match:
            return datetime.time(hour=13, minute=0), datetime.time(hour=17, minute=30)

        raise ValueError('not found: %s' % self.text)
