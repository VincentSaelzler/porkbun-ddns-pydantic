from pydantic import BaseModel


class Person(BaseModel):
    fn: str
    ln: str


p = Person(fn="v", ln="s")

file_path = "person.json"
with open(file_path, "w") as file:
    file.write(p.json())
