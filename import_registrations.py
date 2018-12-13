"""
Import data from contao
"""
import csv
import datetime
import locale
import re
import sqlite3
import time

from registration.models import Registration


def time_converter(text: str):
    match = re.match('(?P<start_hour>\d+)[.,:h]+(?P<start_min>\d+)$', text)
    if match:
        return (datetime.time(hour=int(match.group('start_hour')), minute=int(match.group('start_min'))),
                datetime.time(hour=8 + int(match.group('start_hour')), minute=int(match.group('start_min'))))
    pattern = re.compile(
        '[\D]*(?P<start_hour>\d+)[.,:h]?(?P<start_min>\d*)[\D]+(?P<end_hour>\d+)[.,:h]?(?P<end_min>\d*)')
    match = pattern.match(text)
    if match:
        start_hour = int(match.group('start_hour'))
        start_minute = 0
        if match.group('start_min'):
            start_minute = int(match.group('start_min'))

        end_hour = int(match.group('end_hour'))
        end_minute = 0
        if match.group('end_min'):
            end_minute = int(match.group('end_min'))
        return (datetime.time(hour=start_hour, minute=start_minute), datetime.time(hour=end_hour, minute=end_minute))

    match = re.match('[\D]*(?P<hours>\d+)[\D]*', text)
    if match:
        return (datetime.time(hour=8, minute=30), datetime.time(hour=8 + int(match.group('hours')), minute=30))

    match = re.match('ganztags|pieno|full time|tempo pieno|In linea con Scuola Europea', text, re.IGNORECASE)
    if match:
        return (datetime.time(hour=8, minute=30), datetime.time(hour=17, minute=30))
    match = re.match('vormittags|morning|(Per iniziare solo la )?mattina|mattino|Mezzagiornata', text, re.IGNORECASE)
    if match:
        return (datetime.time(hour=8, minute=30), datetime.time(hour=13, minute=30))
    match = re.match('al momento non saprei|Wissen wir noch nicht genau', text, re.IGNORECASE)
    if match:
        return (datetime.time(hour=9, minute=0), datetime.time(hour=17, minute=30))
    match = re.match('pomeriggio', text, re.IGNORECASE)
    if match:
        return (datetime.time(hour=13, minute=0), datetime.time(hour=17, minute=30))

    raise ValueError('not found: %s' % (text))


def date_converter(text: str) -> datetime.date:
    found_date = datetime.date.today()
    try:
        is_int = int(text)
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
                '%d.%m.%Y', '%d.%m.%Y %H:%M', '%d.%m.%Y %H:%M:%S', '%Y.%m.%d', '%d-%m-%Y', '%Y-%m-%d', '%d %m %Y',
                '%d.%m.%y', '%d-%m-%y', '%d. %B %Y', '%d %B %Y', '%d%B%Y', '%d-%m-%Y %H:%M:%S', '%B %Y', '%d.%b. %Y',
                '%d.%m%Y'):
            try:
                tst = time.strptime(text, pattern)
                found_date = datetime.date(year=tst.tm_year, month=tst.tm_mon, day=tst.tm_mday)
                return found_date
            except ValueError:
                pass  # next try
    raise ValueError("can't find a date format for %s" % (text))


