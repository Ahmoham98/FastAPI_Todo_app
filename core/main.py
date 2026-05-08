from fastapi import FastAPI

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

# RETURN USER WITH THE GIVEN USER_ID
@app.get("/names/{name_id}")
def retrieve_name_detail(name_id: int):
    for name in names_list:
        if name['id'] == name_id:
            return name
    return {'detail': 'staus_code: 404, Object not found!'}

# CHECKING IF APPLICATION IS WORKING
@app.get("/")
def root():
    return {'detail': 'Hello world!'}

