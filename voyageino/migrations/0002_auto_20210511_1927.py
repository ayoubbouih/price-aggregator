# Generated by Django 3.2 on 2021-05-11 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyageino', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='operator',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='voyageino/static/img/operator/'),
        ),
    ]