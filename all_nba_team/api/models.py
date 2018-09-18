# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField, DateRangeField
from django.conf import settings

import redis, requests, time

################## postgresql importdb from existing ################

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

################## stats.nba.com - redis db ################
def load__player_data(id:str):
    url = 'https://stats.nba.com/stats/commonplayerinfo/?PlayerID='+id
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = response.json()['resultSets'][0]['rowSet'][0]
    name,surname = data[1:3]
    dob = data[6]
    country,role = data[8], data[14]
    d_y, d_r, d_n = data[26:29]
    info = { 
        "name":name,
        "surname":surname, 
        "country":country, 
        "role":role, 
        "draft":{
            "year":d_y,
            "round":d_r,
            "number":d_n
        }
    }
    return(info)
    
class NBA_stats:
    """The abstraction of data taken from stats.nba.com and, sometimes, saved on Redis"""
    def __init__(self, *args, **kwargs):
        self.redis = redis.StrictRedis(decode_responses=True,
            host = settings.DATABASES['redis']['HOST'],
            port = settings.DATABASES['redis']['PORT'], 
            password = settings.DATABASES['redis']['PASSWORD']
        )
        self.update = (self.redis.dbsize()!=0)
    def redisFlush(self):
        self.redis.flushdb()
        self.update = False
    def get_Single_PlayerInfo(self,player_id):
        return self.redis.hgetall("user:"+str(player_id))
    def set_Single_PlayerInfo(self,player_id,info):
        for key in info:
            self.redis.hset(key,"user:"+str(player_id),info[key])
    def set_All_PlayerInfo(self):
        pipe = self.redis.pipeline(transaction=False)
        data = list( AllNbaTeamsList.objects.using('data').all().values_list('playerid','teamid_id') )
        for spam in set(tuple(row) for row in data): #delete player_id/team_id duplicates
            player_id, team_id = spam
            player_id, team_id = str(player_id), str(team_id)
            info = load__player_data(player_id)
            pipe.hmset( "user:"+player_id , info )
            time.sleep(1)
        pipe.execute()
        self.update = True
    def isUpToDate(self):
        return self.update