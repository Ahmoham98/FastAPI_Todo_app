from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator

class BasePersonSchema(BaseModel):
    name: str # = Field(..., max_length=50)

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

# ROOT VALIDTOR EXAMPLE
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