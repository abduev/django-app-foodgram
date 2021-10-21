# Foodgram


## Description
Foodgram is a site that allows users publish recipes, subscribe to recipe publications of other users, add their favorite recipes to the list of "Favorites", and before going to the store, download a summary list of ingredients necessary to cook one or more selected dishes.\
Website: https://foodgram.gq/recipes.

## Tech stack
 - Python 3.8+
 - Django framework
 - Django rest framework
 - PostgreSQL
 - Nginx
 - Docker
 - CI/CD (GitHub Actions)

The backend of the project is made on the Django framework, the API to the project is on the Django REST Framework.
The frontend is made on the React framework (this part of project was done by frontend developer).
Implemented containerization of the project using Docker. Docker uses one PostgreSQL and one Nginx and volumes for persisting data.

![foodgram workflow](https://github.com/abduev/django_project_food_gram/actions/workflows/main.yml/badge.svg)


## Scripts

__Unauthorized is allowed to__:
 - Create an account.
 - View recipes on the main page.
 - View individual recipe pages.
 - View user pages.
 - Filter recipes by tags.

__Authorized is allowed to__:
 - Log in to the system using your username and password.
 - Log out.
 - Change your password.
 - Create / edit / delete your own recipes
 - View recipes on the main page.
 - View user pages.
 - View individual recipe pages.
 - Filter recipes by tags.
 - Work with your personal favorites list: add recipes to it or delete them, view your favorites page.
 - Work with a personal shopping list: add / delete any recipes, downpload a file with the amount of required ingredients for recipes from the shopping list.
 - Subscribe to and unsubscribe from recipe authors, view your subscriptions page.


## Setup and Run
Requirements:
 - Python 3.8+
 - Git
 - Docker

Clone repository from GitHub:
```sh
git clone https://github.com/abduev/foodgram-project-react.git
```

In the root directory of the project create a file "__.env__" and copy the environment variables from the file "__prod.env__" there.


Go to the folder "/infra" and start building the project:
```sh
docker-compose up -d
```

Once the build is complete, there are several steps to follow.

Apply migrations.
 ```sh
docker-compose exec -it <BACKEND CONTAINER ID> python manage.py migrate
```

Load statics.
 ```sh
docker-compose exec -it <BACKEND CONTAINER ID> python manage.py collectstatic --no-input
```
Create superuser.
 ```sh
docker-compose exec web python manage.py createsuperuser
```

The project is ready at address 0.0.0.0. API Documentation: http://0.0.0.0/api/docs/redoc.html.


To stop the project run the command:
```sh
docker-compose down
```
