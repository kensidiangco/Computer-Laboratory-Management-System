# Generated by Django 4.1 on 2022-09-03 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_studentlistexcelfile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentListExcelFile',
        ),
        migrations.AddField(
            model_name='sched_request',
            name='class_list',
            field=models.FileField(blank=True, null=True, upload_to='student/excel', verbose_name='students'),
        ),
    ]