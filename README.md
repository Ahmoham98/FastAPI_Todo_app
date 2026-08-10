# About Application
## A clean template for start Developing FastAPI app
- You can simply clone the project, run the Application and start developing your fastapi app using this template which also is easy to scale as your app goes to scale to become bigger as your files and folders grows. this template helps you to focus more on developement rather than taking time on arranging standard template for developing fastapi apps
- if your project is going to grow bigger and you need bigger standard template, checkout this link: https://github.com/fastapi/full-stack-fastapi-template

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
## Technologies
- FastAPI python Framework for fast async backend developement
- SQLAlchemy ORM for code first database connection
- Alembic for Database migration management
- asyncpg configuration for async conncetion to default database (e.g PostgrSQL)
- pydantic-settings for single source of configuration in the whole project
- Dependnecy Injection database connection for
## Better to know about Project and Application
- in rotues.py, flush is used and it will be commited automatically using dependency injection where you define "get db"

