# Generated by Django 4.0.3 on 2022-04-08 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_rename_body_post_content_remove_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]