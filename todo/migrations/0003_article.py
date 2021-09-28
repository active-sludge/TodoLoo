# Generated by Django 3.2.6 on 2021-09-28 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todo_date_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False)),
                ('article_title', models.TextField(blank=True, null=True)),
                ('article_abstract', models.TextField(blank=True, null=True)),
                ('author_list', models.TextField(blank=True, null=True)),
                ('keyword_list', models.TextField(blank=True, null=True)),
                ('pub_date', models.TextField(blank=True, null=True)),
            ],
        ),
    ]