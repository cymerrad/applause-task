# Generated by Django 2.2.2 on 2019-06-30 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('deviceId', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tester',
            fields=[
                ('testerId', models.IntegerField(primary_key=True, serialize=False)),
                ('firstName', models.TextField(max_length=30, verbose_name='first name')),
                ('lastName', models.TextField(max_length=30, verbose_name='last name')),
                ('country', models.TextField(max_length=2, verbose_name='country ID')),
                ('lastLogin', models.DateTimeField(verbose_name='last login')),
            ],
        ),
        migrations.CreateModel(
            name='TesterDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester_matching.Device')),
                ('testerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester_matching.Tester')),
            ],
        ),
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('bugId', models.IntegerField(primary_key=True, serialize=False)),
                ('deviceId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester_matching.Device')),
                ('testerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester_matching.Tester')),
            ],
        ),
    ]
