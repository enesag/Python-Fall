from FallBeanFactory import FallBeanFactory


def main():
    context = FallBeanFactory("src", "configuration.json")
    myCoach = context.getBean("myBaseballCoach")
    print(myCoach.getDailyWorkout())
    print(myCoach.getDailyFortune())
    print(myCoach.getEmailAddress())
    print(myCoach.getTeam())


main()
