from magic_ball_webscraper import Controller
from useless_coach import UselessCoach


def main():
    magic_ball_webscraper = Controller()
    coach = UselessCoach()

    quotes = magic_ball_webscraper.exec_scrapping(magic_ball_webscraper)

    while True:
        coach.present_menu()
        coach.say_something(quotes)


if __name__ == "__main__":
    print("Welcome to the Useless Coach's Magic '8 Ball' Webscraper!")
    main()
