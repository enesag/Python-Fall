class CricketCoach():
    def __init__(self, fortuneService):
        self.fortuneService = fortuneService

    def getDailyWorkout(self):
        print("Cricket")

    def getDailyFortune(self):
        print(self.fortuneService.getFortune())
