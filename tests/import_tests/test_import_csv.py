import codecs
import csv
import datetime
from unittest import TestCase

from tests.import_tests.base import ContaoParser


class TestCSV(TestCase):
    def setUp(self):
        self.german_csv = codecs.open('tests/import_tests/export_fd_anmeldung_20190209_112515.csv', "r",
                                      encoding='iso-8859-1',
                                      # encoding='utf-8',
                                      errors='ignore')
        self.german_reader = csv.reader(self.german_csv, delimiter=';', quotechar='"', )
        self.italian_csv = codecs.open('tests/import_tests/export_fd_preiscrizione_20190209_112528.csv', "r",
                                       encoding='iso-8859-1',
                                       # encoding='utf-8',
                                       errors='ignore')
        self.italian_reader = csv.reader(self.italian_csv, delimiter=';', quotechar='"', )

    def tearDown(self):
        self.german_csv.close()
        self.italian_csv.close()

    def read_line(self, reader, line_number):
        header_array = []
        counter = 0
        for first_row in reader:
            counter += 1
            if counter == line_number:
                for column in first_row:
                    header_array.append(column)
                return header_array

    def test_german_header(self):
        header_array = self.read_line(self.german_reader, 1)
        self.assertEqual(len(header_array), 46)
        self.assertEqual('ID', header_array[0])
        self.assertEqual('SORTING', header_array[1])
        self.assertEqual('Formular', header_array[6])
        self.assertEqual('Varie', header_array[45])
        self.assertEqual('Bestätigungs-Mail gesendet', header_array[9])

    def test_italian_header(self):
        header_array = self.read_line(self.italian_reader, 1)
        self.assertEqual(len(header_array), 42)
        self.assertEqual('ID', header_array[0])
        self.assertEqual('SORTING', header_array[1])
        self.assertEqual('Formular', header_array[6])
        self.assertEqual('Dichiarazione', header_array[41])
        self.assertEqual('Bestätigungs-Mail gesendet', header_array[9])

    def test_german_data(self):
        # "332";"0";"-";"-";"-";"-";"anmeldung";"62.216.206.0";"31.01.2019 20:32";"ja";"31.01.2019 20:32";
        header_array = self.read_line(self.german_reader, 3)
        self.assertEqual(len(header_array), 46)
        self.assertEqual('332', header_array[0])
        self.assertEqual('0', header_array[1])
        self.assertEqual('anmeldung', header_array[6])
        self.assertEqual('', header_array[45])
        self.assertEqual('31.01.2019 20:32', header_array[8])

    def test_italian_data(self):
        # "327";"0";"-";"-";"-";"-";"Preiscrizione";"46.128.208.0";"29.01.2019 22:15";"ja";"29.01.2019 22:15";
        header_array = self.read_line(self.italian_reader, 2)
        self.assertEqual(len(header_array), 42)
        self.assertEqual('327', header_array[0])
        self.assertEqual('0', header_array[1])
        self.assertEqual('Preiscrizione', header_array[6])
        self.assertEqual('', header_array[41])
        self.assertEqual('29.01.2019 22:15', header_array[8])

    def test_contao_converter_date(self):
        test = ContaoParser('27.11.2018 11:16')
        self.assertEqual(datetime.date(2018, 11, 27), test.to_date)
        test.text = '05.11.2018 14:40:06'
        self.assertEqual(datetime.date(2018, 11, 5), test.to_date)
        test.text = '1490050800'
        self.assertEqual(datetime.date(2017, 3, 21), test.to_date)

    def test_contao_converter_timeframe(self):
        test = ContaoParser('10:00 - 11:16')
        self.assertEqual((datetime.time(hour=10, minute=0), datetime.time(hour=11, minute=16)), test.to_datetime)

    def test_all(self):
        list_out = open('tests/import_tests/out.csv', 'w')
        out = csv.writer(list_out, dialect='excel')
        tag = ContaoParser('')
        write_row = list()
        for key in tag.get_mapping():
            write_row.append(key)
        out.writerow(write_row)
        for reader in (self.german_reader, self.italian_reader):
            for row in reader:
                if row[0] == 'ID':
                    continue
                write_row = list()
                for key in tag.get_mapping():
                    if tag.get_index(key) > 40:
                        continue
                    if 'date' in key:
                        write_row.append(ContaoParser(row[tag.get_index(key)]).to_date)
                    # elif 'time' in key: write_row.append(ContaoParser(row[tag.get_index(key)]).to_datetime)
                    else:
                        write_row.append(row[tag.get_index(key)])
                out.writerow(write_row)
        list_out.close()
