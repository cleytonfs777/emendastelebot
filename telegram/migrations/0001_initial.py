# Generated by Django 4.1.7 on 2023-03-03 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeuser', models.CharField(max_length=50)),
                ('user_ident', models.IntegerField(blank=True)),
                ('data', models.CharField(max_length=11)),
                ('rep_dep', models.CharField(max_length=10)),
                ('is_writable', models.BooleanField(default=False)),
                ('tipo', models.CharField(choices=[('D', 'deputado'), ('A', 'acessor')], default='E', max_length=1)),
            ],
        ),
    ]
