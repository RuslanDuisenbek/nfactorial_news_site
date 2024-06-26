# Generated by Django 5.0.3 on 2024-04-10 09:22

import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Category')),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='TagPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads_model')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d', verbose_name='Photo')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time Created')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Time Updated')),
                ('is_published', models.BooleanField(choices=[(False, 'Draft'), (True, 'Published')], default=0, verbose_name='Status')),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='news.category', verbose_name='Category')),
                ('tag', models.ManyToManyField(blank=True, related_name='tags', to='news.tagpost')),
            ],
            options={
                'verbose_name': 'Kazakh News',
                'verbose_name_plural': 'Kazakh News',
                'ordering': ('-time_create',),
                'indexes': [models.Index(fields=['-time_create'], name='news_news_time_cr_5badca_idx')],
            },
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
    ]
