# Generated by Django 4.1.7 on 2023-03-31 10:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql=[('CREATE SCHEMA IF NOT EXISTS content;')],
            reverse_sql=[('DROP SCHEMA IF EXISTS content CASCADE;')],
        ),
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('rating', models.FloatField(blank=True, default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('film_type', models.TextField(choices=[('movie', 'Movie'), ('tv_show', 'TV Show')], verbose_name='film type')),
            ],
            options={
                'verbose_name': 'Film',
                'verbose_name_plural': 'Films',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.TextField(choices=[('director', 'Director'), ('writer', 'Writer'), ('actor', 'actor')], verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person')),
            ],
            options={
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
            ],
            options={
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.person'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work', 'person', 'role'], name='film_work_person_role__idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work', 'genre'], name='film_work_genre_idx'),
        ),
    ]
