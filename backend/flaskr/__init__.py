import os
import random
from crypt import methods

import werkzeug
from flask import Flask, abort, flash, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
from models import Category, Question, db, setup_db

QUESTIONS_PER_PAGE = 10




def paginate_questions(request, selection):
  page=request.args.get('page', 1, type=int)
  start = (page-1)*QUESTIONS_PER_PAGE
  end = start+QUESTIONS_PER_PAGE
  
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "super secret key"
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    #adds some headers to the response
    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Conetent-Type, Authorization, false')
      # response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE, OPTIONS')
      return response
       
    @app.route('/')
    def get_home():
      return jsonify({"Message": "Hello Shamu"})
    
    
    
    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/api/categories')
    def get_categories():
      def format_data(categories):
        data = []
        for category in categories:
          data.append({
          "id": category.id,
          "type": category.type,
          })
        return data
      categories = Category.query.order_by(Category.id).all()
      
      data = format_data(categories)
      
      return jsonify({"results": data})
    
    

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    
    @app.route('/api/questions')
    def get_questions():
      page = request.args.get('page', 1, int)
      def format_categories(categories):
        data = {}
        for category in categories:
          data[category.id] = category.type
        return data
      
      def format_paginated_questions(selection):
        question_dict={}
        for key, value in vars(selection).items():
          print("key", key)
          question_dict[key] =  value
        return question_dict
      
      try:
        questions_all = Question.query.order_by(Question.id).all()
        questions_dict = Question.query.order_by(Question.id).paginate(page, per_page=QUESTIONS_PER_PAGE, error_out=False)

        if len(questions_dict.items) is 0:
          abort(404)
 
        categories = Category.query.order_by(Category.id).all()
        current_questions = format_paginated_questions(questions_dict)
        questions = [question.format() for question in current_questions["items"]]
      
        print("TEST", current_questions["page"])
        result = {
        "success": True,
        "per_page": current_questions["per_page"],
        "page": current_questions["page"],
        "questions": questions,
        "total_questions": current_questions["total"],
        "categories": format_categories(categories),
        "current_category": None,
        "next_num": questions_dict.next_num,
        "prev_num": questions_dict.prev_num,
        "has_next": questions_dict.has_next,
        "has_prev": questions_dict.has_prev,
        }
        return jsonify({"data": result})
    
    
      except:
        flash("No questions found on the record")
        abort(404)
         
      
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  ##one_or_none .one_or_none(), returns None if there is no data in your database, or an instance of class. If there is exactly one data in your database it returns one, or raises an exception if there are multiple products named apple in your database.
  
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
      print("ID", question_id)
      try:
        question = Question.query.filter_by(id = question_id).one_or_none()
        question.delete()
        
        if question is None:  
          abort(404)
          
        question_all=Question.query.order_by(Question.id).all()
        
        return jsonify({
          "success": True,
          "deleted": question_id,
          "total_questions": len(question_all),
          "message":  f"Question with {question_id} has been successfully deleted"
        })
            
      except:
        #422 Unprocessable Entity
        abort(422)
  
    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  
    @app.route("/api/questions", methods = ["POST"])
    def create_trivia_question():
      print("REQUEST", request.data)
      return jsonify({"message": "SHAMUE"})

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
      }), 404

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
      }), 400
      
      
    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
      }), 422
      
    return app
