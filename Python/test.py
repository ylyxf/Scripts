class Fish:
    def eat(self,food):
        if food is not None:
            self.hungry = False
        else: self.hungry = True

f = Fish()
eatFood = input('give a food: ')
print eatFood
f.eat(eatFood)
print f.hungry
