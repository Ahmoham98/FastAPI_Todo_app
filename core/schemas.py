from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator, filed_serializer, model_serializer

class BasePersonSchema(BaseModel):
    name: str = Field(..., description="Enter person's name")

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError("Name must not exceed 32 characters")
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value
    @filed_serializer("name")
    def serialize_name(value):
        return value.title() # ali to Ali
    

class PersonCreateSchema(BasePersonSchema):
    pass

class PersonResponseSchema(BasePersonSchema):
    id: int = Field(..., description="Unique user identifier")

class PersonUpdateSchema(BasePersonSchema):
    pass

# ---- FOR DOCUMENTATION USING MODEL_JSON_SCHEMA ----
class Example(BaseModel):
    name: str = Field(default="John Doe", description="The user's name", example="Nutrialgo", min_length=3, max_length=25)
    #name : str = Field(..., default="John Doe") # ... FOR WHEN YOU WANT TO MAKE A FIELD REQUIRED
print(Example.model_json_schema())
# INCLUDES METADATA IN THE SCHEMA
{
    "title": "Example",
    "properties": {
        "name": {
            "title": "Name",
            "default": "John Doe",
            "description": "the user's name",
            "examples": ["Alice"]
        }
    }
}

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

# FIELD SERIALIZER EXAMPLE
class FieldSerialized(BaseModel):
    number: float

    # IF WE HAVE 1/3 FOR NUMBER, THAT CAN BE 0.333333333333333333 AND WE NEED TO ROUND THAT NUMBER
    @filed_serializer("number")
    def serialize_float(self, value):
        return round(value, 2)

# MODEL SERIALIZER EXAMPLE
class ModelSerialized(BaseModel):
    id: int
    name: str
    is_active: bool

    @model_serializer
    def custom_serializer(self) -> dict:
        return {
            "user_id": self.id,
            "full_name": self.name.upper(),
            "status": "active" if self.is_active else "inactive",
        }




# ---- MODEL_VALIDATE() FUNCTION ----
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


# ---- MODEL_VALIDATE_JSON() FUNCTION ----
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
# --------------------------------------

# ---- SERIALIZATION AND DESERIALIZATION ----
# -> 1. model_dump()
# -> 2. model_dump_json()
#
#from pydantic import BaseModel, EmailStr
#
#class User(BaseModel):
#    name: str
#    email: EmailStr
#    account_id: int
#
#user = User(name="Ahmoham", email="electricallover45@gmail.com", account_id="123")
#
#user.model_dump()
## OUTPUT -> {name='Ahmoham', email='electricallover45@gmail.com', account_id='123'}
#
#user.model_dump_json()
## OUTPUT -> "{name='Ahmoham', email='electricallover45@gmail.com', account_id='123'}"
#
#user.model_dump_json(indent=2)
#''' OUTPUT ->  "
#{
#  name='Ahmoham', 
#  email='electricallover45@gmail.com', 
#  account_id='123'
#}"
#'''