def insert_into_db(db: sqlite3.Connection, row) -> bool:
    db.execute("INSERT INTO request_request (start,time_from,time_to,child_pre_name,"
               "child_name, birth_date, sex, nationality, father_name, father_profession,"
               "father_nationality, father_legal, father_mobile, father_email,mother_name, mother_profession,"
               "mother_nationality, mother_legal, mother_mobile, mother_email,street, number, zip, city,"
               "fon, email, remark, urgency, privacy,data_protection, created, ip_address) VALUES (:start,:time_from,"
               ":time_to,:child_pre_name, :child_name, :birth_date, :sex, :nationality, :father_name, :father_profession,"
               ":father_nationality, :father_legal, :father_mobile, :father_email,:mother_name, :mother_profession,"
               ":mother_nationality, :mother_legal, :mother_mobile, :mother_email,:street, :number, :zip, :city,"
               ":fon, :email, :remark, :urgency, :privacy,:data_protection, :created, :ip_address, :language, "
               ":original_time,)",
               {
                   'start': start_date,
                   'time_from': start_time,
                   'time_to': end_time,
                   'child_pre_name': row[column_header['child_pre_name']],
                   'child_name': row[column_header['child_name']],
                   'birth_date': birth_day,
                   'sex': str.upper(row[column_header['sex']][:1]),
                   'nationality': str.upper(row[column_header['nationality']][:2]),
                   'father_name': row[column_header['father_name']],
                   'father_profession': row[column_header['father_profession']],
                   'father_nationality': str.upper(row[column_header['father_nationality']][:2]),
                   'father_legal': row[column_header['father_legal']],
                   'father_mobile': row[column_header['father_mobile']],
                   'father_email': row[column_header['father_email']],
                   'mother_name': row[column_header['mother_name']],
                   'mother_profession': row[column_header['mother_profession']],
                   'mother_nationality': str.upper(row[column_header['mother_nationality']][:2]),
                   'mother_legal': row[column_header['mother_legal']],
                   'mother_mobile': row[column_header['mother_mobile']],
                   'mother_email': row[column_header['mother_email']],
                   'street': row[column_header['street']],
                   'number': row[column_header['number']],
                   'zip': row[column_header['zip']],
                   'city': row[column_header['city']],
                   'fon': row[column_header['fon']],
                   'email': row[column_header['email']],
                   'remark': row[column_header['remark']],
                   'urgency': 'A',
                   'privacy': True,
                   'data_protection': True,
                   'published': created_date,
                   'ip_address': row[column_header['ip_address']],
                   'language': row[column_header['language']],
                   'original_time': row[column_header['time']],
               });
    return True


def convert_sex(text: str) -> str:
    return text


# db = sqlite3.connect('db.sqlite3', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
column_header = {}
Registration.objects.all().delete()

with open('registrations.csv', newline='') as csv_file:
    spamreader = csv.reader(csv_file, delimiter=',', quotechar='"')
    not_catched = 0
    for row in spamreader:
        if len(column_header) == 0:
            index = 0
            for x in row:
                column_header[x] = index
                index += 1
            print(column_header)
            continue
        try:
            birth_day = date_converter(row[column_header['birth_date']])
            start_date = date_converter(row[column_header['start']])
            created_date = date_converter(row[column_header['created']])
            (start_time, end_time) = time_converter(row[column_header['time']])
            print("%s %s %s %s %s %s" % (row[column_header['id']], created_date, start_date, birth_day, start_time,
                                         end_time))

            Registration.objects.create(
                start=start_date,
                time_from=start_time,
                time_to=end_time,
                child_pre_name=row[column_header['child_pre_name']],
                child_name=row[column_header['child_name']],
                birth_date=birth_day,
                sex=str.upper(row[column_header['sex']][:1]),
                nationality=str.upper(row[column_header['nationality']][:2]),
                father_name=row[column_header['father_name']],
                father_profession=row[column_header['father_profession']],
                father_nationality=str.upper(row[column_header['father_nationality']][:2]),
                father_legal=row[column_header['father_legal']],
                father_mobile=row[column_header['father_mobile']],
                father_email=row[column_header['father_email']],
                mother_name=row[column_header['mother_name']],
                mother_profession=row[column_header['mother_profession']],
                mother_nationality=str.upper(row[column_header['mother_nationality']][:2]),
                mother_legal=row[column_header['mother_legal']],
                mother_mobile=row[column_header['mother_mobile']],
                mother_email=row[column_header['mother_email']],
                street=row[column_header['street']],
                number=row[column_header['number']],
                zip=row[column_header['zip']],
                city=row[column_header['city']],
                fon=row[column_header['fon']],
                email=row[column_header['email']],
                remark=row[column_header['remark']],
                urgency='A',
                privacy=True,
                data_protection=True,
                created=created_date,
                ip_address=row[column_header['ip_address']],
                language=row[column_header['language']],
                original_time=row[column_header['time']],
                published=created_date,
            )

        except ValueError as exc:
            print("%d %s" % (row[column_header['id']], exc))
            not_catched += 1
        except OverflowError as exc:
            print("%d %s" % (row[column_header['id']], exc))
            not_catched += 1

print(not_catched)
