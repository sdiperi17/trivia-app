import os
import random
import math
import json
from crypt import methods
from idlelib import query
import werkzeug
from sqlalchemy.sql.expression import func
from flask import Flask, abort, flash, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
from models import Category, Question, db, setup_db

QUESTIONS_PER_PAGE = 10



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "super secret key"
    setup_db(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, allow_headers='Content-Type')

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    #adds some headers to the response
    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Conetent-Type, Authorization, false')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE, OPTIONS')
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
      categories_list = Category.query.order_by(Category.id).all()
      if len(categories_list) == 0:
        abort(404)  
      categories = Category.format_to_dict(Category, categories_list)

      return jsonify({"results": categories})
    
    

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
      
      try:
        questions_all = Question.query.order_by(Question.id).all()
        paginated_questions = Question.query.order_by(Question.id).paginate(page, per_page=QUESTIONS_PER_PAGE, error_out=False)

        if len(paginated_questions.items) is 0:
          abort(404)
 
        categories_result = Category.query.order_by(Category.id).all()
        categories= Category.format_to_dict(Category, categories_result)
        
        questions = [question.format() for question in paginated_questions.items]
        
        result = {
        "success": True,
        "per_page": paginated_questions.per_page,
        "page": paginated_questions.page,
        "questions": questions,
        "total_questions": paginated_questions.total,
        "categories": categories,
        "current_category": None,
        "next_num": paginated_questions.next_num,
        "prev_num": paginated_questions.prev_num,
        "has_next": paginated_questions.has_next,
        "has_prev": paginated_questions.has_prev,
        }
        print("DOCS", result)
        
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
  
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
          
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
      def format_paginated_questions(selection):
        question_dict={}
        for key, value in vars(selection).items():
          print("key", key)
          question_dict[key] =  value
        return question_dict
      body = request.get_json()
      question = body.get("question", None)
      answer = body.get("answer", None)
      category = body.get("category", None)
      difficulty = body.get("difficulty", None)
      
      if ((question == None) or (answer == None) or (difficulty == None) or (category == None)):
        abort(422)
        
        
      try:
        new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
        new_question.insert()
      
        questions_all = Question.query.order_by(Question.id).all()
        question_num = len(questions_all)
        page = math.ceil(question_num/QUESTIONS_PER_PAGE)
        questions_dict = Question.query.order_by(Question.id).paginate(page, per_page=QUESTIONS_PER_PAGE, error_out=False)
 

        current_questions = format_paginated_questions(questions_dict)
        questions = [question.format() for question in current_questions["items"]]
        
        return jsonify({
        "success": True,
        "page": current_questions["page"],
        "questions": questions,
        "total_questions": current_questions["total"],
        })
      
      except:
        abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  
    @app.route("/api/questions/searchQuestions", methods=["POST"])
    def search_questions():
      body = request.get_json()
      search_key = body["searchTerm"]
      questions_result = Question.query.filter(Question.question.ilike(f"%{search_key}%")).all()
      questions = [question.format() for question in questions_result]
      data = {
        "questions": questions,
        "totalQuestions": len(questions),
        "currentCategory": None
      }
      
      return jsonify(data)
  
  
  
    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  
    @app.route("/api/categories/<int:category_id>/questions", methods=["GET"])
    def get_question_by_category(category_id):
      questions_data = Question.query.filter(Question.category == category_id).paginate(1, per_page=QUESTIONS_PER_PAGE, error_out=False)
      questions = [question.format() for question in questions_data.items]
      
      if len(questions) == 0:
        abort(404)
      
      result = {
        "questions": questions,
        "totalQuestions": len(questions),
        "currentCategory": None
      }
      
      return jsonify(result)
  
  

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
  
    @app.route("/api/quizzes", methods = ["POST"])
    def get_random_questions_by_category():
      body = request.get_json()
      previous_questions = body["previous_questions"]
      search_criteria = json.loads(request.data.decode('utf-8'))
      quiz_category_id = search_criteria["quiz_category"]["id"]
 
      try:
        if request.data:
            category_id = search_criteria["quiz_category"]["id"]
        result = {}
        if (('quiz_category' in search_criteria and quiz_category_id) and 'previous_questions' in search_criteria):
          questions_query = Question.query.filter_by(category=search_criteria['quiz_category']['id']).filter(Question.id.notin_(search_criteria["previous_questions"])).all()
          total_question = len(questions_query)
          if total_question > 0:
            result = {
              "success": True,
              "question": Question.format(questions_query[random.randrange(0, total_question)])
            }
          else:
            result = {
              "success": True,
              "question": None
            }
          return jsonify(result)
        else:
          questions_query_all = Question.query.filter(Question.id.notin_(search_criteria["previous_questions"])).all()
          total_question = len(questions_query_all)
          result = {
            "success": True,
            "question": Question.format(questions_query_all[random.randrange(0, total_question)])
          }
          return jsonify(result)     
      except:
        abort(422)
                
    
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







