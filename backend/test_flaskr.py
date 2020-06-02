import os
import unittest
import json
import math
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["data"]["success"], True)
        self.assertTrue(data["data"]["total_questions"])
        self.assertTrue(len(data["data"]["questions"]))
        self.assertTrue(data["data"]['categories'])
        self.assertFalse(data["data"]["current_category"])
    
    def test_404_sent_requesting_beyond_valid_page(self):
        
        res = self.client().get("/api/questions?page=1000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_pagination_is_ten(self):
        res = self.client().get("/api/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(len(data['data']['questions']), 10)
    
    def test_pagination_has_next_prev_page(self):
        # Page!:
        res_page1 = self.client().get("/api/questions?page=1")
        data_page1 = json.loads(res_page1.data)
        self.assertTrue(data_page1["data"]["has_next"], True)
        self.assertFalse(data_page1["data"]["has_prev"], False)
        
        
        # Page2:
        res_page2 = self.client().get("/api/questions?page=2")
        data_page2 = json.loads(res_page2.data)
        self.assertEqual(data_page2["data"]["page"], 2)
        self.assertEqual(data_page2["data"]["prev_num"], 1)

    
    
    ## IT CAN DELETE QUEATIONS
    # def test_delete_questions(self):
    #     res = self.client().delete('/api/questions/17')
    #     data = json.loads(res.data)
        
    #     print("RES", res.data)
    #     question = Question.query.filter(Question.id==17).one_or_none()
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 17)
    #     self.assertEqual(data["message"], "Question with 17 has been successfully deleted" )
    #     self.assertTrue(data["total_questions"])
        
    def test_404_question_does_not_exist(self):
        res = self.client().delete('/api/questions/9999')
        data = json.loads(res.data)
        print("TEST", data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data['message'], 'unprocessable')
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()