from django.db import models
# Users of the site

#Currently only admin
class User(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
# Site Data
class Competition(models.Model):
    name = models.CharField(max_length=50)
class Team(models.Model):
    name = models.CharField(max_length=50)
    competitions = models.ManyToManyField(Competition)
class Player(models.Model):
    name = models.CharField(max_length=50)
    jerseyNo = models.IntegerField(max_length=30)
    team = models.ForeignKey(Team)
class Fixture(models.Model):
    homeTeam = models.ForeignKey(Team)
    awayTeam = models.ForeignKey(Team,related_name='+')
    date = models.DateField()
    competition = models.ForeignKey(Competition)
class Goal(models.Model):
    scorer = models.ForeignKey(Player)
    scoreTime = models.CharField(max_length=30)
    game = models.ForeignKey(Fixture)
