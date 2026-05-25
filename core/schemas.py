from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator

class BasePersonSchema(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError("Name must not exceed 32 characters")
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value
    

class PersonCreateSchema(BasePersonSchema):
    pass

class PersonResponseSchema(BasePersonSchema):
    id: int

class PersonUpdateSchema(BasePersonSchema):
    pass

# MODEL VALIDTOR EXAMPLE
class Boost(BaseModel):
    start: int 
    end: int

    @model_validator(mode='after') # mode='after' for post-initialization validation
    def check_range(self): # 'self' is passed in 'after' mode
        if self.start >= self.end:
            raise ValueError("start must be less than end!")
        return self

# CUSTOM VALIDATOR EXAMPLE
class User(BaseModel):
    email: EmailStr


# ---- MODEL_VALIDATE FUNCTION ----
# from pydantic import BaseModel

#class Person(BaseModel):
#    first_name: str
#    last_name: str
#    age: int
#
## WHAT IS GOING TO BE CREATED IS
#data = {
#   "first_name": "ali",
#   "last_name": "big",
#   "age": 30
#}
#P = Person.model_validate(data)
# --------------------------------------


# ---- MODEL_VALIDATE_JSON FUNCTION ----
# USEFULL FOR PARSING STRINGS WHICH ARE IN JSON FORMAT
# from pydantic import BaseModel

#class Person(BaseModel):
#    first_name: str
#    last_name: str
#    age: int
#
#data_json = '''
#{
#   "first_name": "ali",
#   "last_name": "big",
#   "age": 30
#}
#'''
#person = Person.model_validate_json(data_json)
#
#
#