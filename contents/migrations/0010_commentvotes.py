# Generated by Django 3.2 on 2022-05-19 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contents', '0009_auto_20220519_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentVotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('vote', models.IntegerField(choices=[(1, 'up_vote'), (-1, 'down_vote')])),
                ('comment', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='contents.comment')),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
