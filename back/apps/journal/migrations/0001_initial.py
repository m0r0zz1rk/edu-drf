# Generated by Django 4.2.7 on 2024-04-23 02:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID объекта')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('source', models.CharField(blank=True, default='', max_length=500, verbose_name='Источник события')),
                ('status', models.CharField(choices=[('NO_RESULT', 'Без результата'), ('SUCCESS', 'Успешно'), ('ERROR', 'Ошибка'), ('WARNING', 'Предупреждение')], default='NO_RESULT', max_length=15, verbose_name='Статус события')),
                ('description', models.TextField(blank=True, default='', max_length=2000, verbose_name='Краткое описание результата события')),
            ],
            options={
                'verbose_name': 'Запись журнала событий',
                'verbose_name_plural': 'Записи журнала событий',
            },
        ),
        migrations.CreateModel(
            name='JournalPayload',
            fields=[
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID объекта')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('payload', models.TextField(blank=True, default=None, max_length=100000, null=True, verbose_name='Полезная нагрузка')),
                ('journal_rec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.journal', verbose_name='Запись журнала событий')),
            ],
            options={
                'verbose_name': 'Полезная нагрузка к записи журнала событий',
                'verbose_name_plural': 'Полезные нагрузки к записям журнала событий',
            },
        ),
        migrations.CreateModel(
            name='JournalOutput',
            fields=[
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID объекта')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('output', models.TextField(blank=True, default=None, max_length=100000, null=True, verbose_name='Результат/Выходные данные')),
                ('journal_rec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.journal', verbose_name='Запись журнала событий')),
            ],
            options={
                'verbose_name': 'Результат/Выходные данные к записи журнала событий',
                'verbose_name_plural': 'Результаты/Выходные данные к записям журнала событий',
            },
        ),
    ]
