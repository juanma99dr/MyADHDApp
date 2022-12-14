# Generated by Django 4.1.3 on 2022-11-25 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='downvotes',
            field=models.PositiveIntegerField(default=0, help_text='Enter the number of downvotes the post has'),
        ),
        migrations.AlterField(
            model_name='post',
            name='upvotes',
            field=models.PositiveIntegerField(default=0, help_text='Enter the number of upvotes the post has'),
        ),
        migrations.AlterField(
            model_name='post',
            name='visits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
