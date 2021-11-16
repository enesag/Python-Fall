class BaseballCoach():
    def getDailyWorkout(self):
        return "Baseball"

    def getDailyFortune(self):
        return self.fortuneService.getFortune()

    def setFortuneService(self, fortuneService):
        self.fortuneService = fortuneService

    def getEmailAddress(self):
        return self.emailAddress

    def setEmailAddress(self, emailAddress):
        self.emailAddress = emailAddress

    def getTeam(self):
        return self.team

    def setTeam(self, team):
        self.team = team
