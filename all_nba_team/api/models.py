# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField, DateRangeField

class Teams(models.Model):
    teamid = models.IntegerField(db_column='TeamID', primary_key=True)  # Field name made lowercase.
    aliases = ArrayField(base_field=models.IntegerField(),db_column='Aliases')  # Field name made lowercase. This field type is a guess.
    class Meta:
        managed = False
        db_table = 'teams'

class TeamAlias(models.Model):
    aliasid = models.IntegerField(db_column='AliasID', primary_key=True)  # Field name made lowercase.
    period = DateRangeField(db_column='Period')  # Field name made lowercase. This field type is a guess.
    aliasname = models.CharField(max_length=200,db_column='AliasName')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'team_alias'

class AllNbaTeamsList(models.Model):
    year = models.DateField(primary_key=True)
    playerid = models.IntegerField(db_column='PlayerID')  # Field name made lowercase.
    type = models.IntegerField()
    teamid = models.ForeignKey('TeamAlias', on_delete=models.CASCADE, db_column='TeamID')  # Field name made lowercase.
    role = models.CharField(max_length=1, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'all-nba-teams_list'
        unique_together = (('year', 'playerid'),)


class Seasons(models.Model):
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100,primary_key=True)
    abbreviation = models.CharField(max_length=10,blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'seasons'



