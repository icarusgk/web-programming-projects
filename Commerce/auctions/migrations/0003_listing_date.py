# Generated by Django 3.1.1 on 2020-10-02 01:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]