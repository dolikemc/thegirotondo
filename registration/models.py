from datetime import time, datetime

from django.db import models
from django.urls import reverse

"""Kinder, deren Mutter oder Vater alleinerziehend und berufstätig oder 
in Ausbildung ist, sowie Kinder deren beide Elternteile berufstätig oder in Ausbildung sind, soweit Umfang und
Lage der Arbeitszeit bzw. Unterrichtszeit die Betreuung erforderlich machen"""


# Create your models here.
class Registration(models.Model):
    SEX = (('M', 'male'), ('F', 'female'))
    URGENCY = (('A', """Familien, die gemäß §27 i.V.m.§36 SGB VIII der „Hilfe zur Erziehung“ bedürfen"""),
               ('B', 'Alleinerziehend'),
               ('S', "Soziale Härtefälle"))
    start = models.DateField(verbose_name='Gewünschter Eintrittstermin')
    time_from = models.TimeField(verbose_name='Betreuungszeit von:', default=time(hour=9))
    time_to = models.TimeField(verbose_name='Betreuungszeit bis:', default=time(hour=17))
    child_pre_name = models.CharField(verbose_name='Vorname des Kindes', max_length=255)
    child_name = models.CharField(verbose_name='Nachname des Kindes', max_length=255)
    birth_date = models.DateField(verbose_name='Geburtstag bzw Termin')
    sex = models.CharField(max_length=1, verbose_name='Geschlecht', choices=SEX)
    nationality = models.CharField(max_length=2, verbose_name='Staatsangeörigkeit', default='DE')
    father_name = models.CharField(verbose_name='Vor- und Nachname des Vater', max_length=255)
    father_profession = models.CharField(verbose_name='Beruf des Vaters', max_length=255)
    father_nationality = models.CharField(max_length=2, verbose_name='Staatsangeörigkeit des Vaters', default='DE')
    father_legal = models.CharField(max_length=64, verbose_name='Familienstand des Vaters', default='verheiratet')
    father_mobile = models.CharField(verbose_name='Handynummer des Vaters', max_length=255)
    father_email = models.EmailField(verbose_name='Email des Vaters')
    mother_name = models.CharField(verbose_name='Vor- und Nachname der Mutter', max_length=255)
    mother_profession = models.CharField(verbose_name='Beruf der Mutter', max_length=255)
    mother_nationality = models.CharField(max_length=2, verbose_name='Staatsangeörigkeit der Mutter', default='DE')
    mother_legal = models.CharField(max_length=64, verbose_name='Familienstand der Mutter', default='verheiratet')
    mother_mobile = models.CharField(verbose_name='Handynummer der Mutter', max_length=255)
    mother_email = models.EmailField(verbose_name='Email der Mutter')
    street = models.CharField(verbose_name='Straße', max_length=255)
    number = models.CharField(verbose_name='Hausnummer', max_length=64)
    zip = models.CharField(verbose_name='Postleitzahl', max_length=64)
    city = models.CharField(verbose_name='Stadt', max_length=64)
    fon = models.CharField(verbose_name='Telefonnummer', max_length=64)
    email = models.EmailField(verbose_name='Email für die Korrespondenz')
    remark = models.CharField(verbose_name='Anmerkungen', max_length=255, blank=True)
    urgency = models.CharField(max_length=1, verbose_name='Dringlichkeit', choices=URGENCY)
    privacy = models.BooleanField()
    data_protection = models.BooleanField()
    created = models.DateTimeField(editable=False, auto_now=True)
    ip_address = models.CharField(editable=False, max_length=64)
    language = models.CharField(max_length=2, blank=True, null=True)
    original_time = models.CharField(editable=False, max_length=64, default='')
    published = models.DateTimeField(blank=True, null=True)

    @property
    def age(self) -> int:
        return int((datetime.today().date() - self.birth_date).days / 365)

    def get_absolute_url(self) -> str:
        # todo: answer page
        return reverse('thanks-request')

    def __str__(self):
        return "%d %s %s: %s" % (self.id, self.child_pre_name, self.child_name, self.email)
