# FSND-Capstone
For all books' lovers out there this API helps you track your favourite books with all of their details.

The API has the following types of users:

- Admin: Has all permissions granted.
- Library-Manager: Can add and update books.
- Authorized User: Has his/her own library of books that no one else can view.
- Unauthorized User: Can only view the listed books in the API.


## [Heruku API URL](https://khaledose-fsnd-capstone.herokuapp.com/) 


## Installing Dependencies for Local Development

1. **Python 3.9** - Install latest version of [Python](https://www.python.org/downloads/) from the official website.

2. **Virtual Enviornment** 
    - Install Virtual Environment by running:
        ```bash
        pip install virtualenv
        ```
    - Create a Virtual Environment in project's root directory by running:
        ```bash
        python -m venv venv
        ```
    - Activate the Virtual Environment from the CMD from root directory by running:
        ```bash
        venv\Scripts\activate
        ```

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies while in root directory by running:
    ```bash
    pip install -r requirements.txt
    ```
    This will install all of the required packages we selected within the `requirements.txt` file.

4. **Environment Variables** - Create **.env** file in the root directory with the following variables:
    ```
    FLASK_APP=app
    FLASK_ENV=development
    AUTH0_CLIENT_ID=YOUR_AUTH0_CLIENT_ID
    AUTH0_DOMAIN=https://YOUR_AUTH0_DOMAIN_URL
    AUTH0_CLIENT_SECRET=YOUR_AUTH0_CLIENT_SECRET
    AUTH0_CALLBACK_URL=YOUR_AUTH0_CALLBACK_URL
    AUTH0_LOGOUT_REDIRECT=YOUR_AUTH0_LOGOUT_URL
    AUTH0_AUDIENCE=YOUR_AUTH0_API_AUDIENCE
    DB_HOST=YOUR_DB_HOST_URL
    POSTGRES_USER=YOUR_POSTGRES_USER
    POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
    POSTGRES_DB_DEV=YOUR_DEV_DB_NAME
    POSTGRES_DB_TEST=YOUR_TEST_DB_NAME
    ```

5. **Setup Database**
    - Create both dev and test databases you defined in your **.env** file from **psql**:
        ```bash
        CREATE DATABASE YOUR_DEV_DB_NAME;
        CREATE DATABASE YOUR_TEST_DB_NAME;
        ```
    - Run the following command from root directory to migrate the database
        ```bash
        flask db upgrade
        ```

6.  **API Unit Tests** - Run the following command in the root directory to run all API unit tests:
    ```bash
    python -m unittest discover ./app/test
    ```

6. **Run Server** - Run the following command in the root directory:
    ```bash
    flask run
    ```

## API Endpoints
These are the endpoints of the API with the expected request and response bodies:

### **Users Endpoint**

#### Auth0 Login (Public)
```
GET '/users/login'
- Redirects to Auth0 login page.
- Request Arguments: None.
- Returns: None.
```

#### Auth0 Callback 
```
GET '/users/profile'
- Signs in/up the user from user details retrieved by Auth0 login.
- Request Arguments: None.
- Returns: User's details, permissions and access token.
{
    'success': True,
    'profile': {
        'id': '',
        'firstName': '',
        'lastName': '',
        'email': ''
    },
    'permissions': ['post:books', 'update:books'],
    'access_token': {ACCESS_TOKEN}
}
```


#### Auth0 Logout **Requires Normal Authorization**
```
GET '/users/logout'
- Signs out the currently logged in and redirects back to home.
- Request Arguments: None.
- Returns: None
```



#### Get Registered Users **Requires Admin Role**
```
GET '/users'
- Gets all registered users in the system and requires authentication and view:users permission.
- Request Arguments: 
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns an array of users.
{
    'success': True,
    'users': [{
            'id': '',
            'firstName': '',
            'lastName': '',
            'email': ''
        },
        {
            'id': '',
            'firstName': '',
            'lastName': '',
            'email': '
        }]
}
```

#### Get Current User Details **Requires Normal Authorization**
```
GET '/users/my_details'
- Gets the currently logged in user's details.
- Request Arguments: 
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns the current user.
{
    'success': True,
    'user': {
            'id': '',
            'firstName': '',
            'lastName': '',
            'email': ''
        }
}
```

#### Update Current User Details **Requires Normal Authorization**
```
PATCH '/users'
- Updatse the currently logged in user's details.
- Request Arguments: 
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns the current user.
{
    'success': True,
    'user': {
            'id': '',
            'firstName': '',
            'lastName': '',
            'email': ''
        }
}
```

#### Delete Current User **Requires Normal Authorization**
```
DELETE '/users'
- Deletes the currently logged in user and logs out from Auth0.
- Request Arguments: 
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns: None
```

### **Books Endpoint**

#### Get Public Books **Public**
```
GET '/books'
- Fetches all books in the database.
- Request Arguments: None.
- Returns an array of books.
{
    'success': True,
    'books': [{
            'id': 1,
            'title': 'Book 1',
            'description': 'A very interesting book.', 
            'author': 'The First Author'
        },
        {
            'id': 2,
            'title': 'Book 2',
            'description': 'A very interesting book.', 
            'author': 'The Second Author'
        }]
}
```

#### Add New Book **Requires Admin or Library-Manager Roles**
```
POST '/books'
- Adds a new book to the database and requires authentication and post:books permission.
- Request Arguments: 
    body = {
        'title': 'New Book',
        'description': 'A very interesting book.', 
        'author': 'The Author'
    }
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns the newly created book.
{
    'success': True,
    'book': {
        'id': 1
        'title': 'New Book',
        'description': 'A very interesting book.', 
        'author': 'The Author'
    }
}
```

#### Update Book **Requires Admin or Library-Manager Roles**
```
PATCH '/books/${book_id}'
- updates an existing book in the database and requires authentication and update:books permission.
- Request Arguments: 
    body = {
        'title': 'New Book',
        'description': 'A very interesting book.', 
        'author': 'The Author'
    }
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns the updated book.
{
    'success': True,
    'book': {
        'id': 1
        'title': 'New Book',
        'description': 'A very interesting book.', 
        'author': 'The Author'
    }
}
```

#### Delete Book **Requires Admin**
```
DELETE '/books/${book_id}'
- deletes an existing book in the database and requires authentication and delete:books permission.
- Request Arguments: 
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns the deleted book.
{
    'success': True,
    'book': {
        'id': 1
        'title': 'New Book',
        'description': 'A very interesting book.', 
        'author': 'The Author'
    }
}
```

#### Search Book **Public**
```
POST '/books/search'
- Searches for all books that matches the given search term.
- Request Arguments: 
    body = {
            'searchTerm': 'any text',
        }
- Returns a list of matched books.
{
    'success': True,
    'books': [{
            'id': 1,
            'title': 'Book 1',
            'description': 'A very interesting book.', 
            'author': 'The First Author'
        },
        {
            'id': 2,
            'title': 'Book 2',
            'description': 'A very interesting book.', 
            'author': 'The Second Author'
        }]
}
```




### **Library Endpoint**

#### Get User's Library **Requires Normal Authorization**
```
GET '/library'
- Fetches all books in user's library and requires authenticated user.
- Request Arguments: 
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Returns an array of user's books.
{
    'success': True,
    'books': [{
            'id': 1,
            'title': 'Book 1',
            'description': 'A very interesting book.', 
            'author': 'The First Author'
        },
        {
            'id': 2,
            'title': 'Book 2',
            'description': 'A very interesting book.', 
            'author': 'The Second Author'
        }]
}
```


#### Add Book to User's Library **Requires Normal Authorization**
```
POST '/library'
- Adds a book to the user's library and requires authenticated user.
- Request Arguments: 
    body = {
        'book_id': 1
    }
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Adds a book to user's library.
{
    'success': True,
    'book': {
        'id': 1
        'title': 'New Book',
        'description': 'A very interesting book.', 
        'author': 'The Author'
    }
}
```

#### Delete Book from User's Library **Requires Normal Authorization**
```
DELETE '/library/${book_id}'
- Deletes a book from the user's library and requires authenticated user.
- Request Arguments: 
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}'
    }
- Deletes the provided book from user's library.
{
    'success': True,
    'book': {
        'id': 1
        'title': 'New Book',
        'description': 'A very interesting book.', 
        'author': 'The Author'
    }
}
```