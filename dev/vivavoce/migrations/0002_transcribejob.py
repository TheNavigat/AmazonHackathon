# Generated by Django 2.0.3 on 2018-03-23 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vivavoce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranscribeJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]
