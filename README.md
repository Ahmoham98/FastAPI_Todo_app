# About Application
## A clean template for start Developing FastAPI app
- You can simply clone the project, run the Application and start developing your fastapi app using this template which also is easy to scale as your app goes to scale to become bigger as your files and folders grows. this template helps you to focus more on developement rather than taking time on arranging standard template for developing fastapi apps
- if your project is going to grow bigger and you need bigger standard template, checkout this link: https://github.com/fastapi/full-stack-fastapi-template

## user authentication
### JWT Token Authentication
- this application is using JWT for authentication
- /Login route for users login:
1. checks if user exists and if it is a valid user, it is going to return access_token & Refresh_token
- /Register rotue for users Registration
1. if user dosn't exists, make sure user is entering valid data and inserts new user into database

## RBAC for Authorization control
### We have USER & ADMIN roles implemented
- you can Simply go to core/users/models.py where RoleChecker class exists, and add more roles for validation
- then navigate to core/core/dependencies.py where RoleChecker exists and adjust the checking logic if any more consideration needed
- finally you can use role checker cleanly as dependency in your routes same as "/api/v1/users/check-role" route we already implemented... (allowed roles argument tells the checker which roles can have access to this routes...)

# How to run the Application
## Run the whole Application with docker-compose 🐳
- 1. navigate to root directory
- 2. simply Run "docker compose up --build -d"
    if you want your docker to work in your terminal background, run:
        "docker compose --build -d"
    if you want your docker to not be detached, simply run:
        "docker compose --build"
    ! you need to use --build flag for the first time. then you can simply run "docker compose" to run the whole application for you 
    ! docker compose will creates "postgres_data" volume in your docker. make sure you will use -v flag for "docker compose down" when you want to permanently bring down the application

## Run FastAPI seperately 🐍
- 1. navigate to core directory of the current cloned project with "cd core"
- 2. simply run "fastapi dev" 
- 3. you have developement mode on working
- 4. for routes that have database interaction, you have these following options:
    - (Docker Image 🏍) run a postgreSQL image using docker manually by pulling ralated image and running it
    - (Docker Compose 🚗) run a postgreSQL image using docker-compose.yml file with the following content:
        services:
            db:
                image: postgres:15-alpine
                container_name: postgres_todo_container
                restart: always
                environment:
                POSTGRES_USER: user
                POSTGRES_PASSWORD: password
                POSTGRES_DB: TodoappTemplateTypeA
                ports:
                - "5432:5432"
                volumes:
                - postgres_data:/var/lib/postgresql/data

            volumes:
            postgres_data: 
    - (Local PostgreSQL 🚲) download postgreSQL app and run it localy and setup a database with the following configurations:
        POSTGRES_USERNAME -> user
        POSTGRES_PASSWORD -> password
        POSTGRES_DATABASE_NAME -> TodoappTemplateTypeA
        port -> 5432 (or any other desired port base on what you are working on...)

## Run Database seperately 🐘
Database is default to PostgreSQL...
in .env file with value SQLALCHEMY_DATABASE_URL. (Check out .env.example file for this)... 
for changing database connection, you can change the SQLALCHEMY_DATABASE_URL value in you .env file. (make sure you will refactor database.py file if your database is not supporting async connection)
- 1. (Docker Image 🏍) run a postgreSQL image using docker manually by pulling ralated image and running it..
- 2. (Docker Compose 🚗) run a postgreSQL image using docker-compose.yml file with the following content:
    services:
        db:
            image: postgres:15-alpine
            container_name: postgres_todo_container
            restart: always
            environment:
            POSTGRES_USER: user
            POSTGRES_PASSWORD: password
            POSTGRES_DB: TodoappTemplateTypeA
            ports:
            - "5432:5432"
            volumes:
            - postgres_data:/var/lib/postgresql/data

        volumes:
            postgres_data: 
- 3. (Local PostgreSQL 🚲) download postgreSQL app and run it localy and setup a database with the following configurations:
    POSTGRES_USERNAME -> user
    POSTGRES_PASSWORD -> password
    POSTGRES_DATABASE_NAME -> TodoappTemplateTypeA
    port -> 5432 (or any other desired port base on what you are working on...)

# About Appliation
## Technologies and Libraries ⚙
- FastAPI python Framework for fast async backend developement
- SQLAlchemy ORM for code first database connection
- Alembic for Database migration management
- asyncpg configuration for async conncetion to default database (e.g PostgrSQL)
- pydantic-settings for single source of configuration in the whole project
- Dependnecy Injection database connection for
- pwdlib for password hashing using 
- PyJWT
## Endpoints
- GET /api/v1/todo/tasks
    returns all found tasks from database + Pagination
- GET /api/v1/todo/tasks/{task_id}
    returns founded tasks from database with given task_id
- POST /api/v1/todo/tasks
    inserts new tasks to database
- PUT /api/v1/todo/tasks/{task_id}
    updates task's data for the found task in database with given task_id
- DELETE /api/v1/todo/tasks/{task_id}
    removes task from database by the found task in database with given task_id
- GET /users/login
    Logs the user in: 
    1. checks if user exists
    2. checks if user's password is valid
    3. if okey, Generate access_token
- GET /users/register
    Registers User
    1. check if user already exists
    2. inserts user for login
- for full documentation check /doc or /redoc like: "http://127.0.0.1:8000/docs" or "http://127.0.0.1:8000/redoc" for redoc (Verbose version of /docs)
## Better to know about Project and Application 
### in rotues.py, flush is used and it will be commited automatically using dependency injection where you define "get db"
### Tables id are defiend as integer type... . You can upgrade to UUID anytime you prefered
### Hash password and verify password helper function are in UserModel class as a method. You can move them to util or share directory on project scalling or keep them in UserModel
### Refresh Token Rotation is implemented (but tokens are not being stored in database yet for proper refresh token validation before token rotation - it may be updated to have it, make sure you implement it in production for your application if it is not already implemented for this template)
### default settings for token expiration are: ACCESS_TOKEN_EXPIRE_MINUTES = 15,  REFRESH_TOKEN_EXPIRE_DAYS = 7 & ALGORITHM = "HS256". You can adjust them base on your usecase in "core/core/security.py" file 
### JWT sub is checking user_id insted of email due to technical standards. You can change it to consider email in "sub" of JWT Payload if you prefer. Considering it's Cons and Prons
- for changing it, go for the following parts of the code:
1. go to where we have defiend /login endpoint
2. find token_data value, and change it form {"sub": str(user_id)} to {"sub": user.email}
3. now, login endpoint is considering email in JWT sub payload
4. You need to also make /refresh-token endpoint to also consider email for generating new access and refresh token. for doing that, simply:
5. got to where we have defined /refresh-token endpoint
6. find user_id_str value and change it from {"sub": str(user_id)} to {"sub": user.email} 
7. then change the if condition after it from "if not user_id_str:" to "if not email"
8. and finally change token_data value from {"sub": str(user_id)} to {"sub": user.email}
9. you also by implementing these changes, don't need to check if user still exists, so you can remove that part of code or you can change it to check if user still exists by checking if email is still exists. (that can be modified base on your usecase)
10. and done, now your JWT is considering email instead of user id for sub in your payload
### JWT cookie Authentication is also implemented you can check it in /login-cookie endpoint and related dependencies in core/security.py file path, where security related functions are gathered
