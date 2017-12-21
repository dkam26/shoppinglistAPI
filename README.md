
# ShoppinglistAPI
[![Build Status](https://travis-ci.org/dkam26/shoppinglistAPI.png)](https://travis-ci.org/dkam26/shoppinglistAPI)
[![Coverage Status](https://coveralls.io/repos/github/dkam26/shoppinglistAPI/badge.svg?branch=develop)](https://coveralls.io/github/dkam26/shoppinglistAPI?branch=develop)
=======
# ShoppingList
Shoppinglist is an app helps users keep track of their purchased goods.Users can add goods bought,update them or even delete them.

## About
A user can have several shoppinglists

A user can delete any of the goods added

A user can view the amount they spent on goods

A user can view all shopped goods

A user is required to include an e-mail address,user name, first name and Surname on creating an account


## Motivation

The need for the continous tracking of one's expenditure on consumables

## Tools
Tools used for development of this API are;
- API development environment: [Postman](https://www.getpostman.com)
- Editor: [Vs code](https://code.visualstudio.com)
- Documentation : [Apiary](https://apiary.io/)
- Database: [Postgresql](https://www.postgresql.org)
- Microframework: [Flask](http://flask.pocoo.org/)
- Programming language: [Python 3.x.x](https://docs.python.org/3/)

## Tests

The tests are to confirm the connection to the database,accounts creation,login session,addition of lists and products

To run the tests,use:

nosetests --with-coverage --cover-package=my_app tests/


## Getting Started

### Prerequisites
1. Install requirements, run 
```sh
     pip install -r requirements.txt
```
2. Database configuration.
   - Download and install postgres from [here](https://www.postgresql.org/download/)
   - Create database in terminal
   ```sh
      psql postgres;
      CREATE DATABASE database_name;
   ```
   - Connect the application to the database by changing the ``` POSTGRES ``` variable in shopping_list/app/__init__.py.
   ```
      POSTGRES = {
            'user': 'database user',
            'pw': 'user password',
            'db': 'database name',
            'host': 'localhost',
            'port': '5432',
            }
   ```
3. To create database tables, from the project's repository run 
```sh 
    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade
    $ python run.py runserver
 ```

## End points
### Endpoints to create a user account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /auth/register/ | True | Create an account
POST | /auth/login/ | True | Login a user
POST | /auth/logout/ | False | Logout a user
POST | /auth/RestPassword/ | False | Reset a user password

### Endpoints to create, update, view and delete a shopping list
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /shoppinglists/ | False | Create a shopping list
GET | /shoppinglists/ | False | View all shopping lists
GET | /shoppinglist/<list_id> | False | View details of a shopping list
PUT | /shoppinglists/<list_id> | False | Updates a shopping list with a given id
DELETE | /shoppinglists/<list_id> | False | Deletes a shopping list with a given id

### Endpoints to create, update, view and delete a shopping list item
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /shoppinglists/<list_id>/items/ | False | Add an Item to a shopping list
PUT | /shoppinglists/<list_id>/items/<item_id> | False | Update a shopping list item on a given list
GET | /shoppinglists/<list_id>/items/ | False | View items in a particular shopping list
DELETE | /shoppinglists/<list_id>/items/<item_id> | False | Delete an item from a given shopping list



## Contributors

https//github.com/dkam26



