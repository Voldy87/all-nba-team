# Generated by Django 2.0.5 on 2018-08-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllNbaTeamsList',
            fields=[
                ('year', models.DateField(primary_key=True, serialize=False)),
                ('playerid', models.IntegerField(db_column='PlayerID')),
                ('type', models.IntegerField()),
                ('role', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'all-nba-teams_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('abbreviation', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'seasons',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TeamAlias',
            fields=[
                ('aliasid', models.IntegerField(db_column='AliasID', primary_key=True, serialize=False)),
                ('period', models.TextField(db_column='Period')),
                ('aliasname', models.CharField(db_column='AliasName', max_length=200)),
            ],
            options={
                'db_table': 'team_alias',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('teamid', models.IntegerField(db_column='TeamID', primary_key=True, serialize=False)),
                ('aliases', models.TextField(blank=True, db_column='Aliases', null=True)),
            ],
            options={
                'db_table': 'teams',
                'managed': False,
            },
        ),
    ]
