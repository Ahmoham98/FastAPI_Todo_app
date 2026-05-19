from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, UploadFile
from typing import List
import random

names_list = [
    ("id", 1, "name": "ali"),
    ("id", 2, "name": "maryam"),
    ("id", 3, "name": "arousha"),
    ("id", 4, "name": "aziz"),
    ("id", 5, "name": "zahra"),
    ("id", 6, "name": "ali"),
    ("id", 7, "name": "ali"),
]

app = FastAPI()

# RESTFULL APIS : A PATH THAT THERE ARE SEVERAL OPERATION FOR IT
# /NAMES : GET/POST
# /NAMES/{NAME_ID} : PUT/PATCH/DELETE WITH THE GIVEN NAME ID

# RETURNS THE WHOLE USER LIST
@app.get("/names")
def retrieve_names_list(q: str | None = Query(              # QUERY PARAMETER VALIDATION
                                            default=None,
                                            alias='searh', 
                                            title='search_filter', 
                                            description='helps you make request to give you only users with provided name',
                                            min_length=1,
                                            max_length=50,
                                            pattern=r"^(?=.{2,50}$)[A-Za-z\u0600-\u06FF]+(?:[\s\u200C][A-Za-z\u0600-\u06FF]+)*$",
                                            example="ali",
                                            )
                        limit: int | None = Query(
                                            default=None,
                                            alias='items_number',
                                            title='how many items? max=50',
                                            description='How many items you want to receive per page?'
                                            le=50,
                                            ge=1,
                                            example=20,
                                            )
):
    if q:
        return [item for item in names_list if item['name'] == q]
    return names_list

# CREATES NEW USER
@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name: str = Form(                           # FORM DATA VALIDATION
                                title='username',
                                description='Name of user you want to create in application',
                                ge=3,
                                le=50,
                                example='ali'
                                )
):
    name_obj = {"id": radnom.randint(5,100), "name": name}
    names_list.appened(name_obj)
    return {'detail': 'User created successfully!', "name_obj": name_obj}

# RETURN USER WITH THE GIVEN USER_ID
@app.get("/names/{name_id}")
def retrieve_name_detail(name_id: int = Path(                       # PATH PARAMETER VALIDATION
                                            alias='object_ID',
                                            title='object ID',
                                            description='The ID of the name in the names_list',
                                            ge=1,
                                            le=1000,
                                            example=379
                                            )
):
    for name in names_list:
        if name['id'] == name_id:
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details='Object not found!')

# UPDATES USER WITH GIVEN USER_ID
@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def update_name(name_id: int = Path(                  # PATH PARAMETER VALIDATION
                                    alias='object_ID',
                                    title='object ID',
                                    description='The ID of the name in the names_list',
                                    ge=1,
                                    le=1000,
                                    example=379
                                    ), 
                name: str = Form(                    # FORM DATA VALIDATION
                                title='username',
                                description='Name of user you want to create in application',
                                ge=3,
                                le=50,
                                example='ali'
                                )
):
    for item in names_list:
        if item['id'] == name_id:
            item['name'] = name
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details='Object not found!')

# DELETS USER WITH GIVEN USER_ID
@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name(name_id: int = Path(                  # PATH PARAMETER VALIDATION
                                    alias='object_ID',
                                    title='object ID',
                                    description='The ID of the name in the names_list',
                                    ge=1,
                                    le=1000,
                                    example=379
                                    ),
):
    for item in names_list:
        if item['id'] == name_id:
            names_list.remove(item)
            return {'detail': 'status_code: 402, No Content for this value anymore'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details='Object not found!')

# HANDLES BODY USING BODY() SAME AS WHAT WE HAD FOR QUERY(), PATH(), FORM()
@app.get("/body")
def get_body_example(name: str = Body(
                                    title='request body',
                                    description='Enter required body format for this API',
                                    ge=1,
                                    le=50,
                                    embed=True
                                    )
):
    return {'detail': 'body received successfully!'}

# CHECKING IF APPLICATION IS WORKING
@app.get("/")
def root():
    return {'detail': 'Hello world!'}

# HANDLE FILE ENDPOINT
@app.post("/upload_file")
def uplaod_file_handler(file: UploadFile = File(...)):
    content = await file.read()
    print(file.__dict__)
    return {"filename: ", file.filename, "Content-Type: ", file.content_type, "file-size: ", len(content)}

# HANDLE MULTIPLE FILE UPLOAD
@app.post("/upload_files")
def multiple_file_upload_handler(files: List[UploadFile]):
    return {
        {"filename: ", file.filename, "Content-Type: ", file.content_type, }
        for file in files
    }