# Generated by Django 4.2.4 on 2024-10-23 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('address', models.TextField()),
                ('admission_number', models.CharField(editable=False, max_length=4, unique=True)),
                ('date_of_enrollment', models.DateField()),
                ('current_class', models.CharField(max_length=50)),
                ('section', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=10)),
                ('total_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fees_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('outstanding_fees', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=255)),
                ('issue_date', models.DateField()),
                ('issued_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='FeesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('total_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fees_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('outstanding_fees', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]
