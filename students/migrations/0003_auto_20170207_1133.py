# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-07 11:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20170207_1114'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='faqs',
            new_name='Faq',
        ),
    ]
