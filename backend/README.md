# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.


# DOCUMENTATION

INTRODUCTION:

REST TRIVIA v1
Build a Trivia Game using our API.
Trivia API is organized around REST. API has predictable resource-oriented URLs, accepts form-encoded request bodies, responds witj JSON-encoded



Allowed HTTPs requests:
PUT     : To create resource
POST    : Update resource
GET     : Get a resource or list of resources
DELETE  : To delete resource



ENDPOINTS:
GET 'api/categories'
GET '/api/questions'
GET '/api/categories/<int:category_id>/questions'
POST '/api/questions'
POST '/api/questions/searchQuestions'
POST '/api/quizzes'
DELETE '/api/questions/<int:question_id>'


#######################################
CATEGORIES:

-Endpoints: GET '/api/categories'

-Test endpoint: $ curl -X GET http://localhost:5000/api/categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

#######################################
QUESTIONS:

-Endpoints: GET '/api/questions'

-Test endpoint: $ curl -X GET http://localhost:5000/api/questions?page=1

-Fetches a dictionary of paginated questions along with categories.
-Response includes 10 questions per page
-Parameters:
    -page optional integer
    -defaulted to 1
-Response returns an object with the following keys and values.

{
    "success": True,
    "per_page": 10,
    "page": 1,
    "questions": []
    "total_questions": 27,
    "categories": {},
    "current_category": None,
    "next_num": 2,
    "prev_num": None,
    "has_next": True,
    "has_prev": False,
        }



#######################################
QESTIONS BY CATEGORY

-Endpoints: GET '/api/categories/<int:category_id>/questions'

-Test endpoint: $ curl -X GET http://localhost:5000/api/categories/2/questions

-Fetches a dictionary of paginated questions by given category.
-Response includes 10 questions per page
-Parameters:
    -page optional integer
    -defaulted to 1
-Response returns an object with the following keys and values.

{
    "success": True,
    "questions": [],
    "totalQuestions": 26),
    "currentCategory": None
}


################################
CREATE QUESTIONS

-Endpoints: POST '/api/questions'

-Fetches paginated updated questions including new question.
-Response includes 10 questions per page
-Body paylod example:

{
    "question", "What year statue of Liberty was built",
    "answer", 1986,
    category = 2,
    difficulty = 5


-Response returns an object with the following

{
    "success": True,
    "page": 1,
    "questions": [],
    "total_questions": 23,
}

################################################

SEARCH QUESTIONS BY KEYWORD

-Endpoints: POST '/api/questions/searchQuestions'


-Fetches  paginated questions that include posted search criteria.
-Response includes 10 questions per page
-Body paylod example:

{ "searchTerm": "which" }


-Response returns an object with the following

{
    "questions": [],
    "totalQuestions": 27,
    "currentCategory": None
}



###############################

GET A QUESTION BY CATEGORY ID OR ALL

-Endpoints: POST '/api/quizzes'


-Fetches a random question based on category id or one question from all categories if no id is given.
-Response includes 1 question
-Body paylod example:

{   "previous_questions": [],
    "quiz_category": 2
}


-Response returns an object with the following

{
    "success": True,
    "question": {}
}

###########################
DELETE QUESTION

-Endpoints: DELETE '/api/questions/<int:question_id>'

-Deletes a question based on given category id
-Parameters:
    -category id requires integer

-Response returns an object with the following
{
    "success": True,
    "deleted": 2,
    "total_questions": 26,
    "message":  "Question with {question_id} has been successfully deleted"
}




Description Of Usual Server Responses:

-200 OK - the request was successful (some API calls may return 201 instead)

-201 Created - the request was successful and a resource was created.

-400 Bad Request - the request could not be understood or was missing required parameters.

-404 Not Found - resource was not found.








```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
