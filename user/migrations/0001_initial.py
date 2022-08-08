# Generated by Django 4.0.6 on 2022-08-03 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('park', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=50, verbose_name='지역')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='사용자 계정')),
                ('password', models.CharField(max_length=128, verbose_name='비밀번호')),
                ('fullname', models.CharField(max_length=20, verbose_name='사용자 이름')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='이메일')),
                ('phone', models.CharField(max_length=20, verbose_name='핸드폰 번호')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='가입일자')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=True)),
                ('bookmarks', models.ManyToManyField(related_name='users', through='park.BookMark', to='park.park', verbose_name='즐겨찾기')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.region', verbose_name='지역')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
