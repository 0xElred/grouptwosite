# Generated by Django 4.2.8 on 2025-05-14 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('gender_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tbl_genders',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=55)),
                ('birth_date', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=55)),
                ('other_phone_number', models.CharField(blank=True, max_length=55)),
                ('email', models.EmailField(blank=True, max_length=55)),
                ('username', models.CharField(max_length=55, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.gender')),
            ],
            options={
                'db_table': 'tbl_users',
            },
        ),
    ]
