from django.http import HttpResponse
from footballscores.models import *
from django.template.loader import get_template
from django.template import Context, Template
class TemplateInput:
    def __init__(self):   
        self.gameDate = "" #String gameDate 
        self.games = [] #List of TemplateGames objects
class TemplateGames:
    def __init__(self):
        self.homeTeam = "" 
        self.awayTeam = "" 
        self.homeTeamGoalsNo = 0
        self.awayTeamGoalsNo = 0
        self.homeTeamGoals = []
        self.awayTeamGoals = []
class TemplateGoal:
    def __init__(self):
        self.scoreTime = "" #String Score Time
        self.scorer = "" #String scorer name

def root(request):
    latestGames = Fixture.objects.order_by('-gameDate').all()[:10]
    gameDates = []
    for i in latestGames:
        if i.gameDate not in gameDates:
            gameDates.append(i.gameDate)
    intList = []
    for i in gameDates:
        listDateGames = []
        for j in latestGames:
            if j.gameDate == i:
                goals = Goal.objects.filter(game=j)
                listDateGames.append( (j,goals) )
        intList.append( (i,listDateGames) )
    finalList = []
    for i in intList:
        templateInputObject = TemplateInput() 
        ( gameDate , gameAndGoals ) = i
        templateInputObject.gameDate = gameDate.strftime("%d-%B-%Y")
        for j in gameAndGoals:
            ( game, goals ) = j
            templateGamesObject = TemplateGames()
            templateGamesObject.homeTeam = game.homeTeam.name
            templateGamesObject.awayTeam = game.awayTeam.name
            for goal in goals:
                if goal.scorer.team.name == templateGamesObject.homeTeam:
                    templateGamesObject.homeTeamGoalsNo += 1
                    templateGoalObject = TemplateGoal()
                    templateGoalObject.scorer = goal.scorer.name
                    templateGoalObject.scoreTime = goal.scoreTime
                    templateGamesObject.homeTeamGoals.append(templateGoalObject )
                else:
                    if goal.scorer.team.name == templateGamesObject.awayTeam:
                        templateGamesObject.awayTeamGoalsNo += 1
                        templateGoalObject = TemplateGoal()
                        templateGoalObject.scorer = goal.scorer.name
                        templateGoalObject.scoreTime = goal.scoreTime
                        templateGamesObject.awayTeamGoals.append(templateGoalObject )
                    else:
                        return HttpResponse(status=500)
            templateInputObject.games.append(templateGamesObject)
        finalList.append(templateInputObject)
    frontPageTemplate = get_template("frontpage.html")
    html = frontPageTemplate.render(Context( {'finalList': finalList} ))
    return HttpResponse(html)
