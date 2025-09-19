from pydantic import BaseModel
# from pydantic.dataclasses import dataclass
from dataclasses import dataclass

class User(BaseModel):
    name:str
    age:int

user = User(name="John", age=20)
print(user)
print("Name", user.name)
print("Age: ", user.age)
print("Json: ",user.model_dump_json())
print(f"Dictionary: {user.model_dump()}\n")
print(f"Schema: {user.model_json_schema()}")



@dataclass
class User2():
    name:str
    age:int

user2 = User2(name="Osama", age=25)
print(user2)
print("Name", user2.name)
print("Age: ", user2.age)

