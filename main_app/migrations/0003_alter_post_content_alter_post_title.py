# Generated by Django 4.1.3 on 2022-11-24 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_rename_user_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(help_text='Enter the content of the post', max_length=5000),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Enter a post title', max_length=100),
        ),
    ]
