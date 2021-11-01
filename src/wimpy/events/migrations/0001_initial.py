# Generated by Django 3.2.8 on 2021-11-01 21:20

from django.db import migrations, models
import django.db.models.deletion
import wimpy.events.constants


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of category used to generate a unique slug', max_length=64, unique=True, verbose_name='Category name')),
                ('description', models.TextField(blank=True, help_text='Brief description about category', max_length=256, null=True, verbose_name='Category description')),
                ('slug', models.SlugField(editable=False, help_text='Identifier used to interact with API', max_length=64, verbose_name='Category slug')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of type used to generate a unique slug', max_length=64, unique=True, verbose_name='Type name')),
                ('description', models.TextField(blank=True, help_text='Brief description about type', max_length=256, null=True, verbose_name='Type description')),
                ('slug', models.SlugField(editable=False, help_text='Identifier used to interact with API', max_length=64, verbose_name='Type slug')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField(db_index=True)),
                ('data', models.JSONField(help_text='Event data sent from client', verbose_name='Event data')),
                ('timestamp', models.DateTimeField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventcategory')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventtype')),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.CreateModel(
            name='EventSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_schema', models.JSONField(blank=True, default=wimpy.events.constants.get_default_event_data_schema, help_text='Custom json schema to validate event data', null=True, verbose_name='Event data schema')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventcategory')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventtype')),
            ],
            options={
                'unique_together': {('category', 'type')},
            },
        ),
    ]
