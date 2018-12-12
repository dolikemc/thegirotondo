# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from django.db import models


# Create your models here.
class AccordionContainer(CMSPlugin):
    def __unicode__(self):
        return "%d columns".format(self.cmsplugin_set.all().count())


class AccordionTab(CMSPlugin):
    title = models.CharField(verbose_name='title', max_length=200, default='')

    def __unicode__(self):
        return self.title
