# Generated by Django 2.1.5 on 2019-09-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binder', '0003_auto_20190922_0505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='cover_image',
        ),
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(default='books/empty_cover.jpg', upload_to='books/'),
        ),
    ]