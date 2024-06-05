# Generated by Django 5.0 on 2024-03-16 14:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CaseInvetation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_approvment', models.BooleanField(default=False)),
                ('org_approvment', models.BooleanField(default=False)),
                ('invetation_status', models.CharField(choices=[('pending', 'قيد الانتظار'), ('accepted', 'مقبول'), ('rejected', 'مرفوض')], max_length=15)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('invetation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cases.caseinvetation')),
            ],
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subject', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='news/images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.lawyer')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.new')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.new')),
            ],
        ),
        migrations.CreateModel(
            name='SolvedCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subject', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.lawyer')),
            ],
        ),
    ]
