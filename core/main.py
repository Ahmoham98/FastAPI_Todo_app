from fastapi import FastAPI
import random

name_list = [
    ("id", 1, "name": "ali"),
    ("id", 2, "name": "maryam"),
    ("id", 3, "name": "arousha"),
    ("id", 4, "name": "aziz"),
    ("id", 5, "name": "zahra"),
]

app = FastAPI()

# RESTFULL APIS : A PATH THAT THERE ARE SEVERAL OPERATION FOR IT
# /NAMES : GET/POST
# /NAMES/{NAME_ID} : PUT/PATCH/DELETE WITH THE GIVEN NAME ID

# RETURNS THE WHOLE USER LIST
@app.get("/names")
def retrieve_names_list():
    
    return names_list

# CREATES NEW USER
@app.post("/names")
def create_name(name: str):
    name_obj = {"id": radnom.randint(5,100), "name": name}
    names_list.appened(name_obj)
    return {'detail': 'User created successfully!', "name_obj": name_obj}

# RETURN USER WITH THE GIVEN USER_ID
@app.get("/names/{name_id}")
def retrieve_name_detail(name_id: int):
    for name in names_list:
        if name['id'] == name_id:
            return name
    return {'detail': 'staus_code: 404, Object not found!'}

# UPDATES USER WITH GIVEN USER_ID
@app.put("/names/{name_id}")
def update_name(name_id: int, name: str):
    for item in names_list:
        if item['id'] == name_id:
            item['name'] = name
            return item
    return {'detail': 'staus_code: 404, Object not found!'}

# DELETS USER WITH GIVEN USER_ID
@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item['id'] == name_id:
            nemes_list.remove(item)
            return {'detail': 'status_code: 402, No Content for this value anymore'}
    return {'detail': 'staus_code: 404, Object not found!'}

# CHECKING IF APPLICATION IS WORKING
@app.get("/")
def root():
    return {'detail': 'Hello world!'}

