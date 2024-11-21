# SPA-application: COMMENTS

This project is a Single Page Application (SPA) for managing and displaying user comments. 
It provides a modern interface where users can leave comments, reply to other comments, 
and view them in a paginated list. The backend is built using Django and SQLite/PostgreSQL as a database, 
while the frontend is designed with HTML and CSS.

## Check it out!

[spa-comments deploved to Render](https://spa-comments-lij6.onrender.com)


## Technology stack

* Backend:
  - Language: Python 3 
  - Framework: Django 
  - Database: SQLite (Postgresql)
  - ORM: Django ORM
* Frontend: HTML/CSS
* Dependency Management: pip
* Virtual Environment: venv
* Collaboration and Version Control:
  - Version Control System: Git
  - Repository Hosting: GitHub
* Database Migrations: Django Migrations
* Environment Variables: .env
* Testing: Unittest
* Containerization: Docker
* Other: 
  - requirements.txt
  - .env for environment variables

## Installation

Python3 must be already installed

```shell
# Local setup
# Clone the repository:
git clone https://github.com/oleg-potichnyi/spa-comments
# Change directory to the project folder:
cd spa_comments
# Set up a virtual environment:
python3 -m venv venv
# Activate the virtual environment on Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
# Install dependencies:
pip install -r requirements.txt
# Environment variables:
## To use the .env and .env.sample files, simply duplicate the .env.sample file and rename it as .env.
## Fill in the variables in the .env file with your actual configuration values, 
## keeping sensitive information private, while the .env.sample file acts as a reference
## for other developers to understand the required environment variables.
# Run this command to apply migrations and update the database schema:
python manage.py migrate
# Start the development server:
python manage.py runserver
```

```shell
# Start the Application via Docker
# Clone the repository:
git https://github.com/oleg-potichnyi/spa-comments
# Change directory to the project folder:
cd spa_comments
# Setup via Docker
# Build the Docker Containers:
docker-compose build
# Start the Docker Containers:
docker-compose up
# Stopping the Docker Containers:
# To stop the Docker containers, use the following command:
docker-compose down
```

## Features

* Comment form with required fields: "User Name", "E-mail", and "Text", and optional "Home Page" field
* CAPTCHA for spam protection
* Sorting of comments by username, e-mail, and date of submission (LIFO)
* Pagination of comments with 25 records per page
* Support for cascading comments (replies to comments)
* Validation of input data on both server and client side
* Docker Support

## Admin credentials

```shell
Username: Oleh
password: admin12345
```
