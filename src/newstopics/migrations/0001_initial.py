# Generated by Django 2.1.5 on 2019-01-19 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news', '0003_news_is_delete'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsTopics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News')),
                ('topics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.Topics')),
            ],
            options={
                'db_table': 'news_topics',
            },
        ),
    ]