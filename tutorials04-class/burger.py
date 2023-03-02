class KrabbyPatty:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def order(self):
        print(self.ingredients)

class Spongebob:
    def oneKrabbyCheese(self):
        ingredients = ["bun", "cheese", "beef-patty"]
        return KrabbyPatty(ingredients)

KrustyKrab = Spongebob()
KrustyKrab.oneKrabbyCheese().order()