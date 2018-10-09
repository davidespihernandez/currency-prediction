# Generated by Django 2.1.2 on 2018-10-09 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=3)),
                ('date', models.DateField(db_index=True)),
                ('goal', models.CharField(max_length=3)),
                ('rate', models.DecimalField(decimal_places=6, max_digits=14)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='exchange',
            unique_together={('base', 'date', 'goal')},
        ),
    ]