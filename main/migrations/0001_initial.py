# Generated by Django 2.1.3 on 2018-11-22 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10)),
                ('curp', models.CharField(max_length=18)),
                ('nombre', models.CharField(max_length=255)),
                ('apellidop', models.CharField(max_length=255)),
                ('apellidom', models.CharField(max_length=255)),
                ('sexo', models.CharField(choices=[('m', 'Mujer'), ('h', 'Hombre')], max_length=1)),
                ('fechanac', models.DateField()),
                ('salario', models.FloatField()),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Empleado')),
            ],
        ),
    ]