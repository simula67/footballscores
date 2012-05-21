from django.http import HttpResponse
from footballscores.models import *
from django.template.loader import get_template
from django.template import Context, Template
class TemplateInput:
    gameDate = "" #String gameDate 
    games = [] #List of TemplateGames objects
class TemplateGames:
    homeTeam = "" #String homeTeam Name
    awayTeam = "" #String awayTeam Name
    homeTeamGoalsNo = 0 #int homeTeamGoalsNo
    awayTeamGoalsNo = 0 #int awayTeamGoalsNo
    homeTeamGoals = [] #List TemplateGoal objects
    awayTeamGoals = [] #List TemplateGoal objects
class TemplateGoal:
    scoreTime = "" #String Score Time
    scorer = "" #String scorer name

def hello(request):
    return HttpResponse("Hello world");
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
                if goal.scorer.team == templateGamesObject.homeTeam:
                    templateGamesObject.homeTeamGoalsNo += 1
                    templateGoalObject = TemplateGoal()
                    templateGoalObject.scorer = goal.scorer.name
                    templateGoalObject.scoreTime = goal.scoreTime
                    templateGamesObject.homeTeamGoals.append(templateGoalObject )
                else:
                    templateGamesObject.awayTeamGoalsNo += 1
                    templateGoalObject = TemplateGoal()
                    templateGoalObject.scorer =goal.scorer.name
                    templateGoalObject.scoreTime = goal.scoreTime
                    templateGamesObject.awayTeamGoals.append(templateGoalObject )
            templateInputObject.games.append(templateGamesObject)
        finalList.append(templateInputObject)
    frontPageTemplate = get_template("frontpage.html")
    html = frontPageTemplate.render(Context( {'finalList': finalList} ))
    return HttpResponse(html)
