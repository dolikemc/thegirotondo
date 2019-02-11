import codecs
import csv
from unittest import TestCase


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
        self.italian_reader = csv.reader(self.german_csv, delimiter=';', quotechar='"', )

    def tearDown(self):
        self.german_csv.close()

    # "ID";"SORTING";"Mitglied";"Benutzer";"Mitgliedergruppe";"Benutzergruppe";"Formular";"IP-Adresse";"Datum";
    # "Best�tigungs-Mail gesendet";"Best�tigungs-Mail gesendet am";"Ver�ffentlicht";"Alias";"Bemerkung";
    # "Datum der Anmeldung";"Gew�nschter Eintrittstermin";"Gew�nschter Betreuungszeit (von ... bis)";"Vorname des Kindes";
    # "Nachname des Kindes";"Geburtdatum bzw. voraussichtl. Termin";"Geschlecht";
    # "Staatsangeh�rigkeit des Kindes";"Vater des Kindes (Vorname und Nachname)";"Beruf des Vaters";
    # "Staatsangeh�rigkeit des Vaters";"Familienstand des Vaters";"Handynummer des Vaters";"E-Mail des Vaters";
    # "Mutter des Kindes (Vorname und Nachname)";"Beruf der Mutter";"Staatsangeh�rigkeit der Mutter";"Familienstand der Mutter";
    # "Handynummer der Mutter";"E-Mail der Mutter";"Stra�e";"Hausnr.";"PLZ";"Ort";"Telefon";"Korrespondenz E-Mail";
    # "Bemerkungen";"Angaben zur Platzvergabe nach Dringlichkeit";"Erkl�rung";"risposta_comitato";"data_incontro";"Varie"
    def test_german_header(self):
        header_array = []
        for first_row in self.german_reader:
            for column in first_row:
                header_array.append(column)
            break
        self.assertEqual(len(header_array), 46)
        self.assertEqual('ID', header_array[0])
        self.assertEqual('SORTING', header_array[1])
        self.assertEqual('Formular', header_array[6])
        self.assertEqual('Varie', header_array[45])
        self.assertEqual('Bestätigungs-Mail gesendet', header_array[9])

    def test_italian_header(self):
        header_array = []
        for first_row in self.italian_reader:
            for column in first_row:
                header_array.append(column)
            break
        self.assertEqual(len(header_array), 46)
        self.assertEqual('ID', header_array[0])
        self.assertEqual('SORTING', header_array[1])
        self.assertEqual('Formular', header_array[6])
        self.assertEqual('Varie', header_array[45])
        self.assertEqual('Bestätigungs-Mail gesendet', header_array[9])
