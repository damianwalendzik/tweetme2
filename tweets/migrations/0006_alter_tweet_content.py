# Generated by Django 4.0.6 on 2022-07-31 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_tweet_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
