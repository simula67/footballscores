from django.db import models
# Users of the site

#Currently only admin
class User(models.Model):
    name = models.CharField(max_length=50)

# Site Data
class Player(models.Model):
    name = models.CharField(max_length=50)
    jerseyNo = models.IntegerField(max_length=30)
class Team(models.Model):
    name = models.CharField(max_length=50)
    players = []
class Competition(models.Model):
    name = models.CharField(max_length=50)
    teams = []
class Goal(models.Model):
    scorer = models.ForeignKey(Player)
    time = models.CharField(max_length=30)
class Fixture:
    homeTeam = models.ForeignKey(Team)
    awayTeam = models.ForeignKey(Team)
    homeTeamGoals = []
    awayTeamGoals = []
    date = models.DateField
    league = models.ForeignKey(Competition)

