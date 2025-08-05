from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

    def welcome(self):
        print(f'Welcome {self.name} you are {self.age} years old')

p1 = Person(name='John', age=25 )
p1.welcome()