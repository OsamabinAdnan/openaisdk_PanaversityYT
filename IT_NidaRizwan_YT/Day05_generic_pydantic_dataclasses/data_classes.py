# Simple Class

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def welcome(self):
        print(f'Welcome {self.name} you are {self.age} years old')

p1 = Person('John', 25 )
p1.welcome()

# Dataclasses

from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

    def welcome(self):
        print(f'Welcome {self.name} you are {self.age} years old')

p1 = Person('John', 25 )
p1.welcome()