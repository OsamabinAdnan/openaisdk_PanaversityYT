from typing import Generic, TypeVar
from dataclasses import dataclass

T= TypeVar("Tcontext")

@dataclass
class Person(Generic[T]):
    name: T
    age: T
    id: T

    def welcome(self):
        print(f'Welcome {self.name} you are {self.age} years old and your id is {self.id}')

p1 = Person[str](name='John', age='25', id='123')
p1.welcome()  # Output: Welcome John you are 25 years old and your id is 123
