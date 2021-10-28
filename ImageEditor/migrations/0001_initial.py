# Generated by Django 3.2.8 on 2021-10-27 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnerList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('video_title', models.CharField(max_length=50)),
                ('frame_path', models.CharField(max_length=200)),
                ('conner_name', models.CharField(max_length=50)),
                ('conner_start', models.IntegerField()),
                ('conner_last', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ImageCrop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left', models.IntegerField()),
                ('top', models.IntegerField()),
                ('right', models.IntegerField()),
                ('bottom', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoCapture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VideoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=200)),
                ('conner', models.CharField(max_length=5)),
            ],
        ),
    ]
