import random


class UselessCoach:
    def __init__(self) -> None:
        pass

    def present_menu(self):
        return input("\nPress ENTER to find the answer you need right now.")

    def say_something(self, quotes):
        if len(quotes) <= 0:
            return print("\nThere are no quotes for today.")
        print(f"\n{random.choice(quotes)}")
