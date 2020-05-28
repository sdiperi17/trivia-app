import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

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

    # @app.route('/questions')
    # def get_question():
    #   questions = Question.query.order_by(Question.id).all()
    #   print("QUESTIONS", questions)
    #   return jsonify({'message': "TEST"})
    @app.route('/api/questions')
    def retrieve_questions():
      def format_categories(categories):
        data = {}
        for category in categories:
          data[category.id] = category.type
        print("FUN", data)   
        return data
      
      
      questions_all = Question.query.order_by(Question.id).all()
      categories = Category.query.order_by(Category.id).all()
     
      current_questions = paginate_questions(request, questions_all)
  
      if len(current_questions) == 0:
       abort(404)   
      
      result = {
        "success": True,
        "questions": current_questions,
        "total_questions": len(questions_all),
        "categories": format_categories(categories),
        "current_category": None
      }
      # print("TESTME", result)
      return jsonify({"data": result})
    
    

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  ##one_or_none .one_or_none(), returns None if there is no data in your database, or an instance of class. If there is exactly one data in your database it returns one, or raises an exception if there are multiple products named apple in your database.
  
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def test(question_id):
      try:
        question = Question.query.filter(Question.id == question_id).one_or_none()
      
        if question is None:
              abort(404)
        
        question.delete()
        question_all=Question.query.order_by(Question.id).all()
        current_questions=paginate_questions(request, question_all)
        
        return jsonify({
          "success": True,
          "deleted": question_id,
          "questions": current_questions,
          "total_questions": len(question_all)
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

    return app
